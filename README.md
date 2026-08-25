# PRISM

**PRISM: A Local Retrieval-Augmented Generation System for Biomedical Research**

PRISM is a locally operated retrieval-augmented generation (RAG) system designed to support the use of domain-specific biomedical knowledge with large language models (LLMs).

The system integrates **LM Studio** for local LLM inference with **Dify** for knowledge-base management and RAG workflow construction. This repository provides the configuration details, procedures, and resources required to reproduce the PRISM system described in our manuscript.

> **Privacy and security notice:**  
> PRISM is designed to enable local processing of user-provided documents and prompts. However, local processing alone does not guarantee complete privacy or security. LM Studio, Dify, operating systems, model repositories, and other software components may initiate network communications depending on their configuration and version. Users handling sensitive or patient-related information should independently assess network behavior, software configuration, access controls, and applicable institutional security requirements.

## Overview

PRISM consists of the following main components:

1. **Local LLM inference** using LM Studio
2. **Retrieval-augmented generation** using Dify
3. **A local knowledge base** containing domain-specific biomedical documents
4. **Vector-based document retrieval**
5. **Prompt generation and response generation** using retrieved contextual information

The system was developed to investigate whether a locally operated RAG workflow can improve the accuracy of LLM responses to domain-specific biomedical questions while reducing dependence on cloud-based LLM services.

## Repository Contents

This repository contains the materials used to reproduce the evaluation reported in the associated manuscript.

- [`QUESTIONS.md`](QUESTIONS.md)  
  The 30 questions used in the evaluation.

- [`evaluation_dataset.csv`](evaluation_dataset.csv)  
  The evaluation dataset containing the questions, reference answers, and generated responses used in the study.

- [`evaluation_results.csv`](evaluation_results.csv)  
  The evaluation results used to derive the reported performance metrics.

- [`evaluation.ipynb`](evaluation.ipynb)  
  The Jupyter Notebook used to perform the evaluation and calculate the reported metrics.

## System Architecture

The basic workflow is:

```text
Biomedical documents
        ↓
Document preprocessing
        ↓
Dify Knowledge Base
        ↓
Vectorization / Retrieval
        ↓
Relevant document chunks
        ↓
Prompt + Retrieved Context
        ↓
LM Studio
        ↓
Local LLM
        ↓
Generated Response
```

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

> **Version used in this study:** The experiments reported in the manuscript were conducted using LM Studio version X.X.X.

### System requirements

For macOS, LM Studio supports Apple Silicon Macs. Please refer to the official LM Studio documentation for the latest system requirements:

**https://lmstudio.ai/docs/app/system-requirements**

## Reproducing the Evaluation

The evaluation reported in the manuscript can be reproduced using the materials provided in this repository.

1. Obtain the evaluation questions and reference answers from `data/`.
2. Obtain the RAG and non-RAG responses from `data/generated_responses.csv`.
3. Run the evaluation scripts provided in `evaluation/`.
4. Compare the resulting metrics with the values reported in the manuscript.

Detailed instructions and required Python dependencies are provided in the `evaluation/` directory.

## Data and Resources

The evaluation dataset used in this study is provided in the `data/` directory.

The publicly released materials include:

- evaluation questions;
- reference answers;
- responses generated under the RAG condition;
- responses generated under the non-RAG condition; and
- the data required to reproduce the reported evaluation results.

The evaluation code is provided in the `evaluation/` directory.

## Privacy and Security Considerations

PRISM performs LLM inference and RAG processing locally when configured as described in the manuscript. This architecture can reduce the need to transmit biomedical content to externally hosted LLM APIs.

However, local execution should not be interpreted as an absolute guarantee of privacy or security.

Users should consider, among other factors:

outbound network connections initiated by software components;
software update and telemetry mechanisms;
vulnerabilities introduced by dependencies or future software versions;
operating-system and network configuration;
access control and authentication;
logging and temporary files; and
institutional requirements for handling sensitive or patient-related information.

The authors do not claim that PRISM eliminates all possible routes of data leakage. Deployment with sensitive information should therefore be accompanied by an independent security assessment appropriate to the intended environment.

## Citation

Citation information will be added upon publication of the associated manuscript.

## License

License information for the materials developed by the authors will be provided separately. Third-party software, models, and datasets remain subject to their respective licenses.
