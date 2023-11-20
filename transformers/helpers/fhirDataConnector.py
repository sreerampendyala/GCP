from typing import Any, Dict  # noqa: E402

# Imports the google.auth.transport.requests transport
from google.auth.transport import requests

# Imports a module to allow authentication using a service account
from google.oauth2 import service_account


class FHIRDataConnector: 
    def search_resources_get(
        self,
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        resource_type,
    ):
        """
        Uses the searchResources GET method to search for resources in the given FHIR store.

        See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
        before running the sample."""
        

        # Gets credentials from the environment.
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"
        credentials = service_account.Credentials.from_service_account_file(
            "creds.json"
        )
        scoped_credentials = credentials.with_scopes(
            ["https://www.googleapis.com/auth/cloud-platform"]
        )
        # Creates a requests Session object with the credentials.
        session = requests.AuthorizedSession(scoped_credentials)

        # URL to the Cloud Healthcare API endpoint and version
        base_url = "https://healthcare.googleapis.com/v1"

        # TODO(developer): Uncomment these lines and replace with your values.
        # project_id = 'my-project'  # replace with your GCP project ID
        # location = 'us-central1'  # replace with the parent dataset's location
        # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
        # fhir_store_id = 'my-fhir-store' # replace with the FHIR store ID
        # resource_type = 'Patient'  # replace with the FHIR resource type
        url = f"{base_url}/projects/{project_id}/locations/{location}"

        resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}".format(
            url, dataset_id, fhir_store_id, resource_type
        )

        response = session.get(resource_path)
        response.raise_for_status()

        resources = response.json()

        return resources


