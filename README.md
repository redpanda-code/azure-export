
# Exporter
Exporter creates a folder structure that mirrors your Azure configuration
Each folder represents a resource group and contains the definitions.


# Resource Support

## Compute
| Resource Type | Status |
|---|---|
| microsoft.compute/virtualmachines | ✅ Exported |
| microsoft.compute/disks | ✅ Exported |
| microsoft.compute/images | ✅ Exported |
| microsoft.compute/virtualmachinescalesets | ✅ Exported |
| microsoft.containerregistry/registries | ✅ Exported |
| microsoft.containerservice/managedclusters (AKS) | ✅ Exported |
| microsoft.sqlvirtualmachine/sqlvirtualmachines | ✅ Exported |
| microsoft.compute/sshpublickeys | ⏭️ Skipped (can't export private key) |
| microsoft.compute/restorepointcollections | ⏭️ Skipped |
| microsoft.containerinstance/containergroups | ✅ Exported |
| microsoft.compute/availabilitysets | ❌ Not handled |
| microsoft.app/containerapps | ❌ Not handled |
| microsoft.batch/batchaccounts | ❌ Not handled |
| microsoft.servicefabric/clusters | ❌ Not handled |
| microsoft.web/serverfarms | ✅ Exported |
| microsoft.web/sites (App Service ) | ✅ Exported |
| microsoft.web/sites (Functions) | ✅ Exported |


## Networking
| Resource Type | Status |
|---|---|
| microsoft.network/virtualnetworks | ✅ Exported |
| microsoft.network/networkinterfaces | ✅ Exported |
| microsoft.network/publicipaddresses | ✅ Exported |
| microsoft.network/publicipprefixes | ✅ Exported |
| microsoft.network/loadbalancers | ✅ Exported |
| microsoft.network/networksecuritygroups | ✅ Exported |
| microsoft.network/routetables | ✅ Exported |
| microsoft.network/privateendpoints | ✅ Exported |
| microsoft.network/natgateways | ✅ Exported |
| microsoft.network/virtualnetworkgateways | ✅ Exported |
| microsoft.network/localnetworkgateways | ✅ Exported |
| microsoft.network/connections | ✅ Exported |
| microsoft.network/dnszones | ✅ Exported |
| microsoft.network/privatednszones | ✅ Exported |
| microsoft.network/privatednszones/virtualnetworklinks | ✅ Exported |
| microsoft.network/dnsresolvers | ✅ Exported |
| microsoft.network/dnsresolvers/inboundendpoints | ✅ Exported |
| microsoft.network/dnsresolvers/outboundendpoints | ✅ Exported |
| microsoft.network/networkwatchers | ⏭️ Skipped (Azure default) |
| microsoft.network/applicationgateways | ✅ Exported |
| microsoft.network/expressroutecircuits | ❌ Not handled |
| microsoft.network/firewalls | ❌ Not handled |
| microsoft.network/trafficmanagerprofiles | ❌ Not handled |
| microsoft.network/frontdoors | ❌ Not handled |
| microsoft.network/bastionhosts | ❌ Not handled |
| microsoft.cdn/profiles | ❌ Not handled |

## Storage
| Resource Type | Status |
|---|---|
| microsoft.storage/storageaccounts | ✅ Exported |
| microsoft.netapp/netappaccounts | ❌ Not handled |
| microsoft.elasticsan/elasticsans | ❌ Not handled |

## Databases
| Resource Type | Status |
|---|---|
| microsoft.sql/servers | ✅ Exported |
| microsoft.sql/servers/databases | ✅ Exported |
| microsoft.sql/servers/elasticpools | ✅ Exported |
| microsoft.dbforpostgresql/flexibleservers | ✅ Exported |
| microsoft.documentdb/databaseaccounts (Cosmos DB) | ⏭️ Skipped |
| microsoft.sql/managedinstances | ❌ Not handled |
| microsoft.cache/redis | ✅ Exported |
| microsoft.dbformysql/servers | ✅ Exported  |
| microsoft.dbformariadb/servers | ❌ Not handled |
| microsoft.kusto/clusters (Data Explorer) | ❌ Not handled |

## Security & Identity
| Resource Type | Status |
|---|---|
| microsoft.keyvault/vaults | ✅ Exported |
| microsoft.managedidentity/userassignedidentities | ⏭️ Skipped |
| microsoft.logic/integrationaccounts | ⏭️ Skipped (can't export private key) |

## Monitoring & Observability
| Resource Type | Status |
|---|---|
| microsoft.insights/components (App Insights) | ⏭️ Skipped |
| microsoft.insights/workbooks | ⏭️ Skipped |
| microsoft.insights/metricalerts | ⏭️ Skipped |
| microsoft.insights/activitylogalerts | ⏭️ Skipped |
| microsoft.insights/actiongroups | ⏭️ Skipped |
| microsoft.insights/webtests | ⏭️ Skipped |
| microsoft.insights/datacollectionendpoints | ⏭️ Skipped |
| microsoft.insights/datacollectionrules | ⏭️ Skipped |
| microsoft.operationalinsights/workspaces | ⏭️ Skipped |
| microsoft.operationalinsights/querypacks | ⏭️ Skipped |
| microsoft.alertsmanagement/actionrules | ⏭️ Skipped |
| microsoft.alertsmanagement/smartdetectoralertrules | ⏭️ Skipped |
| microsoft.alertsmanagement/prometheusrulegroups | ⏭️ Skipped |
| microsoft.monitor/accounts | ⏭️ Skipped |
| microsoft.dashboard/grafana | ⏭️ Skipped |

## Integration & Messaging
| Resource Type | Status |
|---|---|
| microsoft.eventgrid/systemtopics | ⏭️ Skipped (Azure default) |
| microsoft.logic/workflows | ⏭️ Skipped |
| microsoft.web/connections | ⏭️ Skipped |
| microsoft.servicebus/namespaces | ✅ Exported |
| microsoft.eventhub/namespaces | ❌ Not handled |
| microsoft.eventgrid/topics | ❌ Not handled |
| microsoft.apimanagement/service | ❌ Not handled |

## DevOps & Automation
| Resource Type | Status |
|---|---|
| microsoft.automation/automationaccounts | ⏭️ Skipped |
| microsoft.automation/automationaccounts/runbooks | ⏭️ Skipped |
| microsoft.visualstudio/account (Azure DevOps) | ⏭️ Skipped |

## Backup & Recovery
| Resource Type | Status |
|---|---|
| microsoft.recoveryservices/vaults | ⏭️ Skipped |
| microsoft.dataprotection/backupvaults | ⏭️ Skipped |

## Other
| Resource Type | Status |
|---|---|
| microsoft.domainregistration/domains | ⏭️ Skipped |
| microsoft.maintenance/maintenanceconfigurations | ⏭️ Skipped |
| microsoft.portal/dashboards | ⏭️ Skipped |
| microsoft.operationsmanagement/solutions | ⏭️ Skipped |
| microsoft.machinelearningservices/workspaces | ❌ Not handled |
| microsoft.cognitiveservices/accounts | ❌ Not handled |
| microsoft.search/searchservices | ❌ Not handled |
| microsoft.datafactory/factories | ❌ Not handled |
| microsoft.databricks/workspaces | ❌ Not handled |
| microsoft.synapse/workspaces | ❌ Not handled |
| microsoft.web/staticsites | ❌ Not handled |

**Legend:** ✅ Exported to JSON | ⏭️ Recognized but intentionally skipped | ❌ Falls through to unhandled (printed to console)


# Getting Started
> You don't need to use uv, a requirements.txt has been provided for pip users.

1. Create an application under "App registrations"
2. Under Manage > Certificate&secrets, create a new client secret
3. Under Subscription > IAM, add role Reader for your created application
4. uv sync
5. uv run main.py


# next steps
- testing: setup bicep or terraform to create a vnet, and use the exporter to export it again


# Testing instructions
- always make sure you test with an account that has only reader permissions
-

# Notes
- does every resource have a CreatedAt?
- Is there an existing DTO for each resource in the bicep codebase
- do I need to cache client auth?
- can you group VM related resources? (disk, ip, nsg)
- what is the base interface all resources share

# Learnings
- annoying that storage account does not implement ".get()" to match all other apis
- annoying that sub resources do not take a resource name, instead want you to split the properties for that sub resource (sql databases).
- Multiple resources can have the same name, this becomes visible with SQL virtual machines that create a VM and and SQL resource with the same name.

# links
- code examples https://github.com/Azure-Samples/azure-samples-python-management/tree/main/samples

# bugs found
- storage_accounts.get_properties() should be .get()
- resource group name should not be optional

# creating requirements
uv export --no-annotate --no-hashes > requirements.txt
