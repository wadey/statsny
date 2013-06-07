import os

UDP_PORT  = 9026
HTTP_PORT = 8026
TCP_PORT  = 7026

UDP_INTERFACE = "0.0.0.0"
HTTP_INTERFACE = "0.0.0.0"
TCP_INTERFACE = "0.0.0.0"

RESPONSE_CACHE_LENGTH = 50

STATIC_DIR=os.path.realpath(__file__ + "/../../static")

# Machine-specific config
try:
    execfile(os.environ.get("STATSNY_CONFIG", "/etc/statsny/settings.py"))
except IOError:
    pass # No config
