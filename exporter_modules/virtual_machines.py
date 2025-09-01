# Get the configuration of Azure virtual network
# Transform to desired target template format (bicep or terraform)
# Save to file system

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
