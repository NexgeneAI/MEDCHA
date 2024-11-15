from __future__ import annotations
from typing import List, Any, Dict, Optional
import re
import json
import requests
from openCHA.tasks.task import BaseTask
import xml.etree.ElementTree as ET


class MedlinePlusSearch(BaseTask):
    """Search MedlinePlus for health topics and metadata."""

    name: str = "medline_search"
    chat_name: str = "MedlineSearch"
    description: str = "Search MedlinePlus health topics with metadata"
    dependencies: List[str] = []
    inputs: List[str] = ["Search query"]
    outputs: List[str] = ["Health topics data"]
    output_type: bool = False

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
        """Build API request parameters."""
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

    @staticmethod
    def strip_html_tags(text: str) -> str:
        """Remove HTML tags from text."""
        return re.sub(r"<[^>]+>", "", text) if text else ""

    def _extract_health_topic_data(self, health_topic: Optional[ET.Element]) -> Dict:
        """Extract health topic metadata."""
        if not health_topic:
            return {
                k: ""
                for k in [
                    "meta-desc",
                    "title",
                    "url",
                    "id",
                    "language",
                    "date-created",
                    "also-called",
                ]
            }

        return {
            "meta-desc": self.strip_html_tags(health_topic.get("meta-desc")),
            "title": self.strip_html_tags(health_topic.get("title")),
            "url": health_topic.get("url"),
            "id": health_topic.get("id"),
            "language": health_topic.get("language"),
            "date-created": health_topic.get("date-created"),
            "also-called": [
                self.strip_html_tags(ac.text)
                for ac in health_topic.findall("also-called")
            ],
        }

    def _execute(self, inputs: List[Any]) -> str:
        """Search MedlinePlus and return formatted results.

        Args:
            inputs: List containing search query
        Returns:
            JSON string of health topics data
        """
        response = self.session.get(self.BASE_URL, params=self._build_params(inputs[0]))
        response.raise_for_status()

        root = ET.fromstring(response.text)
        documents_data = []

        for doc in root.findall(".//document"):
            data = {
                "title": self.strip_html_tags(
                    doc.find(".//content[@name='title']").text
                    if doc.find(".//content[@name='title']")
                    else ""
                ),
                "url": doc.get("url"),
                "altTitle": [
                    self.strip_html_tags(alt.text)
                    for alt in doc.findall(".//content[@name='altTitle']")
                ],
                "FullSummary": self.strip_html_tags(
                    doc.find(".//content[@name='FullSummary']").text
                    if doc.find(".//content[@name='FullSummary']")
                    else ""
                ),
                "healthTopic": self._extract_health_topic_data(
                    doc.find(".//content[@name='healthTopic']/health-topic")
                ),
            }
            documents_data.append(data)

        return json.dumps(documents_data, indent=4)

    def explain(self) -> str:
        return """
        Searches MedlinePlus health topics API:
        1. Accepts search query (e.g., "diabetes")
        2. Returns topic data: title, summary, metadata
        3. Supports field-specific search (title:value)
        
        Fields: title, alt-title, mesh, full-summary, group
        Results limited to top 50 matches.
        """
