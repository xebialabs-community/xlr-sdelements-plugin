from sdelements.SDEClient import SDEClient

client = SDEClient()
filters = []
result = client.get_tasks(project,task,filters)


