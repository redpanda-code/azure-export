from azure.mgmt.containerservice import ContainerServiceClient

def managed_cluster(credential, subscription_id, resource_group_name, resource_name):
    client = ContainerServiceClient(
        credential=credential,
        subscription_id=subscription_id
    )
    managed_cluster = client.managed_clusters.get(
        resource_group_name,
        resource_name
    )
    return managed_cluster
