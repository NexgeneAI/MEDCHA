from __future__ import annotations

from typing import List, Any, Dict, Optional
import re
import json
import requests
from openCHA.tasks.task import BaseTask
import xml.etree.ElementTree as ET


class MedlinePlusSearch(BaseTask):
    name: str = "medlineplus_search"
    chat_name: str = "MedlinePlusSearch"
    description: str = (
        "Search MedlinePlus for health topics based on a given query. Returns relevant health topics "
        "with titles, summaries, and associated metadata in XML format."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["Search query as keyword or phrase"]
    outputs: List[str] = ["List of all related data and sources"]
    output_type: bool = True

    session: Any = requests.Session()
    BASE_URL: str = "https://wsearch.nlm.nih.gov/ws/query"
    DEFAULT_RESULTS: int = 5

    def _build_params(
        self,
        query: str,
        file: Optional[str] = None,
        server: Optional[str] = None,
        start_index: int = 0,
    ) -> Dict[str, str]:
        """Build query parameters for the API request."""
        params = {
            "db": "healthTopics",
            "term": query,
            "retmax": str(self.DEFAULT_RESULTS),
            "rettype": "all",
        }

        if file and server:
            params.update(
                {"file": file, "server": server, "retstart": str(start_index)}
            )

        return params

    def strip_html_tags(self, text):
        return re.sub(r"<[^>]+>", "", text)

    def _execute(self, inputs: List[Any]) -> Dict[str, Any]:
        query = inputs[0]

        params = self._build_params(query=query)
        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()

        # Parse XML response
        data = response.text
        root = ET.fromstring(data)

        documents_data = []

        # Iterate through all <document> elements
        for document in root.findall(".//document"):
            # Extract the title
            title = document.find(".//content[@name='title']")
            # Extract the URL (from document attribute)
            url = document.get("url")
            # Extract alternative titles
            alt_titles = document.findall(".//content[@name='altTitle']")
            # Extract the FullSummary
            full_summary = document.find(".//content[@name='FullSummary']")
            # Extract healthTopic section
            health_topic = document.find(".//content[@name='healthTopic']/health-topic")

            # Process data into a dictionary
            data = {
                "title": self.strip_html_tags(title.text) if title is not None else "",
                "url": url,
                "altTitle": [
                    self.strip_html_tags(alt_title.text) for alt_title in alt_titles
                ],
                "FullSummary": (
                    self.strip_html_tags(full_summary.text)
                    if full_summary is not None
                    else ""
                ),
                "healthTopic": {
                    "meta-desc": (
                        self.strip_html_tags(health_topic.get("meta-desc"))
                        if health_topic is not None
                        else ""
                    ),
                    "title": (
                        self.strip_html_tags(health_topic.get("title"))
                        if health_topic is not None
                        else ""
                    ),
                    "url": health_topic.get("url") if health_topic is not None else "",
                    "id": health_topic.get("id") if health_topic is not None else "",
                    "language": (
                        health_topic.get("language") if health_topic is not None else ""
                    ),
                    "date-created": (
                        health_topic.get("date-created")
                        if health_topic is not None
                        else ""
                    ),
                    "also-called": [
                        self.strip_html_tags(also_called.text)
                        for also_called in health_topic.findall("also-called")
                    ],
                },
            }
            # Append the document data to the list
            documents_data.append(data)

        return json.dumps(documents_data, indent=4)

    def explain(self) -> str:
        explanation = """
        The MedlinePlusSearch task allows you to search for health topics on MedlinePlus using their Web Service API.
        
        Key Features:
        - Returns full health topic records including titles, summaries, and metadata
        - Returns both brief and detailed information for each topic
        - Returns up to 50 most relevant results
        
        Required Input:
        1. Search query: Text to search for
        
        Field Searching:
        You can limit searches to specific fields using the syntax field:value
        Available fields: title, alt-title, mesh, full-summary, group
        
        Example usage:
        inputs = ["diabetes"]  # Search for "diabetes"
        """
        return explanation
