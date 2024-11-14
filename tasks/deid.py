from __future__ import annotations

from typing import List, Optional, Any, Dict
from openCHA.tasks.task import BaseTask
from pydantic import model_validator
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import os
import warnings

warnings.filterwarnings("ignore")


class DeidentificationTask(BaseTask):
    name: str = "deid_task"
    chat_name: str = "MedicalTextDeidentification"
    description: str = (
        "De-identify medical text by masking sensitive entities using a pre-trained RoBERTa model."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["Medical text containing sensitive information"]
    outputs: List[str] = ["De-identified text with sensitive entities masked"]
    output_type: bool = False

    model: Any = None
    tokenizer: Any = None
    ner_pipeline: Any = None

    @model_validator(mode="before")
    def validate_model(cls, values: Dict) -> Dict:
        """
        Initialize and validate the de-identification model environment.
        """
        try:
            # Load the tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained("obi/deid_roberta_i2b2")
            model = AutoModelForTokenClassification.from_pretrained(
                "obi/deid_roberta_i2b2"
            )

            # Initialize the NER pipeline
            ner_pipeline = pipeline(
                "ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple"
            )

            values["tokenizer"] = tokenizer
            values["model"] = model
            values["ner_pipeline"] = ner_pipeline

        except Exception as e:
            raise ValueError(f"Failed to initialize model and tokenizer: {str(e)}")

        return values

    def _execute(self, inputs: List[Any]) -> str:
        """
        Process the input text and return de-identified version.

        Args:
            inputs: List containing a single string of medical text

        Returns:
            De-identified version of the input text
        """
        if not inputs or not isinstance(inputs[0], str):
            raise ValueError("Input must be a non-empty string of medical text")

        text = inputs[0]

        # Run the NER pipeline on the input text
        entities = self.ner_pipeline(text)

        # Make a copy of the original text for masking
        deidentified_text = text

        # Mask each entity with its entity label
        for entity in entities:
            entity_text = text[entity["start"] : entity["end"]]
            entity_label = f"[{entity['entity_group']}]"

            # Replace the entity text with its label in the de-identified text
            deidentified_text = deidentified_text.replace(entity_text, entity_label)

        return deidentified_text

    def explain(self) -> str:
        explanation = """
        The DeidentificationTask processes medical text to remove or mask sensitive information
        using a pre-trained RoBERTa model specifically fine-tuned for medical text de-identification.

        The task:
        1. Takes a string of medical text as input
        2. Identifies sensitive entities (names, dates, locations, etc.)
        3. Replaces these entities with generic labels indicating their type
        4. Returns the de-identified text

        The model is trained on the i2b2 dataset and can identify various types of protected health
        information (PHI) including:
        - Names (patient, doctor, etc.)
        - Dates
        - Locations (hospitals, cities, etc.)
        - Contact information
        - IDs and other identifiers
        """
        return explanation
