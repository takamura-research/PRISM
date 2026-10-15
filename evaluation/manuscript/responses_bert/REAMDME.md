## Manuscript Evaluation Results

The following CSV files contain the BERTScore (F1), ROUGE-L, and BLEU evaluation results reported in the PRISM manuscript.

- `RAG_conversation_QA_evaluation_results.csv`: Evaluation results for the local Gemma 3 model with RAG.
- `nRG_conversation_QA_evaluation_results.csv`: Evaluation results for the local Gemma 3 model without RAG.

Each file contains 90 evaluation records corresponding to 30 questions evaluated against three cloud-generated reference answers per question.

The files include the original questions, reference answers, local LLM-generated answers, and question-level evaluation scores. The reported manuscript values correspond to the mean scores across the 90 records.

These files represent the original evaluation results used in the manuscript and should be distinguished from the example datasets provided for demonstrating the evaluation workflow.


## Evaluation Summary

The CSV files generated using `PRISM_RAG_vs_NonRAG_Mean_Comparison_Content_Select.ipynb` are stored in the `manuscript/responses_bert/` directory.

- `PRISM_RAG_vs_NonRAG_column_means.csv`: Mean values of the numerical evaluation metrics for the RAG and non-RAG configurations, including their differences and percentage changes.
- `PRISM_RAG_vs_NonRAG_compact_comparison.csv`: A simplified comparison of the mean evaluation scores and their differences between the two configurations.

These summary files were calculated from the original question-level evaluation results and provide the aggregated values used to compare the RAG and non-RAG configurations in the PRISM manuscript.
