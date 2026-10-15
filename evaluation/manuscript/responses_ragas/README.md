## Ragas Evaluation Results

This directory contains the Ragas evaluation datasets and results for the PRISM manuscript.

The evaluation included 30 scientific questions answered by the local Gemma 3 model under two configurations: with RAG and without RAG.

The following files are provided:

- `prism_ragas_5metrics_results.csv`: Question-level responses, reference answers, evaluation contexts, and five Ragas metrics for both configurations.
- `prism_ragas_5metrics_summary.csv`: Summary statistics for the five evaluation metrics.
- `prism_evidence_audit.csv`: Retrieved evidence candidates and their associated retrieval scores for the 30 evaluation questions.

The primary metrics reported in the manuscript were Faithfulness and Answer Correctness.

**Important methodological note:** The same evaluation-specific retrieved contexts were used for both RAG and non-RAG responses to provide a common basis for assessment. The non-RAG configuration generated its answers without access to the source PDF. Context Precision and Context Recall therefore should not be interpreted as direct comparisons of retrieval performance between the two configurations.

These files document the evaluation results reported in the manuscript and are distinct from the example outputs generated during notebook testing.

The evaluation was performed using Ragas 0.2.15, with `gpt-4o-mini` as the evaluator LLM (temperature = 0) and `text-embedding-3-small` as the embedding model. The evaluation procedure and configuration are documented in `PRISM_Ragas_5Metrics_Evaluation_Colab.ipynb`.
