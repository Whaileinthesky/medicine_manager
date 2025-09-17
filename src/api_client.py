import requests

class DURClient:
    """A client for the DUR (Drug Utilization Review) API."""
    BASE_URL = "https://apis.data.go.kr/1471000/DURPrdlstInfoService03/getUsjntTabooInfoList03"

    def __init__(self, api_key: str, timeout: float = 10.0):
        if not api_key:
            raise ValueError("API key (DECODING_KEY) is missing. Please check your config.yaml.")
        self.api_key = api_key
        self.timeout = timeout

    def query_drug_interaction(
        self,
        item_name: str,
        page_no: int = 1,
        rows: int = 3,
        type_name: str = "병용금기",  # Contraindication
        output_format: str = "json",
    ) -> requests.Response:
        """Queries for contraindications for a given drug item."""
        params = {
            "serviceKey": self.api_key,
            "pageNo": str(page_no),
            "numOfRows": str(rows),
            "typeName": type_name,
            "itemName": item_name,
            "type": output_format,
        }
        response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response
