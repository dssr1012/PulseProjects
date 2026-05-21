#!/usr/bin/env python3
"""
Huawei Cloud MCP Server for Hermes Agent
Provides infrastructure management tools via Model Context Protocol.

Resources managed:
- ECS (Elastic Cloud Server) instances
- RDS (Relational Database Service) instances  
- VPC (Virtual Private Cloud) & Subnets
- EIP (Elastic IP) addresses
- OBS (Object Storage Service) buckets
- KMS (Key Management Service) keys
- Security Groups & Rules

Uses Huawei Cloud Python SDK (huaweicloudsdkpython)
"""

import json
import os
import sys
from typing import Any, Sequence

# MCP SDK
from mcp.server import Server
from mcp.types import Tool, TextContent

# Huawei Cloud SDK
try:
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkecs.v2 import EcsClient
    from huaweicloudsdkvpc.v2 import VpcClient
    from huaweicloudsdkeip.v2 import EipClient
    from huaweicloudsdkrds.v3 import RdsClient
    from huaweicloudsdkobs.v1 import ObsClient
    HAS_SDK = True
except ImportError:
    HAS_SDK = False

app = Server("huawei-cloud-mcp")

# Configuration from environment
REGION = os.environ.get("HW_REGION", "la-south-2")
PROJECT_ID = os.environ.get("HW_PROJECT_ID", "")
AK = os.environ.get("HW_ACCESS_KEY", "")
SK = os.environ.get("HW_SECRET_KEY", "")


def get_credentials():
    """Build Huawei Cloud credentials from env vars."""
    if not AK or not SK:
        return None
    creds = BasicCredentials(ak=AK, sk=SK)
    if PROJECT_ID:
        creds.project_id = PROJECT_ID
    return creds


# ─── Tool Definitions ───────────────────────────────────────────────────────

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_ecs_instances",
            description="List all ECS instances in the region with their status, flavor, and IPs",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_rds_instances", 
            description="List all RDS database instances with status and connection info",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_vpcs",
            description="List all VPCs and their subnets in the region",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_eips",
            description="List all Elastic IPs with their status and associated resources",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_security_groups",
            description="List all security groups and their rules",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="ecs_action",
            description="Start or stop an ECS instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_id": {"type": "string", "description": "ECS instance ID"},
                    "action": {"type": "string", "enum": ["start", "stop", "reboot"], "description": "Action to perform"},
                },
                "required": ["instance_id", "action"],
            },
        ),
        Tool(
            name="get_infrastructure_summary",
            description="Get a summary of all Huawei Cloud infrastructure resources and their status",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ─── Tool Handlers ──────────────────────────────────────────────────────────

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if not HAS_SDK:
        return [TextContent(type="text", text="Error: Huawei Cloud SDK not installed. Run: pip install huaweicloudsdkpython")]
    
    creds = get_credentials()
    if not creds:
        return [TextContent(type="text", text="Error: HW_ACCESS_KEY and HW_SECRET_KEY not set in environment")]
    
    try:
        if name == "list_ecs_instances":
            return await _list_ecs(creds)
        elif name == "list_rds_instances":
            return await _list_rds(creds)
        elif name == "list_vpcs":
            return await _list_vpcs(creds)
        elif name == "list_eips":
            return await _list_eips(creds)
        elif name == "list_security_groups":
            return await _list_sgs(creds)
        elif name == "ecs_action":
            return await _ecs_action(creds, arguments)
        elif name == "get_infrastructure_summary":
            return await _infra_summary(creds)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]


async def _list_ecs(creds) -> list[TextContent]:
    from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
    from huaweicloudsdkecs.v2.model.list_servers_details_request import ListServersDetailsRequest
    
    client = EcsClient.new_builder().with_credentials(creds).with_region(EcsRegion.value_of(REGION)).build()
    req = ListServersDetailsRequest()
    resp = client.list_servers_details(req)
    
    instances = []
    for server in resp.servers:
        instances.append({
            "id": server.id,
            "name": server.name,
            "status": server.status,
            "flavor": server.flavor.id if server.flavor else "N/A",
            "public_ip": server.metadata.get("public_ip", "N/A") if server.metadata else "N/A",
        })
    
    return [TextContent(type="text", text=json.dumps(instances, indent=2))]


async def _list_rds(creds) -> list[TextContent]:
    from huaweicloudsdkrds.v3.region.rds_region import RdsRegion
    from huaweicloudsdkrds.v3.model.list_instances_request import ListInstancesRequest
    
    client = RdsClient.new_builder().with_credentials(creds).with_region(RdsRegion.value_of(REGION)).build()
    req = ListInstancesRequest()
    resp = client.list_instances(req)
    
    instances = []
    for db in resp.instances:
        instances.append({
            "id": db.id,
            "name": db.name,
            "status": db.status,
            "engine": f"{db.datastore.type} {db.datastore.version}" if db.datastore else "N/A",
            "flavor": db.flavor_ref if hasattr(db, 'flavor_ref') else "N/A",
        })
    
    return [TextContent(type="text", text=json.dumps(instances, indent=2))]


async def _list_vpcs(creds) -> list[TextContent]:
    from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
    from huaweicloudsdkvpc.v2.model.list_vpcs_request import ListVpcsRequest
    
    client = VpcClient.new_builder().with_credentials(creds).with_region(VpcRegion.value_of(REGION)).build()
    req = ListVpcsRequest()
    resp = client.list_vpcs(req)
    
    vpcs = [{"id": v.id, "name": v.name, "cidr": v.cidr, "status": v.status} for v in resp.vpcs]
    return [TextContent(type="text", text=json.dumps(vpcs, indent=2))]


async def _list_eips(creds) -> list[TextContent]:
    from huaweicloudsdkeip.v2.region.eip_region import EipRegion
    from huaweicloudsdkeip.v2.model.list_publicips_request import ListPublicipsRequest
    
    client = EipClient.new_builder().with_credentials(creds).with_region(EipRegion.value_of(REGION)).build()
    req = ListPublicipsRequest()
    resp = client.list_publicips(req)
    
    eips = [{"id": e.id, "ip": e.public_ip_address, "status": e.status, "type": e.type} for e in resp.publicips]
    return [TextContent(type="text", text=json.dumps(eips, indent=2))]


async def _list_sgs(creds) -> list[TextContent]:
    from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
    from huaweicloudsdkvpc.v2.model.list_security_groups_request import ListSecurityGroupsRequest
    
    client = VpcClient.new_builder().with_credentials(creds).with_region(VpcRegion.value_of(REGION)).build()
    req = ListSecurityGroupsRequest()
    resp = client.list_security_groups(req)
    
    sgs = [{"id": s.id, "name": s.name, "description": s.description} for s in resp.security_groups]
    return [TextContent(type="text", text=json.dumps(sgs, indent=2))]


async def _ecs_action(creds, args) -> list[TextContent]:
    from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
    
    instance_id = args["instance_id"]
    action = args["action"]
    
    client = EcsClient.new_builder().with_credentials(creds).with_region(EcsRegion.value_of(REGION)).build()
    
    if action == "start":
        from huaweicloudsdkecs.v2.model.batch_start_servers_request import BatchStartServersRequest
        from huaweicloudsdkecs.v2.model.server_id import ServerId
        req = BatchStartServersRequest(os_start_body={"servers": [ServerId(id=instance_id)]})
        resp = client.batch_start_servers(req)
    elif action == "stop":
        from huaweicloudsdkecs.v2.model.batch_stop_servers_request import BatchStopServersRequest
        from huaweicloudsdkecs.v2.model.server_id import ServerId
        req = BatchStopServersRequest(os_stop_body={"servers": [ServerId(id=instance_id)]})
        resp = client.batch_stop_servers(req)
    elif action == "reboot":
        from huaweicloudsdkecs.v2.model.batch_reboot_servers_request import BatchRebootServersRequest
        from huaweicloudsdkecs.v2.model.server_id import ServerId
        req = BatchRebootServersRequest(reboot_body={"servers": [ServerId(id=instance_id)]})
        resp = client.batch_reboot_servers(req)
    
    return [TextContent(type="text", text=f"ECS {action} initiated for {instance_id}")]


async def _infra_summary(creds) -> list[TextContent]:
    """Get a comprehensive infrastructure summary."""
    summary = {"region": REGION, "project_id": PROJECT_ID, "resources": {}}
    
    # ECS
    try:
        ecs_result = await _list_ecs(creds)
        summary["resources"]["ecs"] = json.loads(ecs_result[0].text)
    except:
        summary["resources"]["ecs"] = "error"
    
    # VPCs
    try:
        vpc_result = await _list_vpcs(creds)
        summary["resources"]["vpcs"] = json.loads(vpc_result[0].text)
    except:
        summary["resources"]["vpcs"] = "error"
    
    # EIPs
    try:
        eip_result = await _list_eips(creds)
        summary["resources"]["eips"] = json.loads(eip_result[0].text)
    except:
        summary["resources"]["eips"] = "error"
    
    return [TextContent(type="text", text=json.dumps(summary, indent=2))]


# ─── Entry Point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    
    import asyncio
    asyncio.run(main())
