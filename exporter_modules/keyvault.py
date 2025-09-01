from azure.mgmt.keyvault import KeyVaultManagementClient


def vault(credential, subscription_id, resource_group_name, resource_name):
    client = KeyVaultManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    vault = client.vaults.get(
        resource_group_name,
        resource_name
    )
    return vault
