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



Detailed configuration information will be provided in this repository.

## Requirements

The PRISM implementation described in the manuscript uses:

- LM Studio
- Dify
- A locally executable large language model
- A local computer capable of running the selected model

Hardware specifications, software versions, model information, and RAG parameters used in the study are provided in the sections below.

## Installation

Detailed installation instructions will be provided for:

### 1. LM Studio

Instructions will describe:

- LM Studio installation
- Model installation
- Local inference configuration
- Local API server configuration

### 2. Dify

Instructions will describe:

- Dify installation
- Knowledge-base creation
- Connection to the local LLM
- Retrieval configuration
- RAG workflow configuration

## RAG Configuration

The following parameters used in the manuscript will be documented:

- Embedding model
- Vector database / retrieval backend
- Chunking strategy
- Retrieval method
- Top-k
- Prompt configuration
- LLM model and inference parameters

## Reproducing the Evaluation

This repository will provide the materials and procedures necessary to reproduce the evaluation described in the manuscript, subject to applicable data-sharing and licensing restrictions.

The evaluation compares:

- RAG-enabled generation
- Generation without RAG

using the same locally operated LLM.

## Data and Resources

Publicly shareable materials required to reproduce the reported analyses will be provided through this repository or an appropriate public research-data repository.

Any materials that cannot legally or ethically be redistributed will be clearly identified, together with instructions for obtaining the original resources where applicable.

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
