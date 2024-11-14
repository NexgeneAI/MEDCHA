from typing import Dict
from typing import Type

from openCHA.tasks import BaseTask
from openCHA.tasks import GoogleTranslate
from openCHA.tasks import TaskType

from tasks.pubmed import PubMedSearch
from tasks.palmyra import MedicalLLM
from tasks.merlin import MerlinTask
from tasks.deid import DeidentificationTask

TASK_TO_CLASS: Dict[TaskType, Type[BaseTask]] = {
    TaskType.GOOGLE_TRANSLATE: GoogleTranslate,
    TaskType.PUBMED_SEARCH: PubMedSearch,
    TaskType.MEDICAL_LLM: MedicalLLM,
    TaskType.MERLIN_TASK: MerlinTask,
    TaskType.DEID_TASK: DeidentificationTask,
}
