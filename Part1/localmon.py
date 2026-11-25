
import socket
import subprocess
import json


def get_hostname():
    hostname = socket.gethostname()
    return hostname


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.stdout == "":
            print("Error: empty command output.")
            return None

        data = json.loads(result.stdout)

        return data

    except FileNotFoundError:
        print("Error: command not found.")
        return None

    except json.JSONDecodeError:
        print("Error: invalid JSON output.")
        return None


def get_interfaces():
    link_data = run_command(["ip", "-json", "link", "show"])
    address_data = run_command(["ip", "-json", "address", "show"])
    if link_data is None or address_data is None:
        return None

    interfaces = []

    for interface in link_data:
        name = interface["ifname"]
        ip_addresses = []

        for address_interface in address_data:
            if address_interface["ifname"] == name:

                for address in address_interface["addr_info"]:
                    ip_addresses.append({
                        "family": address["family"],
                        "address": address["local"],
                        "prefix_length": address["prefixlen"]
                    })

        interfaces.append({
            "name": name,
            "mtu": interface["mtu"],
            "mac_address": interface["address"],
            "flags": interface["flags"],
            "state": interface["operstate"],
            "ip_addresses": ip_addresses
        })
    

    return interfaces

def get_routes():
    route_data = run_command(["ip", "-json", "route", "show"])
    if route_data is None:
        return None

    routes = []

    for route in route_data:
        routes.append({
            "destination": route["dst"],
            "gateway": route.get("gateway"),
            "interface": route["dev"],
            "protocol": route["protocol"]
        })

    return routes


def display_data(data):
    print("\nLOCAL NETWORK INFORMATION")
    print("-------------------------")

    print("Hostname:", data["hostname"])

    print("\nNETWORK INTERFACES:")

    for interface in data["interfaces"]:
        print("\nInterface:", interface["name"])
        print("MTU:", interface["mtu"])
        print("MAC:", interface["mac_address"])
        print("Flags:", interface["flags"])
        print("State:", interface["state"])
        print("IP addresses:", interface["ip_addresses"])

    print("\nNETWORK ROUTES:")

    for route in data["routes"]:
        print("Destination:", route["destination"])
        print("Gateway:", route["gateway"])
        print("Interface:", route["interface"])


def save_json(data):
    file = open("local_network.json", "w")
    json.dump(data, file, indent=4)
    file.close()

    print("\nNetwork information saved to local_network.json")

def main():
    hostname = get_hostname()
    interfaces = get_interfaces()
    routes = get_routes()

    if interfaces is None or routes is None:
        print("Error: network information could not be collected.")
        return

    data = {
        "hostname": hostname,
        "interfaces": interfaces,
        "routes": routes
    }

    display_data(data)
    save_json(data)


if __name__ == "__main__":
    main()

