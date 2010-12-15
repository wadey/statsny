import json

from twisted.internet.protocol import DatagramProtocol
from twisted.web import server
from twisted.application import service, internet

from ostrich import stats
from ostrich.twisted import StatsTimeSeriesResource
from ostrich.histogram import Histogram

import statsny.settings as settings

# Example histogram spacing (1.2 times spacing instead of 1.3)
#Histogram.BUCKET_OFFSETS = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 18, 22, 26, 31, 38, 46, 55, 66, 79, 95, 114, 137, 164, 197, 237, 284, 341, 410, 492, 590, 708, 850, 1020, 1224, 1469, 1763, 2116, 2539, 3047, 3657, 4388, 5266, 6319, 7583, 9100, 10920, 13104, 15725, 18870, 22644, 27173, 32608, 39130, 46956, 56347, 67617, 81140, 97368]
# Good histogram for data that we expect to be under 1 second
Histogram.BUCKET_OFFSETS = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 15000, 30000, 60000, 120000] 

class Collector(DatagramProtocol):
    def datagramReceived(self, data, (host, port)):
        # print "received %r from %s:%d" % (data, host, port)
        data = json.loads(data)
        endpoint = data['endpoint']
        method = data['method']
        code = data['code']
        endpoint_method = "%s:%s" % (method, endpoint)

        stats.incr(endpoint_method)
        stats.incr("%s:%s:%s" % (method, (code / 100), endpoint))
        stats.add_timing(endpoint_method, data['elapsed'])
        for k, v in data['stats'].items():
            stats.add_timing("stats:%s" % k, v)

application = service.Application("Statsny")
site = server.Site(StatsTimeSeriesResource())
internet.TCPServer(settings.HTTP_PORT, site).setServiceParent(application)
internet.UDPServer(settings.UDP_PORT, Collector()).setServiceParent(application)
