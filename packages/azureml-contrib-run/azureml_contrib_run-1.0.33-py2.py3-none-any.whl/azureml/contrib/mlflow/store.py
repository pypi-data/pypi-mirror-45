# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowStore** provides a class to read and record run metrics and artifacts on Azure via MLflow."""

import logging
import os

from mlflow.store.rest_store import RestStore
from mlflow.utils.rest_utils import MlflowHostCreds

from azureml.core import Workspace
from azureml.core.authentication import AzureMLTokenAuthentication

from azureml._restclient.run_client import RunClient


logger = logging.getLogger(__name__)

PARAM_PREFIX = "azureml.param."
_MLFLOW_RUN_ID_ENV_VAR = "MLFLOW_RUN_ID"
_EXPERIMENT_NAME_ENV_VAR = "MLFLOW_EXPERIMENT_NAME"


class AzureMLRestStore(RestStore):
    """Client for a remote tracking server accessed via REST API calls."""

    def __init__(self, workspace=None, artifact_uri=None):
        """Construct an AzureMLRestStore object."""
        self._artifact_uri = artifact_uri
        self.workspace = workspace if workspace is not None else Workspace.from_config()
        self.get_host_creds = self.get_host_credentials
        super(AzureMLRestStore, self).__init__(self.get_host_creds)

    def get_host_credentials(self):
        """Construct a MlflowHostCreds to be used for obtaining fresh credentials."""
        return MlflowHostCreds(
            self.workspace.service_context._get_run_history_url() +
            "/history/v1.0" + self.workspace.service_context._get_workspace_scope(),
            token=self.workspace._auth.get_authentication_header()["Authorization"][7:])

    def create_run(self, *args, **kwargs):
        """Create a run and set the AzureMLTokenAuthentication in the workspace."""
        run = super(AzureMLRestStore, self).create_run(*args, **kwargs)
        if not isinstance(self.workspace._auth, AzureMLTokenAuthentication) and _EXPERIMENT_NAME_ENV_VAR in os.environ:
            run_uuid = run.info.run_uuid
            experiment_name = os.environ[_EXPERIMENT_NAME_ENV_VAR]
            run_client = RunClient(self.workspace.service_context, experiment_name, run_uuid)
            token = run_client.get_token().token
            auth_object = AzureMLTokenAuthentication.create(
                azureml_access_token=token,
                expiry_time=None,
                host=self.workspace.service_context._get_run_history_url(),
                subscription_id=self.workspace.subscription_id,
                resource_group_name=self.workspace.resource_group,
                workspace_name=self.workspace.name,
                experiment_name=experiment_name,
                run_id=run_uuid
            )
            self.workspace._auth = auth_object

        return run
