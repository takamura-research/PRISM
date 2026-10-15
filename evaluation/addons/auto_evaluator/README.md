# PRISM LM Studio GUI Auto-Evaluator (Prototype)

This tool provides an automated evaluation pipeline for local large language models (LLMs) running in LM Studio. It is implemented as an additional functionality of the PRISM framework to support automated, document-based Q&A evaluation.

The pipeline monitors LM Studio conversation files in read-only mode and evaluates eligible responses without modifying the LM Studio GUI or inference workflow.

**Environment:** Python 3.10+ / macOS

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory and configure the API keys for the cloud-based LLM providers:

```dotenv
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
```

The pipeline supports ChatGPT (OpenAI), Claude (Anthropic), and Gemini (Google). Only providers with configured API keys are used. All three API keys are required to obtain reference responses from all three providers.

**Security:** Never upload or commit your `.env` file containing actual API keys to GitHub.

The BERTScore model (`bert-base-multilingual-cased` by default) must also be available in the local Hugging Face cache before evaluation.

## Verify Conversation Parsing

Before running the evaluation, verify that the pipeline can correctly read an LM Studio conversation file without making external API calls:

```bash
python3 pipeline_structured.py \
  --file '/path/to/test.conversation.json' \
  --dry-run
```

This command extracts the latest completed conversation turn and displays the parsed information without performing cloud-based evaluation.

## Start Automated Evaluation

To start monitoring new LM Studio responses and calculate BERTScore:

```bash
python3 pipeline_structured.py
```

To enable additional Ragas evaluation:

```bash
python3 pipeline_structured.py --ragas
```

Keep the terminal process running while interacting with the local LLM through the standard LM Studio GUI.

The pipeline monitors conversation files and processes eligible completed responses after the files remain unchanged for approximately eight seconds.

Existing conversations are skipped at startup by default. To include existing conversation files, use:

```bash
python3 pipeline_structured.py --process-existing
```

To evaluate a specific conversation file:

```bash
python3 pipeline_structured.py \
  --file '/path/to/file.conversation.json' \
  --process-existing
```

**Note:** Evaluation may involve external API calls and associated usage charges.

## Evaluation Workflow

When a source research paper (PDF) is attached to an LM Studio conversation and the local LLM generates a numbered Markdown Q&A table, the pipeline performs the following operations:

1. **Conversation extraction:** Extracts questions, local LLM answers, and relevant conversation history.
2. **Reference answer generation:** Sends the source PDF and conversation history to configured cloud-based LLMs to obtain reference answers.
3. **BERTScore evaluation:** Calculates semantic similarity between local LLM answers and corresponding cloud-generated reference answers.
4. **Optional Ragas evaluation:** Calculates Answer Relevancy and Answer Correctness, with Faithfulness additionally evaluated when retrieved contexts are available.
5. **Result export:** Saves evaluation scores, responses, and processing information to a CSV file.

The required response format is:

```markdown
| No | Question | Answer |
|---|---|---|
| 1 | Question 1 | Answer 1 |
| 2 | Question 2 | Answer 2 |
```

BERTScore is calculated using only the answer fields. Question numbers and question text are used to verify alignment between local and cloud-generated responses.

## Output

Evaluation results are saved to:

```text
results/evaluation.csv
```

The pipeline also maintains a local SQLite database for tracking processed evaluation jobs:

```text
results/state.sqlite3
```

The CSV output includes:

- Local LLM responses and cloud-generated reference responses
- BERTScore (F1) for each available cloud reference model and their mean
- Optional Ragas evaluation metrics
- Evaluated question counts and conversation metadata
- Processing status and error information

## Design Decisions and Limitations

- **Input requirements:** A source PDF and a numbered Markdown Q&A table are required. PDF attachments are resolved from `~/.lmstudio/user-files/` by default.
- **Conversation monitoring:** The pipeline monitors `~/.lmstudio/conversations/` and processes the latest eligible completed assistant response. Intermediate turns may be missed if multiple responses are generated between scans.
- **Conversation context:** Previous user and assistant messages are included when generating cloud-based reference answers. LM Studio system prompts and GUI-specific retrieval instructions are not reproduced.
- **Reference generation:** Cloud providers receive the source PDF and conversation history but may interpret or process the document differently. Identical retrieval behavior is not guaranteed.
- **BERTScore:** BERTScore measures semantic similarity rather than factual correctness. The default configuration uses `bert-base-multilingual-cased` with nine layers. Scores are averaged across aligned Q&A items for each reference provider.
- **Ragas:** The implementation uses Ragas 0.2.15. Answer Correctness uses the ChatGPT-generated response as its reference rather than an independently validated expert answer. Ragas evaluation additionally requires OpenAI API access.
- **Faithfulness:** Faithfulness is calculated only when citation-derived contexts are available in the LM Studio conversation. These contexts may not represent the complete retrieved information.
- **Evaluation coverage:** Context Precision and Context Recall are not implemented. The pipeline does not calculate ROUGE-L or BLEU.
- **Reproducibility:** Evaluation results depend on model versions, generated reference answers, evaluation settings, and software dependencies.
- **Error handling:** Partial evaluation results may be saved when individual providers or metrics fail. Previously processed jobs are tracked locally, and failed or partial evaluations are not automatically retried.

## Privacy Considerations and Future Development

The current evaluation pipeline uses external LLM APIs (OpenAI, Anthropic, and Google) for reference answer generation. Source PDFs and conversation histories are transmitted to the corresponding external service providers when their APIs are used. Optional Ragas evaluation also involves external API calls.

Consequently, although local LLM inference is performed within LM Studio, **the current evaluation pipeline does not provide a fully local, privacy-preserving evaluation environment**.

Only documents and conversation data authorized for transmission to external providers should be used. Confidential, sensitive, or otherwise restricted information should not be processed without appropriate authorization and data protection measures.

The primary objective of this prototype is to demonstrate **the feasibility of automating the evaluation workflow as an additional functionality of PRISM**, rather than to establish a fully privacy-preserving evaluation system.

Future development will focus on integrating a dedicated local LLM-based evaluation system to replace external API-dependent reference generation and evaluation. This approach aims to enable both response generation and evaluation to be performed entirely within a local computing environment, without transmitting evaluation data to external LLM providers.

The current implementation therefore represents an initial step toward integrating automated evaluation capabilities into PRISM while identifying the requirements for a fully local, privacy-preserving evaluation architecture.

**Note:** This tool is an additional evaluation utility for the PRISM framework and is not intended to reproduce the exact evaluation results reported in the manuscript.