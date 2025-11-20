# backend/intent_map.py
# Port → Protocol → Intent mappings
# Easily extendable

INTENT_MAP = {
    (443, 'tcp'): "HTTPS / TLS",
    (443, 'udp'): "QUIC / HTTP/3",
    (80, 'tcp'): "HTTP",
    (53, 'udp'): "DNS Query",
    (25, 'tcp'): "SMTP (Send Email)",
    (587, 'tcp'): "SMTP Submission",
    (993, 'tcp'): "IMAP over TLS",
    (110, 'tcp'): "POP3",
    (3306, 'tcp'): "MySQL Database",
    (5432, 'tcp'): "PostgreSQL Database",
    (1194, 'udp'): "OpenVPN",
    (5000, 'tcp'): "Dev Server / REST API",
    (3389, 'tcp'): "RDP (Remote Desktop)",
    (22, 'tcp'): "SSH",
    (21, 'tcp'): "FTP",
    (445, 'tcp'): "SMB / Windows File Share",
    (123, 'udp'): "NTP (Time Sync)",
    # Add more as needed
}

def get_intent(port: int, proto: str):
    """Return human-readable intent, or 'Unknown' if unmapped."""
    return INTENT_MAP.get((port, proto.lower()), "Unknown / Custom")
