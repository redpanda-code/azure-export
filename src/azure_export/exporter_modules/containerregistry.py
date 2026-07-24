from azure.mgmt.containerregistry import ContainerRegistryManagementClient


def registry(credential, subscription_id, resource_group_name, resource_name):
    client = ContainerRegistryManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    registry = client.registries.get(
        resource_group_name,
        resource_name
    )
    return registry
