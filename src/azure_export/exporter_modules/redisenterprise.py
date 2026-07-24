from azure.mgmt.redisenterprise import RedisEnterpriseManagementClient


def cache(credential, subscription_id, resource_group_name, resource_name):
    client = RedisEnterpriseManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    result = client.redis_enterprise.get(
        resource_group_name,
        resource_name
    )
    return result
