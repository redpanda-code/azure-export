from azure.mgmt.mysqlflexibleservers import MySQLManagementClient


def server(credential, subscription_id, resource_group_name, resource_name):
    client = MySQLManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    result = client.servers.get(
        resource_group_name,
        resource_name
    )
    return result
