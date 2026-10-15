# PRISM

**PRISM: A Local Retrieval-Augmented Generation System for Biomedical Research**

PRISM is a locally operated retrieval-augmented generation (RAG) system designed to support the use of domain-specific biomedical knowledge with large language models (LLMs).

This repository provides the essential configurations, implementation procedures, and resources to support the reproduction of a minimal functional configuration of the PRISM system described in our manuscript.

> **Privacy and security notice:**
> PRISM was configured to perform LLM inference and document processing locally in the study described in the manuscript. However, local execution does not guarantee complete privacy or security. Software components, including LM Studio and the underlying operating system, may initiate network communications depending on their configuration and version. Users handling sensitive or patient-related information should independently assess network behavior, software configuration, access controls, and applicable institutional security requirements.


## Overview

The PRISM system presented in this repository primarily consists of the following components:

1. **Local LLM inference** using LM Studio.
2. **Domain-specific biomedical documents** serving as the knowledge source for retrieval-augmented generation (RAG).

PRISM was constructed to investigate whether a locally operated RAG workflow can improve the accuracy of LLM-generated responses to domain-specific biomedical questions while reducing dependence on cloud-based LLM services.


## System Architecture
For reproducibility, this repository presents a minimal configuration of PRISM using LM Studio.

The basic workflow is:

```text
HAES Research Paper (PDF)
          ↓
LM Studio Chat
          ↓
Local LLM
          ↓
Question Input
          ↓
Generated Response
```

The HAES research paper is uploaded directly to the LM Studio chat interface, where the local LLM generates responses to user-provided questions based on the document.


## LM Studio Installation

PRISM uses **LM Studio** to run the large language model locally. LM Studio can be installed either using the graphical installer or Homebrew on macOS.

### Option 1: Graphical installation

1. Visit the official LM Studio download page:

   **LM Studio:** https://lmstudio.ai/download

2. Download the macOS version of LM Studio.

3. Open the downloaded installer and install LM Studio.

4. Launch LM Studio from the Applications folder.

### Option 2: Installation using Homebrew

If Homebrew is installed, LM Studio can be installed from Terminal using:

```bash
brew install --cask lm-studio
```

After installation, launch LM Studio from the Applications folder.

To verify the installation through Homebrew, run:

```bash
brew list --cask | grep lm-studio
```

> **Version used in this study:** LM Studio version: PRISM was implemented using the LM Studio 0.3.x series. Because the application may have been updated during the study, the exact version used for each experimental run cannot be retrospectively determined.

### System requirements

For macOS, LM Studio supports Apple Silicon Macs. Please refer to the official LM Studio documentation for the latest system requirements:

**https://lmstudio.ai/docs/app/system-requirements**

### 2. Set Up the Local LLM

PRISM uses Gemma 3 12B as the local large language model.

In LM Studio, search for and download the following model:

`lmstudio-community/gemma-3-12b-it-GGUF`

> **Model used in this study:** `lmstudio-community/gemma-3-12b-it-GGUF`
> The PRISM system was evaluated using Gemma 3 12B as the local large language model. To reproduce the experimental conditions reported in the manuscript, Gemma 3 12B should be used. However, users may select alternative models, such as Gemma 4, for other applications or exploratory purposes.


## Knowledge Base Source Documents
The following document was used as a source document in the PRISM
knowledge base and for the evaluation reported in the manuscript.


### KB01: Evaluation Source Document
**File:** [KB01_Umezawa_2025.pdf](KB01_Umezawa_2025.pdf)

Umezawa A, et al. First-in-human clinical study of an embryonic stem cell product for urea cycle disorders. *Stem Cell Research & Therapy*. 2025;16:120.

DOI: https://doi.org/10.1186/s13287-025-04162-3

License: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

The original PDF is provided for reproducibility of the PRISM evaluation. Only the filename has been changed; the document content remains unmodified. Copyright © The Author(s) 2025.


## Evaluation Q&A Generation
The `PRISM_QA_Generation_Colab.ipynb` notebook provided in this repository enables users to generate evaluation question–answer (Q&A) pairs from source research papers using Ragas. The notebook has been tested in Google Colab. The `QUESTIONS.md` and `ANSWERS.md` files contain the 30 evaluation questions and their corresponding reference answers, respectively, that were used to calculate the evaluation metrics reported in the manuscript. Due to the stochastic nature of LLM-based generation, newly generated Q&A pairs may differ from those used in the manuscript.


### LM Studio Conversation Export
The PRISM_LMStudio_JSON_to_CSV.ipynb notebook converts LM Studio conversation history exported in JSON format into a structured CSV file with three columns: No, Question, and Answer.

The notebook has been successfully tested using an LM Studio conversation JSON file, confirming that the generated responses can be extracted and converted into the specified CSV format.

Example input and output files are provided in the evaluation/examples/ directory for demonstration and reproducibility purposes. These example files are not the original evaluation results reported in the manuscript.


## Q&A Datasets
This repository provides two types of Q&A datasets for different purposes.

### Q&A Dataset Used in the Manuscript
- [`QUESTIONS.md`](QUESTIONS.md): The 30 questions used to evaluate PRISM in the manuscript.
- [`ANSWERS.md`](ANSWERS.md): The corresponding reference answers used in the evaluation.

These files document the Q&A dataset used to calculate the evaluation results reported in the PRISM manuscript.

### Example Outputs from Q&A Generation
- [`gold_qa_draft.csv`](examples/qa_generation_2026-10-15/gold_qa_draft.csv): Example Q&A pairs generated by the notebook.
- [`gold_qa_evidence_audit.csv`](examples/qa_generation_2026-10-15/gold_qa_evidence_audit.csv): Example Q&A pairs with supporting evidence and review information.

These CSV files were generated on October 15, 2026, during an execution test of `PRISM_QA_Generation_Colab.ipynb` in Google Colab.

**Important:** These example CSV files are not the Q&A dataset used in the PRISM manuscript and were not used to calculate the reported evaluation results. They are provided solely to demonstrate the Q&A generation workflow and output format.


## BERTScore Evaluation
The `PRISM_BERTScore_Evaluation_Colab.ipynb` notebook provides a Google Colab-compatible workflow for evaluating the responses generated by PRISM using BERTScore (Precision, Recall, and F1), ROUGE-L (F1), and BLEU.

The notebook accepts CSV files containing candidate responses from the RAG and non-RAG configurations, together with reference answers generated by cloud-based LLMs (ChatGPT, Claude, and Gemini) or other reference-answer datasets.

The input CSV files are available in [`evaluation/bertscore/`](evaluation/bertscore/).

Users can upload the CSV files to Google Colab, select the candidate and reference datasets, and calculate the evaluation metrics. The notebook exports both question-level results and summary statistics as CSV files.

**Note:** Reproducing the exact numerical results reported in the manuscript requires using the same evaluation settings, model versions, and reference-answer datasets as those used in the original evaluation.


## Ragas-Based Evaluation

The [`PRISM_Ragas_5Metrics_Evaluation_Colab.ipynb`](evaluation/PRISM_Ragas_5Metrics_Evaluation_Colab.ipynb) notebook provides an evaluation workflow using Ragas to compare RAG and non-RAG responses.

The notebook supports five evaluation metrics: Answer Correctness, Answer Relevancy, Faithfulness, Context Precision, and Context Recall. It uses the source research paper and reference answers to evaluate response quality.

The notebook is designed to run in Google Colab and exports the evaluation results as CSV files.

The input datasets used for the five-metric evaluation are provided in the [`evaluation/ragas_5metrics/`](evaluation/ragas_5metrics/) directory, including RAG-generated answers, non-RAG-generated answers, and reference answers. The source research paper is also available in this repository.

Re-evaluation using the provided notebook produced results broadly consistent with those reported in the manuscript. Detailed information on the datasets and evaluation procedure is provided in the corresponding directory.

**Note:** Context Precision and Context Recall are calculated using evaluation-specific retrieved evidence and should not be interpreted as direct measurements of PRISM's retrieval performance.


## Automated Evaluation with LM Studio

In addition to the Google Colab notebooks, PRISM provides a Python-based automated evaluation pipeline (`pipeline_structured.py`) for local large language models (LLMs) running in LM Studio.

This pipeline is implemented as an additional functionality of the PRISM framework to automate the evaluation of local LLM responses. By running the script in a separate terminal, users can interact with local LLMs through the standard LM Studio GUI while the pipeline monitors conversations and evaluates eligible responses without modifying the interface or inference workflow.

### Evaluation Workflow

The pipeline monitors LM Studio conversation files and detects newly completed responses. When a source research paper (PDF) is provided and the local LLM generates a structured Q&A table, the pipeline automatically performs the following operations:

1. **Conversation extraction:** Extracts questions, local LLM responses, and relevant conversation history from LM Studio.
2. **Reference answer generation:** Submits the conversation history and source PDF to configured cloud-based LLMs (ChatGPT, Claude, and Gemini) to generate reference responses.
3. **BERTScore evaluation:** Calculates BERTScore (F1) between local LLM answers and their corresponding cloud-generated reference answers.
4. **Optional Ragas evaluation:** Calculates Answer Relevancy and Answer Correctness, and additionally evaluates Faithfulness when retrieved contexts are available.
5. **Result export:** Saves model responses, evaluation metrics, and processing information to a CSV file.

BERTScore is calculated using only the answer fields, with questions aligned by their corresponding identifiers.

### Execution

Start the evaluation pipeline in a terminal:

```bash
python3 pipeline_structured.py
```

To enable additional Ragas evaluation:

```bash
python3 pipeline_structured.py --ragas
```

Keep the terminal process running while interacting with the local LLM through the LM Studio GUI. The pipeline automatically detects and evaluates eligible responses generated after monitoring begins.

By default, existing conversations are not evaluated at startup. The `--process-existing` option can be used to include existing conversation files.

### Requirements

- Python 3.10 or later
- LM Studio with a configured local LLM
- Required Python dependencies
- API keys for the cloud-based LLM providers being used
- A locally cached BERTScore model
- A source research paper in PDF format
- Local LLM responses formatted as numbered Markdown tables with `No`, `Question`, and `Answer` columns

The default BERTScore configuration uses `bert-base-multilingual-cased` with nine layers. The model must be available locally because the pipeline enables Hugging Face offline mode during BERTScore evaluation.

### Output

Evaluation results are saved to `results/evaluation.csv` by default.

The output includes:

- Local LLM responses and cloud-generated reference responses
- BERTScore (F1) for each available cloud reference model and their mean
- Optional Ragas evaluation metrics
- Evaluated question counts and conversation metadata
- Processing status and error information

### Limitations and Considerations

The pipeline is designed for structured, document-based Q&A evaluation rather than unrestricted conversational assessment.

- **Input requirements:** Evaluation requires an accessible source PDF and a correctly formatted Q&A table.
- **Reference availability:** Cloud-based evaluation depends on configured API keys and successful API responses.
- **BERTScore dependencies:** The specified BERTScore model must be cached locally before evaluation.
- **Ragas evaluation:** Ragas metrics are optional and require additional API calls. Faithfulness is calculated only when retrieved contexts are available.
- **Conversation monitoring:** The pipeline processes eligible completed responses detected through conversation file updates and does not guarantee independent evaluation of every historical conversation turn.
- **API costs:** Cloud-based reference generation and optional Ragas evaluation may incur API usage charges.
- **Evaluation reproducibility:** Numerical results depend on the local and cloud LLMs, reference responses, model configurations, and evaluation settings.

### Privacy Considerations and Future Development

The current implementation relies on external LLM APIs (OpenAI, Anthropic, and Google) for reference answer generation. Consequently, source documents and conversation histories are transmitted to external service providers when the corresponding APIs are used. Optional Ragas evaluation also involves external API calls.

Therefore, although the response generation process can be performed locally, **the current evaluation pipeline does not provide a fully local, privacy-preserving environment**. It should not be used with confidential or sensitive information unless external data transmission is explicitly permitted and appropriate data protection measures are in place.

The primary objective of this implementation is to demonstrate **the feasibility of automating the evaluation process as an additional functionality of PRISM**, rather than to establish a fully privacy-preserving evaluation system.

Future development will focus on integrating a dedicated local LLM-based evaluation system to replace external API-dependent reference generation and evaluation. This approach is intended to enable both response generation and evaluation to be performed entirely within a local computing environment, without transmitting evaluation data to external LLM providers.

The present implementation therefore serves as an initial step toward incorporating automated evaluation capabilities into the PRISM framework while identifying the requirements for a fully local, privacy-preserving evaluation architecture.

**Note:** This pipeline is provided as an additional evaluation utility for PRISM and is not intended to reproduce the exact evaluation results reported in the manuscript.


## Privacy and Security Considerations
PRISM was configured to perform LLM inference and RAG processing locally in the study described in the manuscript. This approach can reduce the need to transmit biomedical content to externally hosted LLM APIs.

However, local execution should not be interpreted as an absolute guarantee of privacy or security.

Users should consider, among other factors:

- Outbound network connections initiated by software components;
- Software update and telemetry mechanisms;
- Vulnerabilities introduced by dependencies or future software versions;
- Operating-system and network configuration;
- Access control and authentication;
- Logging and temporary files; and
- Institutional requirements for handling sensitive or patient-related information.

The authors do not claim that PRISM eliminates all possible routes of data leakage. Deployment with sensitive information should therefore be accompanied by an independent security assessment appropriate to the intended environment.


## Citation
Citation information will be added upon publication of the associated manuscript.


## License
License information for the materials developed by the authors will be provided separately. Third-party software, models, and datasets remain subject to their respective licenses.
