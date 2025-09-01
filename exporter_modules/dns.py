from azure.mgmt.dns import DnsManagementClient

def dns_zone(credential, subscription_id, resource_group_name, resource_name):
    client = DnsManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    dns_zone = client.zones.get(
        resource_group_name,
        resource_name
    )
    return dns_zone
