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
    r = dns_zone_records(
        credential,
        subscription_id,
        resource_group_name,
        resource_name
    )
    dns_zone.records = list(r)
    return dns_zone

def dns_zone_records(credential, subscription_id, resource_group_name, zone_name):
    client = DnsManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    return client.record_sets.list_by_dns_zone(
        resource_group_name,
        zone_name
    )


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

def virtual_network_link(credential, subscription_id, resource_group_name, private_zone_name, virtual_network_link_name):
    client = PrivateDnsManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    virtual_network_link = client.virtual_network_links.get(
        resource_group_name,
        private_zone_name,
        virtual_network_link_name
    )
    return virtual_network_link
