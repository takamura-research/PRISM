### BERTScore Model Download and Offline Execution

The evaluation pipeline runs BERTScore in offline mode to prevent unexpected model downloads during automated evaluation.

If the required model is not available in the local Hugging Face cache, BERTScore evaluation is skipped and the error is recorded. Cloud-generated reference responses are retained, and the pipeline continues with optional Ragas evaluation (when enabled and properly configured) and CSV export.

To enable BERTScore, download the required model separately before starting the evaluation pipeline:

```bash
python3 -c "from transformers import AutoModel, AutoTokenizer; m='bert-base-multilingual-cased'; AutoTokenizer.from_pretrained(m); AutoModel.from_pretrained(m)"
```

The initial download may take several minutes, depending on network conditions.

If the download stalls, check Hugging Face connectivity and retry the download independently. The evaluation pipeline can still operate without BERTScore, although semantic similarity scores will not be available.

Start the pipeline normally:

```bash
python3 pipeline_structured.py --ragas
```

**Note:** Previously processed evaluation jobs are tracked in a local SQLite database. Failed or partially completed evaluations are not automatically retried. Therefore, downloading the BERTScore model after an evaluation does not automatically update previously saved results. Re-evaluation must be performed explicitly.