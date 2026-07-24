from azure.mgmt.servicebus import ServiceBusManagementClient

def servicebus(credential, subscription_id, resource_group_name, resource_name):
    client = ServiceBusManagementClient(credential, subscription_id)
    resource = client.namespaces.get(
        resource_group_name,
        resource_name
    )
    queues = list(client.queues.list_by_namespace(
        resource_group_name,
        resource_name
    ))
    queue_names = [q.name for q in queues]
    resource.queues = queue_names
    return resource
