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
    outputs: List[str] = [
        "List of PubMed IDs (PMIDs) for relevant papers",
        "List of paper titles",
        "List of publication years",
        "List of paper full text content",
    ]
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

        pmids = [str(id) for id in data["esearchresult"]["idlist"]]

        # Fetch additional metadata and content for the papers
        paper_titles = []
        publication_years = []
        paper_contents = []
        for pmid in pmids:
            meta_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
            meta_response = requests.get(meta_url)
            meta_data = meta_response.json()
            paper_titles.append(meta_data["result"][pmid]["title"])
            publication_years.append(meta_data["result"][pmid]["pubdate"][:4])

            # Fetch full text content
            content_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=text&rettype=abstract"
            content_response = requests.get(content_url)
            paper_contents.append(content_response.text)

        return {
            "pmids": pmids,
            "titles": paper_titles,
            "years": publication_years,
            "contents": paper_contents,
        }

    def _post_execute(self, result: Dict[str, List[Any]]) -> str:
        return super()._post_execute(json.dumps(result))

    def explain(self) -> str:
        explanation = """
        The PubMedSearchTask is used to search for scientific papers on PubMed based on a given query. It allows you to filter the search results by publication date range, and it returns a comprehensive set of metadata for the relevant papers, including:

        1. List of PubMed IDs (PMIDs) for the papers
        2. List of paper titles
        3. List of publication years
        4. List of paper content

        To use this task, you'll need to provide the following inputs:

        1. Search query (required): The text query to search for on PubMed.

        The task will then use the NCBI Entrez API to search PubMed and fetch the relevant metadata and content for the papers. The results are returned as a dictionary, with each key containing a list of the corresponding data (e.g., the "pmids" key contains a list of PubMed IDs).

        This task can be useful for quickly gathering a comprehensive set of information about papers related to a particular topic, which can then be further analyzed or used in other parts of your application or research workflow.
        """
        return explanation
