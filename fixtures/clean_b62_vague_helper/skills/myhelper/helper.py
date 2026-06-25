"""General helper — vague/permissive declaration means B62 must never flag this."""
import socket


def help_out(task):
    """Perform some task — vague helper that uses network."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("example.com", 80))
    s.sendall(b"GET / HTTP/1.0\r\n\r\n")
    s.close()
    return f"done: {task}"
