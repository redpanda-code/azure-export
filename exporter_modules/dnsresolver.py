from azure.mgmt.dnsresolver import DnsResolverManagementClient

def dns_resolver(credential, subscription_id, resource_group_name, resource_name):
    client = DnsResolverManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    dns_resolver = client.dns_resolvers.get(
        resource_group_name,
        resource_name
    )
    return dns_resolver

def inbound_endpoint(credential, subscription_id, resource_group_name, dns_resolver_name, inbound_endpoint_name):
    client = DnsResolverManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    inbound_endpoint = client.inbound_endpoints.get(
        resource_group_name,
        dns_resolver_name,
        inbound_endpoint_name
    )
    return inbound_endpoint

def outbound_endpoint(credential, subscription_id, resource_group_name, dns_resolver_name, outbound_endpoint_name):
    client = DnsResolverManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    outbound_endpoint = client.outbound_endpoints.get(
        resource_group_name,
        dns_resolver_name,
        outbound_endpoint_name
    )
    return outbound_endpoint
