import json

from twisted.internet.protocol import DatagramProtocol
from twisted.web import server
from twisted.application import service, internet

from ostrich import stats
from ostrich.twisted import StatsTimeSeriesResource
from ostrich.histogram import Histogram

# Substitute a more granular histogram (1.2 times spacing instead of 1.3)
# TODO pick bucket sizes that make more sense for the graphs?
Histogram.BUCKET_OFFSET = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 18, 22, 26, 31, 38, 46, 55, 66, 79, 95, 114, 137, 164, 197, 237, 284, 341, 410, 492, 590, 708, 850, 1020, 1224, 1469, 1763, 2116, 2539, 3047, 3657, 4388, 5266, 6319, 7583, 9100, 10920, 13104, 15725, 18870, 22644, 27173, 32608, 39130, 46956, 56347, 67617, 81140, 97368]

class Collector(DatagramProtocol):
    def datagramReceived(self, data, (host, port)):
        # print "received %r from %s:%d" % (data, host, port)
        data = json.loads(data)
        endpoint = data['endpoint']
        stats.incr(endpoint)
        stats.incr("%s:%s" % ((data['code'] / 100), endpoint))
        stats.add_timing(endpoint, data['elapsed'])
        for k, v in data['stats'].items():
            stats.add_timing(k, v)

application = service.Application("Statsny")
site = server.Site(StatsTimeSeriesResource())
internet.TCPServer(8026, site).setServiceParent(application)
internet.UDPServer(9026, Collector()).setServiceParent(application)
