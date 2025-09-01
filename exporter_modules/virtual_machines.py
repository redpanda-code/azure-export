from azure.mgmt.compute import ComputeManagementClient

def machine(credential, subscription_id, resource_group_name, resource_name):
    client = ComputeManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    machine = client.virtual_machines.get(
        resource_group_name,
        resource_name
    )
    return machine


def disk(credential, subscription_id, resource_group_name, resource_name):
    client = ComputeManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    disk = client.disks.get(
        resource_group_name,
        resource_name
    )
    return disk

def image(credential, subscription_id, resource_group_name, resource_name):
    client = ComputeManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    image = client.images.get(
        resource_group_name,
        resource_name
    )
    return image
