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
from exporter_modules import containerservice
from exporter_modules import sqlvirtualmachine

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

        if rg.name.startswith("MA_"):
            continue # skipping automatic created monitoring resource groups

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

            match resource.type.lower():
                # VM, disk, nsg, ip often go together, maybe they can be grouped
                case "microsoft.compute/virtualmachines":
                    result = virtual_machines.machine(credential, subscription_id, rg.name, resource.name)
                case "microsoft.compute/disks":
                    result = virtual_machines.disk(credential, subscription_id, rg.name, resource.name)
                case "microsoft.network/networksecuritygroups":
                    result = network.network_security_group(credential, subscription_id, rg.name, resource.name)
                case "microsoft.network/publicipaddresses":
                    result = network.public_ip_address(credential, subscription_id, rg.name, resource.name)

                case "microsoft.network/virtualnetworks":
                    result = network.virtual_network(credential, subscription_id, rg.name, resource.name)
                case "microsoft.compute/images":
                    result = virtual_machines.image(credential, subscription_id, rg.name, resource.name)
                case "microsoft.network/networkinterfaces":
                    result = network.network_interface(credential, subscription_id, rg.name, resource.name)
                case "microsoft.network/loadbalancers":
                    result = network.load_balancer(credential, subscription_id, rg.name, resource.name)
                case "microsoft.storage/storageaccounts":
                    result = storage.storage_account(credential, subscription_id, rg.name, resource.name)
                case "microsoft.keyvault/vaults":
                    result = keyvault.vault(credential, subscription_id, rg.name, resource.name)
                case "microsoft.containerregistry/registries":
                    result = containerregistry.registry(credential, subscription_id, rg.name, resource.name)
                case "microsoft.network/dnszones":
                    p = pathlib.Path(rg_path, "dns")
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path("dns", f"{resource.name}.json")
                    result = dns.dns_zone(credential, subscription_id, rg.name, resource.name)
                case "microsoft.network/privatednszones":
                    p = pathlib.Path(rg_path, "private_dns")
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path("private_dns", f"{resource.name}.json")
                    result = dns.private_zone(credential, subscription_id, rg.name, resource.name)
                case "microsoft.network/privatednszones/virtualnetworklinks":
                    dns_name, link_name = resource.name.split("/")
                    p = pathlib.Path(rg_path, "private_dns_link")
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path("private_dns_link", f"{link_name}.json")
                    result = dns.virtual_network_link(credential, subscription_id, rg.name, dns_name, link_name)
                case "microsoft.dbforpostgresql/flexibleservers":
                    result = postgresql.server(credential, subscription_id, rg.name, resource.name)
                case "microsoft.network/publicipprefixes":
                    result = network.public_ip_prefix(credential, subscription_id, rg.name, resource.name)
                    pass
                case "microsoft.sql/servers":
                    p = pathlib.Path(rg_path, resource.name)
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path(resource.name, f"{resource.name}.json")
                    result = sql.server(credential, subscription_id, rg.name, resource.name)
                case "microsoft.sql/servers/elasticpools":
                    server_name, pool_name = resource.name.split("/")
                    p = pathlib.Path(rg_path, server_name)
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path(server_name, f"{pool_name}.json")
                    result = sql.elastic_pool(credential, subscription_id, rg.name, server_name, pool_name)
                case "microsoft.sql/servers/databases":
                    server_name, database_name = resource.name.split("/")
                    p = pathlib.Path(rg_path, server_name, "databases")
                    p.mkdir(parents=True, exist_ok=True)
                    file_path = pathlib.Path(server_name, "databases", f"{database_name}.json")
                    result = sql.database(credential, subscription_id, rg.name, server_name, database_name)

                case "microsoft.network/natgateways":
                    result = network.nat_gateway(credential, subscription_id, rg.name, resource.name)

                case "microsoft.network/routetables":
                    result = network.route_table(credential, subscription_id, rg.name, resource.name)

                case "microsoft.network/virtualnetworkgateways":
                    result = network.virtual_network_gateway(credential, subscription_id, rg.name, resource.name)

                case "microsoft.network/localnetworkgateways":
                    result = network.local_network_gateway(credential, subscription_id, rg.name, resource.name)

                case "microsoft.compute/virtualmachinescalesets":
                    result = virtual_machines.virtual_machine_scale_set(credential, subscription_id, rg.name, resource.name)

                case "microsoft.containerservice/managedclusters":
                    result = containerservice.managed_cluster(credential, subscription_id, rg.name, resource.name)


# sql database instance
#   Resource: sql-yw-test of type Microsoft.Sql/managedInstances
#   Resource: mi_default_275ce4f3-33df-44cc-8e85-f9545083b8bf_10-0-0-0-24 of type Microsoft.Network/networkIntentPolicies
#   Resource: VirtualCluster38645a5d-0814-4ed9-bc20-16d3bb81d3bb of type Microsoft.Sql/virtualClusters

                case "microsoft.sqlvirtualmachine/sqlvirtualmachines":
                    result = sqlvirtualmachine.sql_virtual_machine(credential, subscription_id, rg.name, resource.name)
                    file_path = f"{resource.name}_sqlvm.json" # avoid duplicate names

                case "microsoft.compute/sshpublickeys":
                    pass # we cant export private key

                case "microsoft.insights/webtests" | "microsoft.logic/workflows":
                    pass
                case "microsoft.web/connections":
                    pass
                case "microsoft.domainregistration/domains":
                    pass # ignoring domain registrations
                case "microsoft.automation/automationaccounts" | "microsoft.automation/automationaccounts/runbooks":
                    pass # ignoring automation for now
                case "microsoft.recoveryservices/vaults" | "microsoft.compute/restorepointcollections" | "microsoft.dataprotection/backupvaults":
                    pass # ignoring recovery services for now
                case "microsoft.containerinstance/containergroups":
                    pass # ignoring container instances for now
                case "microsoft.documentdb/databaseaccounts":
                    pass # ignoring documentdb for now
                case "microsoft.maintenance/maintenanceconfigurations":
                    pass
                case "microsoft.visualstudio/account":
                    pass # ignoring devops subscription
                case "microsoft.operationalinsights/querypacks" | "microsoft.dashboard/grafana" | "microsoft.insights/components" | "microsoft.insights/actiongroups" | "microsoft.operationalinsights/workspaces" | "microsoft.alertsmanagement/actionrules" | "microsoft.insights/metricalerts" | "microsoft.monitor/accounts" | "microsoft.alertsmanagement/smartdetectoralertrules":
                    pass # ignoring monitoring for now
                case "microsoft.network/networkwatchers" | "microsoft.eventgrid/systemtopics":
                    pass # ignore azure defaults
                case "microsoft.insights/metricalerts" | "microsoft.insights/workbooks" | "microsoft.alertsmanagement/prometheusrulegroups" | "microsoft.insights/datacollectionendpoints" | "microsoft.insights/datacollectionrules":
                    pass # ignore metrics stuff for now
                case "microsoft.managedidentity/userassignedidentities" | "microsoft.operationsmanagement/solutions" | "microsoft.portal/dashboards":
                    pass
                case _:
                    print(f"  Resource: {resource.name} of type {resource.type}")


            if result is not None:
                # print id, name, type, location, tags

                file_path = pathlib.Path(rg_path, file_path)
                write_azure_data(result, file_path)


    # remove all empty folders in output_path
    for dirpath, dirnames, filenames in os.walk(output_path, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)


if __name__ == "__main__":
    main()
