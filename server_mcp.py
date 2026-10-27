from mcp.server import MCPServer
mcp=MCPServer("IT support server")

@mcp.tool()
def check_server(server_name: str) -> str:
    """
    Check the current status of a server
    """ 
    servers = {
        "APP01":"RUNNING",
        "APP02":"STOPPED",
        "DB01":"RUNNING"
    }

    status = servers.get(
        server_name.upper(),
        "SERVER NOT FOUND"
    )

    return f'{server_name}: "status'

@mcp.tool()
def get_incient(incident_id: str) -> str:
    """
    Get information about an IT incident
    """
    incidents = {
        "INC001": {
            "issue":"Application unavailable",
            "priority":"P1",
            "status":"Investigation"
        },
        "INC002": {
            "issue":"High CPU utilization",
            "priorty": "P2",
            "status":"In Proegess"
        },
        "INC003": {
            "issue":"Database connection failure",
            "priority":"P2",
            "status":"Resolved"
        }
    }

    incidents = incidents.get(
        incident_id.upper()
    )

    if incidents is None:
        return "Incident not found"

    return (
        f'Incident:{incident_id}\n'
        f'Issue: {incidents['issue']}\n'
        f'Priority: {incidents['priority']}\n'
        f'Status: {incidents['status']}'
    )

