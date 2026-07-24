from azure.mgmt.sql import SqlManagementClient

def server(credential, subscription_id, resource_group_name, resource_name):
    client = SqlManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

    server = client.servers.get(
        resource_group_name,
        resource_name
    )
    return server

def database(credential, subscription_id, resource_group_name, server_name, database_name):
    client = SqlManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

    database = client.databases.get(
        resource_group_name,
        server_name,
        database_name
    )
    return database

def elastic_pool(credential, subscription_id, resource_group_name, server_name, elastic_pool_name):
    client = SqlManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

    elastic_pool = client.elastic_pools.get(
        resource_group_name,
        server_name,
        elastic_pool_name
    )
    return elastic_pool
