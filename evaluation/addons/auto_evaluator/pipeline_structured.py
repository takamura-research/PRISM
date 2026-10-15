"""LM Studio GUI conversation watcher and multi-provider evaluation. Python 3.10+."""
import argparse
import base64
import csv
import hashlib
import json
import logging
import os
import re
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

FIELDS = ['job_id','timestamp_utc','conversation','turn_index','local_model','query','local_response','local_answers','evaluated_question_count',
          'chatgpt_response','claude_response','gemini_response','bert_chatgpt','bert_claude',
          'bert_gemini','bert_mean','ragas_answer_relevancy','ragas_answer_correctness',
          'ragas_faithfulness','ragas_status','retrieved_contexts_count','pdf_paths','status','error']


def chosen(msg):
    versions = msg.get('versions', [])
    if not versions: return {}
    idx = msg.get('currentlySelected', 0)
    return versions[idx] if isinstance(idx, int) and 0 <= idx < len(versions) else versions[-1]


def text_parts(parts):
    if isinstance(parts, str): return parts
    return '\n'.join(p.get('text','') for p in (parts or []) if isinstance(p,dict) and p.get('type') == 'text').strip()


def extract(data, source):
    history, pdf_ids, context = [], [], []
    for idx, msg in enumerate(data.get('messages', [])):
        v = chosen(msg)
        role = v.get('role')
        if role == 'user':
            content = v.get('content', [])
            for item in content:
                if item.get('type') == 'file' and item.get('fileType') == 'application/pdf':
                    fid = item.get('fileIdentifier')
                    if fid and fid not in pdf_ids: pdf_ids.append(fid)
            body = text_parts(content)
        elif role == 'assistant':
            context = []  # citations for this assistant turn only
            blocks = [s for s in v.get('steps',[]) if s.get('type') == 'contentBlock']
            body = '\n'.join(text_parts(s.get('content', [])) for s in blocks).strip()
            for s in v.get('steps', []):
                if s.get('type') == 'citationBlock' and s.get('citedText'):
                    context.append(s['citedText'])
            if blocks:
                gen = blocks[-1].get('genInfo',{})
                model = gen.get('identifier') or v.get('senderInfo',{}).get('senderName','')
                stop = gen.get('stats',{}).get('stopReason')
            else: model, stop = '', None
        else: continue
        if body:
            history.append({'role':role,'content':body,'index':idx,
                            'model':model if role=='assistant' else '',
                            'stop':stop if role=='assistant' else None})
    if len(history) < 2 or history[-1]['role'] != 'assistant' or history[-2]['role'] != 'user':
        return None
    if history[-1]['stop'] not in ('eosFound','stopStringFound','maxPredictedTokensReached'):
        # Some versions omit stop reason; file stability is then the completion signal.
        if history[-1]['stop'] is not None: return None
    last = history[-1]
    # For follow-up prompts, preserve all previous turns (including assistant responses).
    return {'conversation':str(source),'turn_index':last['index'], 'query':history[-2]['content'],
            'local_response':last['content'],'local_model':last['model'],
            'history':history[:-1], 'pdf_ids':pdf_ids, 'retrieved_contexts':list(dict.fromkeys(context))}


def resolve_pdfs(ids, root):
    resolved=[]
    for fid in ids:
        # identifiers are filenames from LM Studio, never accept directory traversal
        name=Path(fid).name
        if name != fid: raise ValueError('Unsafe PDF identifier')
        p=root/name
        if not p.is_file(): raise FileNotFoundError(f'PDF missing: {p}')
        if p.suffix.lower() != '.pdf': raise ValueError(f'Not a PDF: {p}')
        resolved.append(p)
    return resolved


def cloud_history(job):
    return [{'role':h['role'],'content':h['content']} for h in job['history']]


def ask_openai(history,pdfs,model):
    from openai import OpenAI
    msgs=[]
    for i,h in enumerate(history):
        if i == 0 and h['role'] == 'user':
            content=[{'type':'input_text','text':h['content']}]
            for pdf in pdfs:
                content.append({'type':'input_file','filename':pdf.name,
                                'file_data':'data:application/pdf;base64,'+base64.b64encode(pdf.read_bytes()).decode()})
            msgs.append({'role':'user','content':content})
        else: msgs.append({'role':h['role'],'content':h['content']})
    resp=OpenAI(timeout=180).responses.create(model=model,input=msgs)
    return resp.output_text.strip()


def ask_claude(history,pdfs,model):
    import anthropic
    msgs=[]
    for i,h in enumerate(history):
        if i==0 and h['role']=='user':
            content=[]
            for pdf in pdfs:
                content.append({'type':'document','source':{'type':'base64','media_type':'application/pdf',
                                  'data':base64.b64encode(pdf.read_bytes()).decode()}})
            content.append({'type':'text','text':h['content']})
            msgs.append({'role':'user','content':content})
        else: msgs.append({'role':h['role'],'content':h['content']})
    result=anthropic.Anthropic(timeout=180).messages.create(model=model,max_tokens=4096,messages=msgs)
    return '\n'.join(b.text for b in result.content if getattr(b,'type',None)=='text').strip()


def ask_gemini(history,pdfs,model):
    from google import genai
    from google.genai import types
    contents=[]
    for i,h in enumerate(history):
        parts=[]
        if i==0 and h['role']=='user':
            parts += [types.Part.from_bytes(data=p.read_bytes(),mime_type='application/pdf') for p in pdfs]
        parts.append(types.Part.from_text(text=h['content']))
        contents.append(types.Content(role='user' if h['role']=='user' else 'model',parts=parts))
    with genai.Client(api_key=os.environ['GEMINI_API_KEY']) as client:
        resp=client.models.generate_content(model=model,contents=contents)
        return (resp.text or '').strip()


def parse_answer_rows(text):
    """Extract numbered Answer cells from a Markdown No|Question|Answer table.

    Returns [(number, question, answer), ...]. Handles literal <br> and
    escaped Markdown pipes (\\|). Never evaluates the table header or question.
    """
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.I)
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        # Split only unescaped pipe delimiters.
        cells = [c.strip().replace(r'\|', '|') for c in re.split(r'(?<!\\)\|', line)]
        if cells and not cells[0]: cells.pop(0)
        if cells and not cells[-1]: cells.pop()
        if len(cells) < 3 or not re.fullmatch(r'\d+', cells[0]):
            continue
        number, question = int(cells[0]), cells[1]
        answer = '|'.join(cells[2:]).strip()
        if not question or not answer:
            raise ValueError(f'Empty question/answer in row {number}')
        if any(number == old[0] for old in rows):
            raise ValueError(f'Duplicate question number {number}')
        rows.append((number, question, answer))
    if not rows:
        raise ValueError('No numbered Markdown No|Question|Answer rows found')
    return rows


def aligned_answers(local_text, cloud_text):
    """Require matching row IDs for tables; accept plain cloud answer for one row."""
    local_rows = parse_answer_rows(local_text)
    try:
        cloud_rows = parse_answer_rows(cloud_text)
    except ValueError as exc:
        # Plain-text cloud answer is valid only for a single-question evaluation.
        if len(local_rows) != 1 or re.search(r'(?m)^\s*\|', cloud_text):
            raise ValueError(f'Cloud response cannot be aligned: {exc}') from exc
        plain = cloud_text.strip()
        if not plain:
            raise ValueError('Empty cloud response')
        return [(local_rows[0][1], local_rows[0][2], plain)]
    local_map = {n: (q, a) for n, q, a in local_rows}
    cloud_map = {n: (q, a) for n, q, a in cloud_rows}
    if local_map.keys() != cloud_map.keys():
        raise ValueError('Local/cloud question numbers differ')
    for n in local_map:
        if re.sub(r'\s+', ' ', local_map[n][0]).strip() != re.sub(r'\s+', ' ', cloud_map[n][0]).strip():
            raise ValueError(f'Local/cloud question differs at row {n}')
    return [(local_map[n][0], local_map[n][1], cloud_map[n][1]) for n in local_map]


def score_bert(local, cloud):
    """BERTScore F1: compare Answer cells only; mean over aligned questions."""
    from bert_score import score
    names = [n for n in ('chatgpt', 'claude', 'gemini') if cloud.get(n)]
    if not names: return {}
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
    candidates, references, owners = [], [], []
    for name in names:
        for _, local_answer, cloud_answer in aligned_answers(local, cloud[name]):
            candidates.append(local_answer)
            references.append(cloud_answer)
            owners.append(name)
    logging.info('BERTScore: comparing Answer cells only (%d aligned pairs)', len(owners))
    _, _, f = score(candidates, references,
                    model_type=os.getenv('BERT_MODEL', 'bert-base-multilingual-cased'),
                    num_layers=9, lang='ja', verbose=False)
    scores = {}
    for name, value in zip(owners, f):
        scores.setdefault(name, []).append(float(value))
    return {name: sum(values)/len(values) for name, values in scores.items()}


def score_ragas(job, reference):
    """RAGAS 0.2.x; score each aligned Question/Answer row, then average."""
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import answer_relevancy, answer_correctness, faithfulness
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    metrics = [answer_relevancy, answer_correctness]
    contexts = job['retrieved_contexts']
    if contexts: metrics.append(faithfulness)
    aligned = aligned_answers(job['local_response'], reference)
    sample = {'question': [q for q, _, _ in aligned],
              'answer': [a for _, a, _ in aligned],
              'ground_truth': [r for _, _, r in aligned],
              'contexts': [contexts for _ in aligned]}
    res = evaluate(Dataset.from_dict(sample), metrics=metrics,
                   llm=ChatOpenAI(model=os.getenv('RAGAS_JUDGE_MODEL', 'gpt-4o-mini'), temperature=0),
                   embeddings=OpenAIEmbeddings(model=os.getenv('RAGAS_EMBEDDING_MODEL', 'text-embedding-3-small')),
                   raise_exceptions=False)
    frame = res.to_pandas()
    result = {}
    for key in ('answer_relevancy', 'answer_correctness', 'faithfulness'):
        if key in frame.columns:
            values = [float(v) for v in frame[key] if v is not None and not __import__('math').isnan(float(v))]
            if values: result[key] = sum(values) / len(values)
    return result


def init_db(db):
    con=sqlite3.connect(db)
    con.execute('CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, status TEXT, updated REAL)')
    con.commit();return con


def run_job(job, args, con):
    jid=hashlib.sha256((job['conversation']+'|'+str(job['turn_index'])+'|'+job['local_response']).encode()).hexdigest()[:24]
    if con.execute('SELECT 1 FROM jobs WHERE id=? AND status IN ("done","partial","running")',(jid,)).fetchone(): return
    parse_answer_rows(job['local_response'])  # validate structure before API calls
    pdfs=resolve_pdfs(job['pdf_ids'],args.pdf_root)
    if not pdfs: raise ValueError('No PDF in conversation; same-PDF comparison cannot run')
    con.execute('INSERT OR REPLACE INTO jobs VALUES (?,?,?)',(jid,'running',time.time()));con.commit()
    row={k:'' for k in FIELDS}
    row.update(job_id=jid,timestamp_utc=datetime.now(timezone.utc).isoformat(),
               conversation=job['conversation'],turn_index=job['turn_index'],
               local_model=job['local_model'],query=job['query'],local_response=job['local_response'],
               pdf_paths=';'.join(str(p) for p in pdfs),retrieved_contexts_count=len(job['retrieved_contexts']))
    parsed_rows = parse_answer_rows(job['local_response'])
    row['local_answers'] = json.dumps([{'no': n, 'question': q, 'answer': a} for n,q,a in parsed_rows], ensure_ascii=False)
    row['evaluated_question_count'] = len(parsed_rows)
    errors=[]; cloud={}
    api_keys={'chatgpt':'OPENAI_API_KEY','claude':'ANTHROPIC_API_KEY','gemini':'GEMINI_API_KEY'}
    for name,fn,model in [('chatgpt',ask_openai,args.openai_model),('claude',ask_claude,args.claude_model),('gemini',ask_gemini,args.gemini_model)]:
        if not os.getenv(api_keys[name], '').strip():
            logging.info('SKIP %s: %s is not configured',name,api_keys[name])
            continue
        try:
            logging.info('Calling %s (%s)',name,model)
            cloud[name]=fn(cloud_history(job),pdfs,model)
            row[name+'_response']=cloud[name]
        except Exception as exc:
            logging.exception('%s failed',name);errors.append(f'{name}: {type(exc).__name__}: {exc}')
    try:
        bs=score_bert(job['local_response'],cloud)
        for name,val in bs.items():row['bert_'+name]=val
        if bs: row['bert_mean']=sum(bs.values())/len(bs)
    except Exception as exc:
        logging.warning('BERTScore unavailable (model not cached or runtime error): %s',exc);errors.append('bert: '+str(exc))
    if args.ragas and cloud and os.getenv('OPENAI_API_KEY', '').strip():
        try:
            # Explicit reference policy: ChatGPT is the designated reference.
            reference=cloud.get('chatgpt')
            if reference:
                rg=score_ragas(job,reference)
                for k,target in [('answer_relevancy','ragas_answer_relevancy'),
                                 ('answer_correctness','ragas_answer_correctness'),
                                 ('faithfulness','ragas_faithfulness')]:
                    if k in rg: row[target]=rg[k]
                row['ragas_status']='ok'
            else: row['ragas_status']='skipped: ChatGPT reference unavailable'
        except Exception as exc:
            logging.exception('RAGAS failed');row['ragas_status']='error';errors.append('ragas: '+str(exc))
    else: row['ragas_status']='skipped: disabled, no cloud response, or no OpenAI judge key'
    row['status']='done' if not errors else 'partial'
    row['error']=' | '.join(errors)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    if args.out.exists() and args.out.stat().st_size:
        with args.out.open('r', encoding='utf-8-sig', newline='') as existing:
            header = next(csv.reader(existing), [])
        if header != FIELDS:
            raise ValueError('Existing CSV has different columns; use --out results/evaluation_structured.csv')
    with args.out.open('a',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS)
        if f.tell()==0:w.writeheader()
        w.writerow(row)
    con.execute('UPDATE jobs SET status=?,updated=? WHERE id=?',(row['status'],time.time(),jid));con.commit()
    logging.info('Saved %s: %s',jid,row['status'])


def scan(args, con, observed):
    """Evaluate each stable file revision once, including skipped/invalid revisions."""
    files = [args.file] if args.file else args.conversations.glob('*.conversation.json')
    for file in files:
        if not file.exists():
            continue
        key = str(file.resolve())
        try:
            st = file.stat()
            sig = (st.st_mtime_ns, st.st_size)
            prev = observed.get(key)
            if prev is None:
                # On startup, existing files are baseline, not evaluation jobs.
                observed[key] = {'signature': sig, 'since': time.monotonic(),
                                 'handled': not args.process_existing}
                if not args.process_existing:
                    continue
            elif prev['signature'] != sig:
                observed[key] = {'signature': sig, 'since': time.monotonic(),
                                 'handled': False}
                continue
            entry = observed[key]
            if entry['handled'] or time.monotonic() - entry['since'] < args.settle:
                continue
            raw = file.read_bytes()
            after = file.stat()
            if (after.st_mtime_ns, after.st_size) != sig:
                continue
            data = json.loads(raw)
            job = extract(data, file)
            # Never run a second time for the same unchanged file revision,
            # even when no PDF, no completed turn, or an API failure occurs.
            entry['handled'] = True
            if job is None:
                continue
            if not job['pdf_ids']:
                logging.info('SKIP no PDF: %s', file.name)
                continue
            try:
                run_job(job, args, con)
            except Exception as exc:
                logging.error('Evaluation skipped for %s: %s', file.name, exc)
        except (OSError, json.JSONDecodeError) as exc:
            # Retry incomplete writes only; stable invalid files can be ignored
            # until they change again.
            if time.monotonic() - observed[key]['since'] >= args.settle * 2:
                observed[key]['handled'] = True
                logging.warning('Invalid/unreadable conversation %s: %s', file.name, exc)


def main():
    load_dotenv()
    p=argparse.ArgumentParser()
    p.add_argument('--conversations',type=Path,default=Path.home()/'.lmstudio/conversations')
    p.add_argument('--pdf-root',type=Path,default=Path.home()/'.lmstudio/user-files')
    p.add_argument('--file',type=Path,help='Process a specific conversation JSON or exported .txt')
    p.add_argument('--out',type=Path,default=Path('results/evaluation.csv'))
    p.add_argument('--db',type=Path,default=Path('results/state.sqlite3'))
    p.add_argument('--process-existing',action='store_true',help='Allow API calls for preexisting turns')
    p.add_argument('--dry-run',action='store_true',help='Print parsed latest turn; no API calls')
    p.add_argument('--ragas',action='store_true',help='Enable additional RAGAS judge API calls')
    p.add_argument('--settle',type=float,default=8.0)
    p.add_argument('--interval',type=float,default=2.0)
    p.add_argument('--openai-model',default=os.getenv('OPENAI_MODEL','gpt-4.1-mini'))
    p.add_argument('--claude-model',default=os.getenv('CLAUDE_MODEL','claude-sonnet-4-5'))
    p.add_argument('--gemini-model',default=os.getenv('GEMINI_MODEL','gemini-2.5-flash'))
    args=p.parse_args()
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
    if args.dry_run:
        if not args.file: p.error('--dry-run requires --file')
        job=extract(json.loads(args.file.read_text(encoding='utf-8')),args.file)
        if not job: p.error('No completed user/assistant turn found')
        print(json.dumps({k:v for k,v in job.items() if k not in ('history','retrieved_contexts')},ensure_ascii=False,indent=2))
        print('history turns:',len(job['history']),'retrieved contexts:',len(job['retrieved_contexts']))
        return
    args.db.parent.mkdir(parents=True,exist_ok=True)
    con=init_db(args.db)
    observed={}
    logging.info('Watching %s (existing=%s)',args.conversations,args.process_existing)
    try:
        while True:
            scan(args,con,observed)
            if args.file: break
            time.sleep(args.interval)
    except KeyboardInterrupt: logging.info('Stopped')
    finally: con.close()

if __name__=='__main__':main()
