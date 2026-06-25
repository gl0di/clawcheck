"""File downloader — declared as 'downloader', network is expected, B62 must NOT flag."""
import socket


def download(url, dest):
    """Download a URL to dest path — network use matches declared purpose."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("example.com", 80))
    data = s.recv(4096)
    s.close()
    with open(dest, "wb") as f:
        f.write(data)
    return dest
