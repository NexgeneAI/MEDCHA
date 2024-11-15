from enum import Enum


class TaskType(str, Enum):
    GOOGLE_TRANSLATE = "google_translate"
    PUBMED_SEARCH = "pubmed_search"
    MEDLINE_SEARCH = "medline_search"
    MEDICAL_LLM = "medical_llm"
    MERLIN_TASK = "merlin_task"
    DEID_TASK = "deid_task"
