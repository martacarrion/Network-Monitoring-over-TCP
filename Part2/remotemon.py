
import argparse
import socket
import os
import sys

# Add Part1 folder to Python search path
part1_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Part1")
)
# os.path.dirname(__file__) obtiene la carpeta donde está remotemon.py
# os.path.join(..., "..", "Part1") localiza la carpeta Part1
# sys.path.append()
  
sys.path.append(part1_path)

import localmon

def run_server(args):

    # 1. Create a server socket
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Bind the socket to the selected port
    socketAddr = ("", args.p)
    serverSock.bind(socketAddr)

    # 3. Listen for client connections
    serverSock.listen(1)

    print("Server listening on port:", args.p)

    while True:
        # 4. Accept a client connection
        print("Waiting for client to connect...")
        connectSock, addr = serverSock.accept()

        print("Client connected:", addr)

                # 5. Receive request from the client
        request = connectSock.recv(1024)

        print("Received request:", request.decode("UTF-8"))

        # 6. Collect network information
        network_data = collect_network_data()

        if network_data is not None:
            print("Network information collected successfully.")
            print("Hostname:", network_data["hostname"])

        # 7. Close the connection
        connectSock.close()

def run_client(args):

    # 1. Create a client socket
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Connect to the server
    serverAddr = (args.ip, args.p)
    clientSock.connect(serverAddr)

    print("Connected to server:", serverAddr)

    # 3. Send a message to the server
    message = "Hello from client"
    clientSock.sendall(message.encode("UTF-8"))

    # 4. Receive the server response
    data = clientSock.recv(1024)

    print("Received from server:", data.decode("UTF-8"))

    # 5. Close the connection
    clientSock.close()

def collect_network_data():

    # Get hostname
    hostname = localmon.get_hostname()

    # Get network interfaces
    interfaces = localmon.get_interfaces()

    # Get network routes
    routes = localmon.get_routes()

    # Check if information was collected successfully
    if interfaces is None or routes is None:
        print("Error: network information could not be collected.")
        return None

    # Store all information in a dictionary
    data = {
        "hostname": hostname,
        "interfaces": interfaces,
        "routes": routes
    }

    return data


def main():
    parser = argparse.ArgumentParser(
        description="Remote Network Monitoring Tool"
    )

    # Select application mode
    mode = parser.add_mutually_exclusive_group(required=True) #significa que las opciones del grupo son incompatibles y require=True significa que debemos seleccionar obligatoriamente una. 

    mode.add_argument(
        "-r",
        action="store_true",
        help="Run in server mode"
    )

    mode.add_argument(
        "-t",
        action="store_true",
        help="Run in client mode"
    )

    # Configure TCP port
    parser.add_argument(
        "-p",
        type=int,
        default=7777,
        help="TCP port (default: 7777)"
    )

    # Configure server IP address
    parser.add_argument(
        "-ip",
        default="127.0.0.1",
        help="Server IP address (default: 127.0.0.1)"
    )

    args = parser.parse_args()#analiza los argumentos que hemos escrito al ejecutar el programa y los almacena en el objeto args

    if args.r:
        run_server(args)

    elif args.t:
        run_client(args)

    data = collect_network_data()
    print(data)


if __name__ == "__main__":
    main()
