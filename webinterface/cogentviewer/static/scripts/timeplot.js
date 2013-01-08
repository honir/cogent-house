// Generated by CoffeeScript 1.3.3

require(["dojo/topic", "dojo/io/script"], function(topic, ioscript) {
  var fetchData, plotTS;
  topic.subscribe("navTree", function(arg1) {
    return fetchData(arg1);
  });
  fetchData = function(args) {
    console.log("Fecthing Data with Args ", args);
    args.graphType = "time";
    return ioscript.get({
      url: "jsonFetch",
      content: args,
      callbackParamName: "callback"
    }).then(function(data) {
      console.log("Data Returned ", data);
      plotTS(data);
      console.log("Plotted");
    });
  };
  plotTS = function(theData) {
    var chart, options;
    console.log("Building Time Series ", theData);
    console.log("Title", theData.title);
    console.log("Seires", theData.series);
    options = {
      chart: {
        renderTo: "theGraph"
      },
      title: {
        text: "CHART TITLE"
      },
      legend: {
        enabled: true,
        align: "left",
        layout: "vertical",
        verticalAlign: "top"
      },
      credits: {
        enabled: false
      },
      exporting: {
        width: 1024
      },
      xAxis: {
        type: "datetime"
      },
      rangeSelector: {
        buttons: [
          {
            type: "day",
            count: 1,
            text: "1d"
          }, {
            type: "day",
            count: 3,
            text: "3d"
          }, {
            type: "week",
            count: 1,
            text: "1w"
          }, {
            type: "all",
            text: "All"
          }
        ],
        selected: 2
      }
    };
    options.series = theData.series;
    options.title.text = theData.title;
    console.log("Options ", options);
    chart = new Highcharts.StockChart(options);
    console.log("----> TS DONE", options);
  };
});
