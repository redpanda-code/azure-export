# deprecated legacy redis offering
from azure.mgmt.redis import RedisManagementClient


def cache(credential, subscription_id, resource_group_name, resource_name):
    client = RedisManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    result = client.redis.get(
        resource_group_name,
        resource_name
    )
    return result
