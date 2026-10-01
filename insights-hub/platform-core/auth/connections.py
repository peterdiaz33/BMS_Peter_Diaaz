# platform-core/data/connections.py

from typing import Any, Dict

class DataWarehouseStub:
    """
    Stubbed data warehouse connection.
    In reality, this would connect to a real warehouse.
    """

    def query(self, tenant: str, query: str) -> Dict[str, Any]:
        # Return fake data based on tenant and query
        return {
            "tenant": tenant,
            "query": query,
            "data": [{"id": 1, "value": "stubbed-result"}],
        }


class RestApiStub:
    """
    Stubbed internal REST API client.
    """

    def get(self, tenant: str, path: str) -> Dict[str, Any]:
        return {
            "tenant": tenant,
            "path": path,
            "data": {"status": "ok", "message": "stubbed-api-response"},
        }
