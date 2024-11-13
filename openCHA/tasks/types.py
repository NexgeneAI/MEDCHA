from typing import Dict
from typing import Type

from openCHA.tasks import AskUser
from openCHA.tasks import BaseTask
from openCHA.tasks import ExtractText
from openCHA.tasks import GoogleSearch
from openCHA.tasks import GoogleTranslate
from openCHA.tasks import RunPythonCode
from openCHA.tasks import SerpAPI
from openCHA.tasks import TaskType
from openCHA.tasks import TestFile
from openCHA.tasks.affect import ActivityAnalysis
from openCHA.tasks.affect import ActivityGet
from openCHA.tasks.affect import PPGAnalysis
from openCHA.tasks.affect import PPGGet
from openCHA.tasks.affect import SleepAnalysis
from openCHA.tasks.affect import SleepGet
from openCHA.tasks.affect import StressAnalysis
from openCHA.tasks.nutritionix import (
    CalculateFoodRiskFactor,
)
from openCHA.tasks.nutritionix import QueryNutritionix

from tasks.pubmed import PubMedSearch
from tasks.palmyra import MedicalLLM
from tasks.merlin import MerlinTask

TASK_TO_CLASS: Dict[TaskType, Type[BaseTask]] = {
    TaskType.GOOGLE_TRANSLATE: GoogleTranslate,
    TaskType.PUBMED_SEARCH: PubMedSearch,
    TaskType.MEDICAL_LLM: MedicalLLM,
    TaskType.MERLIN_TASK: MerlinTask,
}
