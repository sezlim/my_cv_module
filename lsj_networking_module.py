import socket

def get_my_ip_address():
    """
    Returns the local IP address of the machine where this function is run.
    """
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Connect to an external server (here, Google's DNS server) to determine the local IP
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "Unable to determine IP"
    return ip
