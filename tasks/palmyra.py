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
    description: str = "Generate medical responses using specialized LLM"
    dependencies: List[str] = []
    inputs: List[str] = [
        "Medical query with summative literature search results, CT findings and user query"
    ]
    outputs: List[str] = [
        "Model response with output format include in-text citation as [1], [2] and references title "
        + """Output Format:
      In the case of the provided CT images, the analysis from merlin_task suggests a high probability of [Insert phenotype] in the [Insert context, e.g., lung or brain] region, consistent with previous studies on [Insert related condition]. Literature indicates that this feature is present in [X%] of cases presenting with [Insert related symptoms or imaging patterns], as shown in a recent study by [Author(s)] [1].
      Additionally, recent advancements in [Insert aspect, e.g., early diagnosis of pulmonary infections] have demonstrated improved patient outcomes, as supported by a systematic review published in [Year] [2]. Evidence from [Author(s)] reinforces these findings, with a focus on [Insert specific intervention or treatment] [3].

      References:
      1. [Author Name(s)], "[Title of Study]," [Year], [Publication Link].
      2. [Author Name(s)], "[Title of Study]," [Year], [Publication Link].
      3. [Author Name(s)], "[Title of Study]," [Year], [Publication Link]."""
    ]
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
            temperature=0.0,
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
