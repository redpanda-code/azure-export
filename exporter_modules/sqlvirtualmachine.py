from azure.mgmt.sqlvirtualmachine import SqlVirtualMachineManagementClient

def sql_virtual_machine(credential, subscription_id, resource_group_name, resource_name):
    client = SqlVirtualMachineManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    sql_virtual_machine = client.sql_virtual_machines.get(
        resource_group_name,
        resource_name
    )
    return sql_virtual_machine
