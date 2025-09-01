from azure.mgmt.storage import StorageManagementClient

def storage_account(credential, subscription_id, resource_group_name, resource_name):
    client = StorageManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

    # NOTE: get_properties() instead of get()
    storage_account = client.storage_accounts.get_properties(
        resource_group_name,
        resource_name
    )
    return storage_account
