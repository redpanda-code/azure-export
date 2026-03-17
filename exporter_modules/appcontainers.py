from azure.mgmt.appcontainers import ContainerAppsAPIClient

def container_app(credential, subscription_id, resource_group_name, resource_name):
    client = ContainerAppsAPIClient(
        credential=credential,
        subscription_id=subscription_id
    )
    app = client.container_apps.get(
        resource_group_name,
        resource_name
    )
    return app
