import os

UDP_PORT  = 9026
HTTP_PORT = 8026

# Machine-specific config
try:
    execfile(os.environ.get("STATSNY_CONFIG", "/etc/statsny/settings.py"))
except IOError:
    pass # No config
