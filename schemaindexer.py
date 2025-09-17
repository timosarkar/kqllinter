"""
this script indexes all table schemas alongside datatypes in sentinel and defender xdr advanced hunting to inject into the okayql linter
"""
# python3 -m pip install azure-identity azure-monitor-query --break-system-packages
# curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# az login --use-device-code
from azure.identity import AzureCliCredential
from azure.monitor.query import LogsQueryClient
from datetime import timedelta
from dotenv import load_dotenv

import json
import os

load_dotenv()

credential = AzureCliCredential()
client = LogsQueryClient(credential)
workspace_id = os.getenv("SENTINEL_WORKSPACE_ID")

"""
to get all tablenames you must extract them in your sentinel and defender advanced hunting workspace
using the following KQL query:

let tableList =
search *
| where TimeGenerated >= ago(3d)
| summarize by TableName = $table
| project TableName;
let tableNames = materialize(tableList);
tableNames

then you must add them to table_names as seen below
"""

table_names = ["SigninLogs", "SecurityEvent", "CommonSecurityLog"]  # Replace with your actual list

schemas = {}

for table in table_names:
    query = f"{table} | getschema"
    response = client.query_workspace(workspace_id, query, timespan=timedelta(days=1))
    columns = response.tables[0].rows
    schema = [{"name": col[0], "type": col[3]} for col in columns]
    schemas[table] = schema

    for field in schema:
        print(f"  {field['name']} ({field['type']})")

with open("kql_tableschemas.json", "w") as f:
    json.dump(schemas, f, indent=2)
