from azure.mgmt.resource import ResourceManagementClient


def resource_group(credential, subscription_id, resource_group_name):
    client = ResourceManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    resource_group = client.resource_groups.get(
        resource_group_name
    )
    return resource_group
