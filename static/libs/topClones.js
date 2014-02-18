function dominationPlot() {
  var margin = {top: 30, right: 30, bottom: 50, left: 30},
  width = 600,
  height = 300,
  x = d3.scale.linear(),
  y = d3.scale.linear();
  

  function plot(selection) {
    selection.each(function (data) {
    // make the svg
      var svg = selection.selectAll("svg").data([data]);

      svg.enter().append('svg')
      .attr('height', height)
      .attr('width', width);

      var gPlot = svg.append('g')
      .data([d3.map(data).entries()])
      .attr("class", "inner")
      .attr("transform", "translate(" + (margin.left) + "," + (margin.top) + ")");


      // set up x and y scales
      x.domain([0,100]).range([0, width- margin.left -margin.right]);
      y.domain([0,1]).range([height-margin.bottom - margin.top,0 ]);


      // line layout
      var line = d3.svg.line()
      .x(function(d,i) {return x(i)})
      .y(function(d) {return y(d)});

      // draw lines
      var samplePath = gPlot.selectAll('path').data(function(d) { return d});

      samplePath.enter().append('path');

      samplePath
      .attr('class', function (d) {return "cf-" + d.key})
      .attr("fill", "none")
      .attr('d', function(d) {return line(d.value)});

      // draw axes
      var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

      gPlot.append("g")
        .attr("class", "axis xAxis")
        .attr("transform", "translate(0," + (height - margin.top - margin.bottom) + ")")
        .call(xAxis);

      var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

      gPlot.append("g")
        .attr("class", "axis yAxis")
        .attr("transform", "translate("+margin.left+",0)")
        .call(yAxis);

      // add eventbus stuff
      var classToggle = function (s, addOrRemove) {
        var selection= s;
        return function () {
          selection.classed('active', addOrRemove);
        }
      }

      var subscribeActivation = function(selection, key) {
        eventBus.subscribe('activate ' + key, classToggle(selection, true));
        eventBus.subscribe('inactivate ' + key, classToggle(selection, false));
      }

      samplePath.data().forEach(function (d) {
        var cfid = "cf-" + d.key;
        var selection = svg.selectAll('.'+cfid);
        subscribeActivation(selection, cfid);
      });


    });
  }



  plot.eventBus = function (value) {
    if (!arguments.length) return eventBus;
    eventBus = value;
    return plot
  }

  plot.width = function(value) {
    if(!arguments.length) return width;
    width = value;
    return plot;
  }

  return plot;
}
