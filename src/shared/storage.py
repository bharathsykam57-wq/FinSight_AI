"""
Azure Blob Storage Service Module.

Handles uploading generated markdown reports to Azure Blob Storage
so they persist permanently after the container shuts down.

Usage:
    from src.shared.storage import StorageService
    storage = StorageService()
    url = storage.upload_file("report.md", "investment_report_NVDA.md")
"""

from azure.storage.blob import BlobServiceClient
from src.shared.config import settings


class StorageService:
    """Manages file uploads to Azure Blob Storage."""

    def __init__(self) -> None:
        """Initialize the Blob Storage client and ensure container exists."""
        self.service_client = BlobServiceClient.from_connection_string(
            settings.azure_blob_storage_connection_string
        )
        self.container_name = "reports"
        self._ensure_container_exists()

    def _ensure_container_exists(self) -> None:
        """Creates the reports container if it does not already exist."""
        try:
            container_client = self.service_client.get_container_client(
                self.container_name
            )
            if not container_client.exists():
                container_client.create_container()
        except (ValueError, RuntimeError) as e:
            print(f"Warning checking container: {e}")

    def upload_file(self, file_path: str, destination_name: str) -> str:
        """
        Uploads a local file to Azure Blob Storage.

        Args:
            file_path: Local path to the file (e.g., 'report.md').
            destination_name: Name the file should have in the cloud.

        Returns:
            The public URL of the uploaded blob, or an error message string.
        """
        try:
            blob_client = self.service_client.get_blob_client(
                container=self.container_name,
                blob=destination_name
            )
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

            return (
                f"https://{self.service_client.account_name}"
                f".blob.core.windows.net/{self.container_name}/{destination_name}"
            )

        except (ValueError, FileNotFoundError, RuntimeError) as e:
            return f"Error uploading to Azure: {str(e)}"