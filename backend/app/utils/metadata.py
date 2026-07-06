from pathlib import Path


class MetadataExtractor:

    DOMAIN_KEYWORDS = {
        "Safety": [
            "safety",
            "ppe",
            "hse",
        ],
        "HR": [
            "leave",
            "attendance",
            "employee",
            "hr",
        ],
        "Drilling": [
            "drilling",
            "rig",
            "well",
        ],
        "Finance": [
            "invoice",
            "budget",
            "finance",
        ],
    }

    def extract(self, filename: str, text: str):

        filename = filename.lower()

        text = text.lower()

        domain = "General"

        for key, words in self.DOMAIN_KEYWORDS.items():

            if any(word in filename or word in text for word in words):
                domain = key
                break

        return {
            "domain": domain,
            "department": domain,
        }