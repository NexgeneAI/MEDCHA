from __future__ import annotations
from typing import List, Any, Dict
from openCHA.tasks.task import BaseTask
from pydantic import model_validator
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import warnings

warnings.filterwarnings("ignore")

class DeidentificationTask(BaseTask):
    """Medical text de-identification using RoBERTa model."""
    
    name: str = "deid_task"
    chat_name: str = "MedicalTextDeidentification"
    description: str = "Mask sensitive information in medical text"
    dependencies: List[str] = []
    inputs: List[str] = ["Medical text"]
    outputs: List[str] = ["De-identified text"]
    output_type: bool = False

    model: Any = None
    tokenizer: Any = None
    ner_pipeline: Any = None

    @model_validator(mode="before")
    def validate_model(cls, values: Dict) -> Dict:
        """Initialize de-identification model."""
        try:
            model_name = "obi/deid_roberta_i2b2"
            values.update({
                "tokenizer": AutoTokenizer.from_pretrained(model_name),
                "model": AutoModelForTokenClassification.from_pretrained(model_name),
            })
            values["ner_pipeline"] = pipeline(
                "ner", 
                model=values["model"], 
                tokenizer=values["tokenizer"], 
                aggregation_strategy="simple"
            )
            return values
        except Exception as e:
            raise ValueError(f"Model initialization failed: {str(e)}")

    def _execute(self, inputs: List[Any]) -> str:
        """De-identify medical text.
        
        Args:
            inputs: List with medical text string
        Returns:
            De-identified text with masked entities
        """
        if not inputs or not isinstance(inputs[0], str):
            raise ValueError("Input must be non-empty medical text")

        text = inputs[0]
        entities = self.ner_pipeline(text)
        result = text

        for entity in entities:
            entity_text = text[entity["start"]:entity["end"]]
            result = result.replace(entity_text, f"[{entity['entity_group']}]")

        return result

    def explain(self) -> str:
        return """
        De-identifies medical text by:
        1. Detecting sensitive entities (names, dates, locations)
        2. Replacing them with type labels (e.g., [NAME], [DATE])
        3. Preserving medical content while removing PHI
        
        Uses RoBERTa model trained on i2b2 dataset to identify:
        - Personal names
        - Dates
        - Locations
        - Contact info
        - Medical IDs
        """