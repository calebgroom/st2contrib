
import requests
from pawn import client

from st2actions.runners.pythonrunner import Action

__all__ = [
    'CheckmateBaseAction'
]


class CheckmateBaseAction(Action):

    def __init__(self, config=None):
        super(CheckmateBaseAction, self).__init__(config)
        self.checkmateclient = client.CheckmateClient()
        tenant_creds = config.get('tenant_credentials') or {}
        if tenant_creds:
            if all(k in tenant_creds for k in ('apikey', 'username')):
                self.checkmateclient.authenticate(
                    username=tenant_creds['username'],
                    apikey=tenant_creds['apikey'])

    @property
    def version(self):
        return self.checkmateclient.server_version()

    def list_deployments(self, limit=5, offset=0, status='UP', **query):

        status = status or 'UP'
        limit = limit if limit <= 5 else 5
        return self.checkmateclient.list_deployments(
            limit=limit, offset=offset, status=status, **query)

    def get_deployment(self, deployment_id):
        deployment = self.checkmateclient.get_deployment(deployment_id)
        ret = {
            'status': deployment.get('status'),
            'resources': deployment.get('resources'),
            'name': deployment.get('name'),
            'id': deployment.get('id'),
            'created': deployment.get('created'),
            'operation': deployment.get('operation'),
        }
        return ret

    def add_nodes(self, deployment_id, service, count=1):
        """Add nodes to an existing deployment."""
        response = self.checkmateclient.add_nodes(deployment_id, service,
                                                  count)
        return response.status_code == requests.codes.ok

    def get_workflow(self, deployment_id, workflow_id):
        """Return summary data set for a workflow."""
        workflow = self.checkmateclient.get_workflow(workflow_id)
        return workflow['attributes']
