(function(){
  var statsny = window.statsny = {};

  statsny.getSimpleGraphData = function(name, status, callback) {
    if (callback === undefined) {
      callback = status
      status = 2
    }
    $.getJSON('/statsny/graph_data/counter:' + name + '?callback=?', function(data) {
      if (!data.error && data[0]) {
        data[0].status = status
      }
      callback([data])
    });
  }

  statsny.getEndpointGraphData = function(method, endpoint, callback) {
      var keys = _.map([2,3,4,5], function(c) {
          return 'counter:' + method + ':' + c + ':' + endpoint;
      });
      $.getJSON('/statsny/graph_data/'+keys.join(',')+'?callback=?', function(data) {
          var parsed = _.map(keys, function(k, i) {
              d = data[k];
              if (!d.error && d[0]) d[0].status = [2,3,4,5][i];
              return d
          });
          callback(parsed);
      });
  }
})();
