from __future__ import annotations

from typing import List, Optional
from typing import Any
from typing import Dict

from openCHA.tasks.task import BaseTask
from openCHA.utils import get_from_dict_or_env
from pydantic import model_validator


class MedicalLLM(BaseTask):
    name: str = "medical_llm"
    chat_name: str = "MedicalLLM"
    description: str = (
        "Generate medical responses using specialized LLM"
    )
    dependencies: List[str] = []
    inputs: List[str] = ["Medical query as a question or statement"]
    outputs: List[str] = ["Model response"]
    output_type: bool = False

    client: Any = None
    nvidia_api_key: Optional[str] = None

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict) -> Dict:
        """
            Validate that api key and python package exists in environment.

        Args:
            values (Dict): The dictionary of attribute values.
        Return:
            Dict: The updated dictionary of attribute values.
        Raise:
            ValueError: If the SerpAPI python package is not installed.

        """

        nvidia_api_key = get_from_dict_or_env(
            values, "nvidia_api_key", "NVIDIA_API_KEY"
        ).replace('"', "")

        try:
            from openai import OpenAI

            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1", api_key=nvidia_api_key
            )
            values["client"] = client
        except ImportError:
            raise ValueError(
                "Could not import serpapi python package. "
                "Please install it with `pip install google-search-results`."
            )
        return values

    def _execute(self, inputs: List[Any]) -> Dict[str, List[Any]]:
        query = inputs[0]

        completion = self.client.chat.completions.create(
            model="writer/palmyra-med-70b",
            messages=[{"role": "user", "content": query}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
        )

        return completion.choices[0].message.content

    def explain(self) -> str:
        return """
        Medical LLM using Palmyra-med-70b model:
        1. Processes medical queries and questions
        2. Generates responses based on LLM's medical knowledge
        3. Useful for initial research and information gathering
        
        Note: Results should be verified with authoritative sources.
        """
