from sdetools.sdelib import restclient


class SDEClient(restclient):
    """
    Note: In all the API calls:
    - a 'project' arg variable is the project id
    - a 'task' arg variable is in the format <project_id>-<task_id>
        e.g. '127-T106'
    """

    def __init__(self, conf_prefix, conf_name, config):
        pass

    def get_tasks(self, project, **filters):
        """
        Get all tasks for a project indicated by the ID of the project
        """
        filters['absolute_urls'] = True
        result = self.call_api('projects/%d/tasks/' % project, args=filters)
        return result['results']
