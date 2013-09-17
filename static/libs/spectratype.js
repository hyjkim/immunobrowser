function spectratype() {
  var margin = {top: 20, right: 20, bottom: 60, left: 20},
  width = 600,
  height = 400,
  x = d3.scale.linear(),
  y = d3.scale.linear();



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
      
      var samplePath = gInner.selectAll('path').data(freqByCfid.entries());
      samplePath.enter().append('path')
      .attr('class', function (d) {return "cf-" + d.key})
      .attr("fill", "none")
      .attr('d', function(d) {return line(d.value)});
      ;



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

  return plot;
}
