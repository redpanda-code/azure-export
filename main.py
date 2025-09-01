import os
from dotenv import dotenv_values
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
import jsonpickle
import pathlib
import datetime
import json

from exporter_modules import virtual_machines
from exporter_modules import network
from exporter_modules import resource_group
from exporter_modules import storage
from exporter_modules import keyvault
from exporter_modules import containerregistry
from exporter_modules import dns
from exporter_modules import postgresql
from exporter_modules import sql

config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.secret")
}

class DatetimeHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')

jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)

def remove_property_recursive(obj, property_name):
    if isinstance(obj, dict):
        return {k: remove_property_recursive(v, property_name) for k, v in obj.items() if k != property_name}
    elif isinstance(obj, list):
        return [remove_property_recursive(item, property_name) for item in obj]
    else:
        return obj

def write_azure_data(result, file_path):
    d_json = jsonpickle.encode(result, indent=2) # jsonpickle tuns objecs/class into json
    d_obj = json.loads(d_json)
    d_obj = remove_property_recursive(d_obj, "etag")
    d_obj = remove_property_recursive(d_obj, "py/object")
    with open(file_path, "w") as f:
        f.write(json.dumps(d_obj, indent=2))

def main():
    credential = ClientSecretCredential(
        tenant_id=config["AZURE_TENANT_ID"],
        client_id=config["AZURE_CLIENT_ID"],
        client_secret=config["AZURE_CLIENT_SECRET"]
    )

    subscription_id = config.get("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        raise ValueError("AZURE_SUBSCRIPTION_ID not found in configuration")

    output_path = pathlib.Path("export/")
    output_path.mkdir(parents=True, exist_ok=True)


    client = ResourceManagementClient(credential=credential, subscription_id=subscription_id)
    for rg in client.resource_groups.list():
        rg_path = pathlib.Path(output_path, rg.name)
        rg_path.mkdir(parents=True, exist_ok=True)

        result = resource_group.resource_group(credential, subscription_id, rg.name)
        file_path = pathlib.Path(rg_path, f"{rg.name}.json")
        write_azure_data(result, file_path)

        resources = list(client.resources.list_by_resource_group(rg.name))

        print(f"Resource group: {rg.name} in {rg.location} ({len(resources)} resources)")

        for resource in resources:
            result = None
            file_path = f"{resource.name}.json"

            if str(resource.type).endswith("/extensions"):
                continue

            match resource.type:
                # VM, disk, nsg, ip often go together, maybe they can be grouped
                case "Microsoft.Compute/virtualMachines":
                    result = virtual_machines.machine(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Compute/disks":
                    result = virtual_machines.disk(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Network/networkSecurityGroups":
                    result = network.network_security_group(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Network/publicIPAddresses":
                    result = network.public_ip_address(credential, subscription_id, rg.name, resource.name)

                case "Microsoft.Network/virtualNetworks":
                    result = network.virtual_network(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Compute/images":
                    result = virtual_machines.image(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Network/networkInterfaces":
                    result = network.network_interface(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Network/loadBalancers":
                    result = network.load_balancer(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Storage/storageAccounts":
                    result = storage.storage_account(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.KeyVault/vaults":
                    result = keyvault.vault(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.ContainerRegistry/registries":
                    result = containerregistry.registry(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Network/dnszones":
                    p = pathlib.Path(rg_path, "dns")
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path("dns", f"{resource.name}.json")
                    result = dns.dns_zone(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Network/privateDnsZones":
                    p = pathlib.Path(rg_path, "private_dns")
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path("private_dns", f"{resource.name}.json")
                    result = dns.private_zone(credential, subscription_id, rg.name, resource.name)
                # "Microsoft.Network/privateDnsZones/virtualNetworkLinks"
                case "Microsoft.DBforPostgreSQL/flexibleServers":
                    result = postgresql.server(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Network/publicIPPrefixes":
                    result = network.public_ip_prefix(credential, subscription_id, rg.name, resource.name)
                    pass
                case "Microsoft.Sql/servers":
                    p = pathlib.Path(rg_path, resource.name)
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path(resource.name, f"{resource.name}.json")
                    result = sql.server(credential, subscription_id, rg.name, resource.name)
                case "Microsoft.Sql/servers/elasticpools":
                    server_name, pool_name = resource.name.split("/")
                    p = pathlib.Path(rg_path, server_name)
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path(server_name, f"{pool_name}.json")
                    result = sql.elastic_pool(credential, subscription_id, rg.name, server_name, pool_name)
                case "Microsoft.Sql/servers/databases":
                    server_name, database_name = resource.name.split("/")
                    p = pathlib.Path(rg_path, server_name, "databases")
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path(server_name, "databases", f"{database_name}.json")
                    result = sql.database(credential, subscription_id, rg.name, server_name, database_name)

                # "Microsoft.ContainerService/managedClusters"
                # Microsoft.Compute/virtualMachineScaleSets
                # "Microsoft.Network/connections"
                # "Microsoft.Network/virtualNetworkGateways"
                # "Microsoft.Network/natGateways"
                # "Microsoft.Network/localNetworkGateways"
                # "Microsoft.Compute/sshPublicKeys"
                # "Microsoft.Network/privateDnsZones/virtualNetworkLinks"
                # "microsoft.insights/webtests"
                case "Microsoft.DomainRegistration/domains":
                    pass # ignoring domain registrations
                case "Microsoft.Automation/automationAccounts" | "Microsoft.Automation/automationAccounts/runbooks":
                    pass # ignoring automation for now
                case "Microsoft.RecoveryServices/vaults" | "Microsoft.Compute/restorePointCollections":
                    pass # ignoring recovery services for now
                case "Microsoft.ContainerInstance/containerGroups":
                    pass # ignoring container instances for now
                case "Microsoft.DocumentDb/databaseAccounts":
                    pass # ignoring documentdb for now
                case "microsoft.visualstudio/account":
                    pass # ignoring devops subscription
                case "microsoft.insights/actiongroups" | "Microsoft.OperationalInsights/workspaces" | "Microsoft.AlertsManagement/actionRules" | "Microsoft.Insights/actiongroups" | "microsoft.insights/metricalerts" | "microsoft.monitor/accounts" | "microsoft.monitor/accounts" | "microsoft.alertsmanagement/smartDetectorAlertRules":
                    pass # ignoring monitoring for now
                case "Microsoft.Network/networkWatchers" | "Microsoft.EventGrid/systemTopics":
                    pass # ignore azure defaults
                case "Microsoft.Insights/metricalerts" | "Microsoft.Insights/workbooks" | "Microsoft.AlertsManagement/prometheusRuleGroups" | "Microsoft.Insights/dataCollectionEndpoints" | "Microsoft.Insights/dataCollectionRules":
                    pass # ignore metrics stuff for now
                case "Microsoft.ManagedIdentity/userAssignedIdentities" | "Microsoft.OperationsManagement/solutions" | "Microsoft.Portal/dashboards":
                    pass
                case _:
                    print(f"  Resource: {resource.name} of type {resource.type}")


            if result is not None:
                file_path = pathlib.Path(rg_path, file_path)
                write_azure_data(result, file_path)


    # remove all empty folders in output_path
    for dirpath, dirnames, filenames in os.walk(output_path, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)


if __name__ == "__main__":
    main()
