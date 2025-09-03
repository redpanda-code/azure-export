from azure.mgmt.network import NetworkManagementClient

def virtual_network(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    virtual_network = client.virtual_networks.get(
        resource_group_name,
        resource_name
    )
    return virtual_network

def public_ip_address(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    public_ip_address = client.public_ip_addresses.get(
        resource_group_name,
        resource_name
    )
    return public_ip_address

def public_ip_address(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    public_ip_address = client.public_ip_addresses.get(
        resource_group_name,
        resource_name
    )
    return public_ip_address


def public_ip_prefix(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    public_ip_prefix = client.public_ip_prefixes.get(
        resource_group_name,
        resource_name
    )
    return public_ip_prefix

def network_security_group(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    network_security_group = client.network_security_groups.get(
        resource_group_name,
        resource_name
    )
    return network_security_group

def network_interface(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    network_interface = client.network_interfaces.get(
        resource_group_name,
        resource_name
    )
    return network_interface

def load_balancer(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    load_balancer = client.load_balancers.get(
        resource_group_name,
        resource_name
    )
    return load_balancer

def nat_gateway(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    nat_gateway = client.nat_gateways.get(
        resource_group_name,
        resource_name
    )
    return nat_gateway



def dns_zone(credential, subscription_id, resource_group_name, resource_name):
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    network_interface = client.network_interfaces.get(
        resource_group_name,
        resource_name
    )
    return network_interface
