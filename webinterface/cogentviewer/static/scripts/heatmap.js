// Generated by CoffeeScript 1.7.1
var buckets, colors, doplot, margin;

console.log("Starting Heatmap Script");

margin = {
  top: 100,
  right: 20,
  bottom: 0,
  left: 30
};

buckets = 9;

colors = colorbrewer.RdYlGn[10];

doplot = function() {
  return d3.json("http://127.0.0.1:6543/rest/heatmap/", function(thejson) {
    var bucketwidth, data, datelabels, dates, gridheight, gridsize, gridwidth, heatlabel, heatrows, height, idx, largest, maxval, minval, nodelabels, nodes, range, row, svg, viewport_height, viewport_width, width, _i, _len, _results;
    console.log(thejson);
    nodes = thejson.nodelist;
    dates = thejson.datelist;
    data = thejson.data;
    minval = 0;
    maxval = +thejson.max;
    range = maxval - minval;
    bucketwidth = (range + 1) / buckets;
    console.log("Min ", minval, "Max", maxval);
    console.log("The Range is ", range, "Bucket Width", bucketwidth);
    largest = nodes.length;
    if (dates.length > nodes.length) {
      largest = dates.length;
    }
    console.log("Largest Element ", largest);
    gridsize = Math.floor(height / largest);
    gridheight = 25;
    gridwidth = 25;
    viewport_width = (gridheight * dates.length) + 50;
    viewport_height = (gridheight * nodes.length) + 100;
    width = viewport_width - margin.left - margin.right;
    height = viewport_height - margin.top - margin.bottom;
    console.log("Gridwidth ", gridwidth);
    svg = d3.select("#chart").append("svg").attr("width", viewport_width).attr("height", viewport_height).attr("display", "block").append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    svg.append("svg:rect").attr("x", 0).attr("y", 0).attr("width", width).attr("height", height).attr("fill", '#fff').attr("stroke", '#000');
    nodelabels = svg.selectAll(".nodelabel").data(nodes).enter().append("svg:text").text(function(d) {
      return d;
    }).attr("x", 0).attr("y", function(d, i) {
      return i * gridheight;
    }).style("text-anchor", "end").attr("dx", -6).attr("dy", gridheight / 2);
    datelabels = svg.selectAll(".datelabel").data(dates).enter().append("svg:text").text(function(d) {
      return d;
    }).attr("transform", "rotate(-90)").attr("text-anchor", "start").attr("x", 0).attr("y", function(d, i) {
      return i * gridwidth;
    }).attr("dy", gridwidth / 1.5);
    _results = [];
    for (idx = _i = 0, _len = data.length; _i < _len; idx = ++_i) {
      row = data[idx];
      heatrows = svg.selectAll(".heatrows").data(row).enter().append("svg:rect").attr("width", gridwidth).attr("height", gridheight).attr("fill", function(d) {
        return colors[Math.floor(d / bucketwidth)];
      }).attr("stroke", '#aaa').attr("x", function(d, i) {
        return i * gridwidth;
      }).attr("y", function(d) {
        return idx * gridheight;
      });
      _results.push(heatlabel = svg.selectAll(".heatlabel").data(row).enter().append("svg:text").text(function(d) {
        return d;
      }).attr("x", function(d, i) {
        return i * gridwidth;
      }).attr("y", function(d) {
        return idx * gridheight;
      }).attr("dy", gridheight / 2));
    }
    return _results;
  });
};

doplot();