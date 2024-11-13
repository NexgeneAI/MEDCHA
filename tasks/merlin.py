from __future__ import annotations

from typing import List, Optional, Any, Dict
from openCHA.tasks.task import BaseTask
from pydantic import model_validator
import os
import warnings
import torch
import pandas as pd
import merlin

warnings.filterwarnings("ignore")


class MerlinTask(BaseTask):
    name: str = "merlin_task"
    chat_name: str = "MerlinCTImageInference"
    description: str = (
        "Process a 3D CT image through the Merlin model and return phenotype probabilities."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["Path to a 3D CT image in NIfTI format"]
    outputs: List[str] = ["Formatted string of top phenotypes with probabilities"]

    model: Any = None
    device: str = None
    phecodes_df: pd.DataFrame = None

    @model_validator(mode="before")
    def validate_model(cls, values: Dict) -> Dict:
        """
        Initialize and validate the Merlin model environment.
        """
        # Load the Merlin model if not already loaded
        device = "cuda" if torch.cuda.is_available() else "cpu"
        values["device"] = device

        model = merlin.models.Merlin()
        model.eval()
        model.to(device)
        values["model"] = model

        # Ensure phenotype file is available
        phecodes_path = os.path.join("data", "phenotypes.csv")
        if not os.path.exists(phecodes_path):
            raise FileNotFoundError("Phenotypes file not found at expected path.")
        values["phecodes_df"] = pd.read_csv(phecodes_path)

        return values

    def _execute(self, inputs: List[Any]) -> str:
        image_path = inputs[0]

        # Prepare data loader for input image
        datalist = [{"image": image_path, "text": ""}]
        cache_dir = os.path.join(os.path.dirname(image_path), "cache")
        dataloader = merlin.data.DataLoader(
            datalist=datalist,
            cache_dir=cache_dir,
            batchsize=1,
            shuffle=False,
            num_workers=0,
        )

        # Perform inference
        with torch.no_grad():
            for batch in dataloader:
                outputs = self.model.model.encode_image(batch["image"].to(self.device))

                # Get phenotype predictions and probabilities
                softmax_outputs = torch.softmax(outputs[1], dim=1)[0]
                top_20_indices = torch.topk(softmax_outputs, 20).indices

                # Map phecodes to labels and probabilities
                phecode_to_label = dict(
                    zip(self.phecodes_df["phecode"], self.phecodes_df["phecode_str"])
                )
                formatted_output = "Top 20 Predicted Phenotypes:\n"
                formatted_output += "----------------------------------------\n"

                for idx in top_20_indices:
                    idx = int(idx.item())
                    phecode = self.phecodes_df.iloc[idx]["phecode"]
                    label = phecode_to_label.get(phecode, "Unknown")
                    probability = softmax_outputs[idx].item()
                    formatted_output += (
                        f"Label: {label}, Probability: {probability:.4f}\n"
                    )

        return formatted_output

    def explain(self) -> str:
        explanation = """
        The MerlinTask takes a path to a 3D CT image as input and processes it through a pre-trained Merlin model.
        It returns the top 20 predicted phenotypes with their associated probabilities as a formatted string, 
        making it useful for medical research, diagnosis, or analysis of complex medical images.
        
        This task requires a NIfTI-formatted image and provides phenotype predictions based on the trained model. 
        These predictions are not guaranteed to be diagnostic and should be used as an informational starting point.
        """
        return explanation
