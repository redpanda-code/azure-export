# Get the configuration of Azure virtual network
# Transform to desired target template format (bicep or terraform)
# Save to file system

from azure.mgmt.network import NetworkManagementClient

def network(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

    network = client.virtual_networks.get(
        resource_group_name,
        resource_name
    )

    return network
