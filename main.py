import os
from dotenv import dotenv_values
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
import jsonpickle
import pathlib
import pprint
import datetime

config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.secret")
}

class DatetimeHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')

jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)


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
        print(f"Resource group: {rg.name} in {rg.location}")
        rg_path = pathlib.Path(output_path, rg.name)
        rg_path.mkdir(parents=True, exist_ok=True)

        for resource in client.resources.list_by_resource_group(rg.name):
            result = None

            match resource.type:
                case "Microsoft.Compute/virtualMachines":
                    from exporter_modules import virtual_machines
                    result = virtual_machines.machine(credential, subscription_id, rg.name, resource.name)
                
                case "Microsoft.Network/virtualNetworks":
                    from exporter_modules import virtual_networks
                    result = virtual_networks.network(credential, subscription_id, rg.name, resource.name)
                
                case _:
                    print(f"  Resource: {resource.name} of type {resource.type}")


            if result is not None:            
                file_path = pathlib.Path(rg_path, f"{resource.name}.json")
                with open(file_path, "w") as f:
                    f.write(jsonpickle.encode(result, indent=4))


    # remove all empty folders in output_path
    for dirpath, dirnames, filenames in os.walk(output_path, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)


if __name__ == "__main__":
    main()
