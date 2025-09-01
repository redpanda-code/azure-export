from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.privatedns import PrivateDnsManagementClient

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


def private_zone(credential, subscription_id, resource_group_name, resource_name):
    client = PrivateDnsManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    private_zone = client.private_zones.get(
        resource_group_name,
        resource_name
    )
    return private_zone

def virtual_network_link(credential, subscription_id, resource_group_name, resource_name):
    client = PrivateDnsManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    virtual_network_link = client.virtual_network_links.get(
        resource_group_name,
        resource_name
    )
    return virtual_network_link
