import socket

def get_hostname():
    hostname = socket.gethostname()
    return hostname

def main():
    hostname = get_hostname()
    print("Hostname:", hostname)

if __name__ == "__main__":
    main()