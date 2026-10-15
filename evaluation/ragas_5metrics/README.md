# Ragas Five-Metric Evaluation Dataset
This directory contains the input datasets used to evaluate PRISM using five Ragas metrics.

## Input Files

| File | Description |
|---|---|
| `RAG_conversation_QA.csv` | LLM-generated answers obtained under the RAG condition. |
| `nRG_conversation_QA.csv` | LLM-generated answers obtained under the non-RAG condition. |
| `gold_qa_draft.csv` | Reference answers used for the evaluation. |

The source research paper (`KB01_Umezawa_2025.pdf`) is available in the root directory of this repository.


## Evaluation Procedure
The datasets can be evaluated using [PRISM_Ragas_5Metrics_Evaluation_Colab.ipynb](../PRISM_Ragas_5Metrics_Evaluation_Colab.ipynb).

The notebook accepts the source research paper, RAG-generated answers, non-RAG-generated answers, and an optional reference-answer CSV file.

The following five metrics are calculated:

1. Answer Correctness
2. Answer Relevancy
3. Faithfulness
4. Context Precision
5. Context Recall

The `gold_qa_draft.csv` file was used as the reference-answer dataset for the five-metric evaluation. The RAG and non-RAG responses were evaluated using the same reference-answer dataset and evaluation procedure to ensure consistency between conditions. Individual metrics assess different aspects of response quality and do not necessarily represent direct comparisons with the reference answers.

The evaluation results can be exported as CSV files for further analysis.


## Reproducibility Note
These files document the input datasets selected for the Ragas evaluation. The resulting metric values may vary depending on the evaluation models, software versions, and execution settings.


## Reproducibility and Validation
The datasets provided in this directory correspond to those used in the evaluation reported in the manuscript.

The evaluation was reproduced using the `PRISM_Ragas_5Metrics_Evaluation_Colab.ipynb` notebook, and the resulting metrics were found to be broadly consistent with those reported in the manuscript.

Exact numerical agreement is not guaranteed, as evaluation results may vary depending on the evaluation models, software versions, and execution settings.


**Note:** The `gold_qa_draft.csv` file in this directory is distinct from the file with the same name in `examples/qa_generation_2026-10-15/`, which was generated separately to verify the Q&A generation workflow on October 15, 2026.
