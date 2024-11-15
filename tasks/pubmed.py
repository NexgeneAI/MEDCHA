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
    output_type: bool = True

    def _execute(self, inputs: List[Any]) -> Dict[str, List[Any]]:
        query = inputs[0]

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 50,  # Increase result limit to 50
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
        explanation = """
        The PubMedSearchTask is used to search for scientific papers on PubMed based on a given query. It allows you to filter the search results by publication date range, and it returns a comprehensive set of metadata for the relevant papers, including:

        1. List of related PubMed papers

        To use this task, you'll need to provide the following inputs:

        1. Search query (required): The text query to search for on PubMed.

        The task will then use the NCBI Entrez API to search PubMed and fetch the relevant metadata and content for the papers. The results are returned as a dictionary, with each key containing a list of the corresponding data (e.g., the "pmids" key contains a list of PubMed IDs).

        This task can be useful for quickly gathering a comprehensive set of information about papers related to a particular topic, which can then be further analyzed or used in other parts of your application or research workflow.
        """
        return explanation
