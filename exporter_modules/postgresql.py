from azure.mgmt.postgresqlflexibleservers import PostgreSQLManagementClient

def server(credential, subscription_id, resource_group_name, resource_name):
    client = PostgreSQLManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    server = client.servers.get(
        resource_group_name,
        resource_name
    )
    return server
