from azure.mgmt.containerinstance import ContainerInstanceManagementClient

def container_group(credential, subscription_id, resource_group_name, resource_name):
    client = ContainerInstanceManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    container_group = client.container_groups.get(
        resource_group_name,
        resource_name
    )
    return container_group
