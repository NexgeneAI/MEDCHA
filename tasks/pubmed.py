from __future__ import annotations

from typing import List
from typing import Any
from typing import Dict

import json
import requests
from openCHA.tasks.task import BaseTask


class PubMedSearch(BaseTask):
    name: str = "pubmed_search"
    chat_name: str = "PubMedSearch"
    description: str = (
        "Search PubMed for scientific papers based on a given query. Allows filtering by publication date range and returning paper abstracts and full text content."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["Search query as keyword or phrase"]
    outputs: List[str] = ["List of related PubMed papers"]
    output_type: bool = False

    def _execute(self, inputs: List[Any]) -> Dict[str, List[Any]]:
        query = inputs[0]

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 5,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        paper_contents = []
        pmids = [str(id) for id in data["esearchresult"]["idlist"]]
        for pmid in pmids:
            content_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=text&rettype=abstract"
            content_response = requests.get(content_url)
            paper_contents.append(content_response.text)

        return paper_contents

    def explain(self) -> str:
        return """
        Searches PubMed papers for gathering recent medical literature:
        1. Retrieves detailed paper information
        2. Includes titles, abstracts, authors, dates
        
        Example query: "CRISPR cancer therapy 2024"
        """
