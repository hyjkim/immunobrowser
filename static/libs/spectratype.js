function spectratype() {
  var margin = {top: 20, right: 20, bottom: 60, left: 40},
  width = 600,
  height = 400,
  x = d3.scale.linear(),
  y = d3.scale.linear(),
  eventBus = EventBus.newEventBus();




  function plot(selection) {
    selection.each(function (data) {
      // Scale the axes
      //var minFreq = d3.min(data, function (d) {return d.freq});
      var minFreq = 0;
      var maxFreq = d3.max(data, function (d) {return d.freq});
      var minLength = d3.min(data, function (d) {return d.length});
      var maxLength = d3.max(data, function (d) {return d.length});

      x.domain([minLength, maxLength]).range([margin.left, width-margin.right]);
      y.domain([minFreq, maxFreq]).range([height-margin.bottom, margin.top]);

      // nest the data so plotting a line is possible
      var freqByCfid = d3.nest()
      .key(function(d) {return d.cfid})
      .map(data, d3.map);

      // define the line plotting function
      var line = d3.svg.line()
//      .define(function (d) { return d.length != null; })
      .x(function(d) {return x(d.length)})
      .y(function(d) {return y(d.freq)});

    // insert the svg
      var svg = selection.selectAll("svg").data([data]);
      svg.enter().append('svg')
      .attr('class', 'spectraplot')
      .attr('width', width)
      .attr('height', height);

      var gInner = svg.append('g')
      .attr('class', 'inner')
      .attr('transform','translate('+margin.top+', '+margin.left+')');
      

      // plot the lines
      var samplePath = gInner.selectAll('path').data(freqByCfid.entries());
      samplePath.enter().append('path')
      .attr('class', function (d) {return "cf-" + d.key})
      .classed('spectraplot', true)
      .attr("fill", "none")
      .attr('d', function(d) {return line(d.value)});
      ;

      // plot the circles
      var circles = gInner.selectAll('circle').data(data);
      circles.enter().append('circle')
      .attr('class', function (d) { return 'cf-'+d.cfid })
      .attr('cx', function(d) {return x(d.length)})
      .attr('cy', function(d){return y(d.freq)})
      .attr('r', 5);

      // plot the axes
      var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

      gInner.append("g")
        .attr("class", "axis xAxis")
        .attr("transform", "translate(0," + (d3.max(y.range()) + ")"))
        .call(xAxis);

      var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

      gInner.append("g")
        .attr("class", "axis yAxis")
        .attr("transform", "translate("+margin.left+",0)")
        .call(yAxis);

      // eventBus stuff
      var classToggle = function (s, addOrRemove) {
        var selection= s;
        return function () {
          selection.classed('active', addOrRemove);
        }
      }

      var subscribeActivation = function(selection, key) {
      console.log(key);
        eventBus.subscribe('activate ' + key, classToggle(selection, true));
        eventBus.subscribe('inactivate ' + key, classToggle(selection, false));
      }

      freqByCfid.keys().forEach(function (d) {
        var cfid = "cf-" + d;
        var selection = svg.selectAll('.'+cfid);
        subscribeActivation(selection, cfid);
      });

    });
  }

  plot.width = function (value) {
    if(!arguments.length) return width;
    width = value;
    return plot
  }

  plot.height = function (value) {
    if(!arguments.length) return height;
    height = value;
    return plot
  }

  plot.eventBus = function (value) {
    if (!arguments.length) return eventBus;
    eventBus = value;
    return plot
  }

  return plot;
}
