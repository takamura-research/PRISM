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


### KB01
Umezawa A, et al. First-in-human clinical study of an embryonic
stem cell product for urea cycle disorders.
Stem Cell Research & Therapy. 2025;16:120.

DOI: 10.1186/s13287-025-04162-3

License: Creative Commons Attribution 4.0 International (CC BY 4.0)


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
