# Huawei Cloud MCP Server

## Overview
Model Context Protocol server for Huawei Cloud infrastructure management.
Provides tools for managing ECS, RDS, VPC, EIP, OBS, and Security Group resources.

## Tools Provided
| Tool | Description |
|------|-------------|
| `list_ecs_instances` | List all ECS instances with status, flavor, IPs |
| `list_rds_instances` | List all RDS database instances |
| `list_vpcs` | List all VPCs and subnets |
| `list_eips` | List all Elastic IPs |
| `list_security_groups` | List security groups and rules |
| `ecs_action` | Start/stop/reboot an ECS instance |
| `get_infrastructure_summary` | Comprehensive resource summary |

## Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `HW_ACCESS_KEY` | Yes | Huawei Cloud AK |
| `HW_SECRET_KEY` | Yes | Huawei Cloud SK |
| `HW_REGION` | No | Region (default: la-south-2) |
| `HW_PROJECT_ID` | No | Enterprise project ID |

## Usage
Configured in `~/.hermes/config.yaml` under `mcp_servers.huawei-cloud`.

## Dependencies
- `huaweicloudsdkcore` >= 3.1
- `huaweicloudsdkecs` >= 3.1
- `huaweicloudsdkvpc` >= 3.1
- `huaweicloudsdkeip` >= 3.1
- `huaweicloudsdkrds` >= 3.1
- `mcp` >= 1.0
