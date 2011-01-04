import json

from twisted.internet.protocol import DatagramProtocol
from twisted.web import server
from twisted.application import service, internet

from ostrich import stats
from ostrich.timing import TimingStat
from ostrich.twisted import StatsTimeSeriesResource
from ostrich.histogram import Histogram

import statsny.settings as settings

# Example histogram spacing (1.2 times spacing instead of 1.3)
#Histogram.BUCKET_OFFSETS = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 18, 22, 26, 31, 38, 46, 55, 66, 79, 95, 114, 137, 164, 197, 237, 284, 341, 410, 492, 590, 708, 850, 1020, 1224, 1469, 1763, 2116, 2539, 3047, 3657, 4388, 5266, 6319, 7583, 9100, 10920, 13104, 15725, 18870, 22644, 27173, 32608, 39130, 46956, 56347, 67617, 81140, 97368]
# Good histogram for data that we expect to be under 1 second
Histogram.BUCKET_OFFSETS = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 121, 141, 161, 181, 201, 221, 241, 261, 281, 301, 321, 341, 361, 381, 401, 421, 441, 461, 481, 501, 551, 601, 651, 701, 751, 801, 851, 901, 951, 1001, 1251, 1501, 1751, 2001, 2251, 2501, 2751, 3001, 3501, 4001, 4501, 5001, 5501, 6001, 7001, 8001, 9001, 10001, 11001, 12001, 15001, 30001, 60001, 120001, 240001, 480001, 3600001] 

class Collector(DatagramProtocol):
    def datagramReceived(self, data, (host, port)):
        data = json.loads(data)
        if data.has_key('batch'):
            self.add_stats(data['batch'])
        else:
            self.add_request_stats(data)

    def add_stats(self, data):
        for k, v in data['timings'].iteritems():
            if v['count'] > 0:
                stats.add_timing(TimingStat.from_raw_dict(v))
        for k, v in data['counters'].iteritems():
            if v > 0:
                stats.incr(k, v)

    def add_request_stats(self, data):
        # print "received %r from %s:%d" % (data, host, port)
        endpoint = data['endpoint']
        method = data['method']
        code = data['code']
        simple_code = str(code / 100)
        endpoint_method = "%s:%s" % (method, endpoint)

        stats.incr(simple_code)
        stats.incr(endpoint_method)
        stats.incr("%s:%s" % (method, simple_code))
        stats.incr("%s:%s:%s" % (method, simple_code, endpoint))
        stats.add_timing(endpoint_method, data['elapsed'])
        for k, v in data['stats'].items():
            stats.add_timing("stats:%s" % k, v)

application = service.Application("Statsny")
site = server.Site(StatsTimeSeriesResource())
internet.TCPServer(settings.HTTP_PORT, site).setServiceParent(application)
internet.UDPServer(settings.UDP_PORT, Collector()).setServiceParent(application)
