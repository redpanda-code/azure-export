from azure.mgmt.web import WebSiteManagementClient

# know as App Service Plan
def server_farm(credential, subscription_id, resource_group_name, resource_name):
    client = WebSiteManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    result = client.app_service_plans.get(
        resource_group_name,
        resource_name
    )
    return result


# also covers functions
def web_app(credential, subscription_id, resource_group_name, resource_name):
    client = WebSiteManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    result = client.web_apps.get(
        resource_group_name,
        resource_name
    )
    return result

