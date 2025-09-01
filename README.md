
# Exporter
Exporter creates a folder structure that mirrors your Azure configuration
Each folder represents a resource group and contains the definitions.


# Getting Started
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

# Learnings
- annoying that storage account does not implement ".get()" to match all other apis
- annoying that sub resources do not take a resource name, instead want you to split the properties for that sub resource (sql databases).

# links
- code examples https://github.com/Azure-Samples/azure-samples-python-management/tree/main/samples
