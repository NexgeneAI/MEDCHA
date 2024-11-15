# MEDCHA
Multi Modal Evidence-Driven Conversational Healthcare Agent

## Installation and Setup

1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set the required API keys by creating `.env` file (see `.env.example`)

## Run with Interface
To start the Gradio application, run:
```bash
python main.py
```

## Acknowdledgements
* [openCHA](https://github.com/Institute4FutureHealth/CHA): Open Conversational Health Agents Framework
* [PubMed API](https://pubmed.ncbi.nlm.nih.gov): Medical Literature Search
* [MedlinePlus API](https://medlineplus.gov): Governmental Health Information Resource
* [Merlin](https://arxiv.org/abs/2406.06512): A Vision Language Foundation Model for 3D Computed Tomography
* [Palmyra-Med-70b](https://dev.writer.com): A powerful LLM designed for healthcare
* [obi/deid_roberta_i2b2](https://huggingface.co/obi/deid_roberta_i2b2): A pretrained NER model for masking PII/PHI
* [Nvidia NIM](https://build.nvidia.com/explore/discover): Optimized LLM deployment and inference
