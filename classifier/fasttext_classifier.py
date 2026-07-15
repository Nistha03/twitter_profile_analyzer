import os
import re
import fasttext
from typing import Tuple

class FastTextClassifier:
    def __init__(self, model_path: str = "models/google_taxonomy_model.bin") -> None:
        self.model_path = model_path
        self.model = None

    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        text = re.sub(r"@\w+|#\w+", "", text)
        return re.sub(r"\s+", " ", text).strip().lower()

    def train_model_from_file(self) -> None:
        training_data_path = "models/taxonomy_train.txt"
        os.makedirs("models", exist_ok=True)
        
        # Only create the backup file if the user's friend's file is missing!
        if not os.path.exists(training_data_path):
            dataset_content = (
                "__label__electronics new apple silicon computer system updates engineering laptop smartphone gadget.\n"
                "__label__software python code machine learning frameworks application architecture programming bugs ui dev.\n"
                "__label__apparel fashion summer clothing trends lifestyle organic streetwear shirt shoes outfit designer.\n"
                "__label__media movies streaming entertainment cinema reviews music video broadcast podcast.\n"
            )
            with open(training_data_path, "w", encoding="utf-8") as f:
                f.write(dataset_content)
        
        # --- OPTIMIZED FOR SPEED ---
        # Changed epoch to 5 and wordNgrams to 1 so training finishes in minutes
        self.model = fasttext.train_supervised(input=training_data_path, epoch=5, lr=0.1, wordNgrams=1)
        self.model.save_model(self.model_path)

    def load_model(self) -> None:
        if not os.path.exists(self.model_path):
            self.train_model_from_file()
        self.model = fasttext.load_model(self.model_path)

    def predict_category(self, text: str) -> Tuple[str, float]:
        if not self.model:
            self.load_model()
        cleaned = self.clean_text(text)
        if not cleaned:
            return "Uncategorized", 0.0
        labels, probabilities = self.model.predict(cleaned, k=1)
        return labels[0].replace("__label__", ""), float(probabilities[0])