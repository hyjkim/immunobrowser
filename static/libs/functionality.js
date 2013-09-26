function functionality2() {
  var margin = {top: 30, right: 10, bottom: 10, left: 10},
  width = 800,
  height,
  heightScale = 40,
  plotWidth = 400,
  labelWidth = 200,
  legendHeightScale= 20,
  xAxisHeight = 60,
  tooltip,
  colorScale = d3.scale.ordinal(),
  nameMap = function(d) {return d},
  eventBus = EventBus.newEventBus();

  function plot (selection) {
    if (typeof tooltip ==='undefined') {
      tooltip = selection
      .append("div")
      .style("visibility", "hidden")
      .style("z-index", "10")
      .style("position", "absolute")
      .style("background", "white")
      .attr("class", "functionality-tooltip")
      ;
    }

    selection.each (function (data) {
      // Get sample IDs
      var sampleIds = data.map(function (d) {return d.key});

      // get set of productivity statuses
      var prodStatuses = d3.set([].concat.apply([],data.map(function (d) {
        return d3.map(d.values).keys();
      }))).values();
      var legendHeight = prodStatuses.length * legendHeightScale;
      var legendScale = d3.scale.ordinal().domain(prodStatuses).rangeRoundBands([0,legendHeight]);

      // Set height based on data 
      height = sampleIds.length * heightScale + margin.bottom + margin.top + legendHeight + xAxisHeight;

      // Make svg and set some attributes

      var svg = d3.select(this).selectAll("svg").data(d3.select(this).data());

      svg.enter().append("svg");
      svg.attr("width", width)
      .attr("height", height);

      var gPlot = svg.append('g')
      .attr("class", "inner")
      .attr("transform", 'translate(' + (margin.left + labelWidth) + ',' + (margin.top) +')');


      // draw legend with set of productivity statuses




      // map data such that each productivity status has a sample id and a
      // percentage
      var dataMap = prodStatuses.map(
        function(prodStatus) {
          return {
            'key': prodStatus,
            'values': data.map(
              function (d) {
                var y;
                (prodStatus in d.values) ? y = d.values[prodStatus]: y = 0;

                return {
                  'x': d.key,
                  'y': y
                };
              })
          };
        });



        var y = d3.scale.ordinal()
        .domain(sampleIds)
        .rangeRoundBands([0, height - margin.top - margin.bottom - legendHeight - xAxisHeight], 0.1);
        //.rangeRoundBands([0, width - margin.left - margin.right]);

        var x = d3.scale.linear()
        .domain([0,1])
        .range([plotWidth - margin.left - margin.right, 0]);
        //.range([height - margin.top - margin.bottom, 0], 0.1);

        var color = d3.scale.category10();

        var stackMax = 1;
        var stack = d3.layout.stack()
        .values(function (d) { return d.values })
        ;


        var layers = gPlot.selectAll('.layer')
        .data(stack(dataMap))
        .enter()
        .append('g')
        .attr('class', function (d) {return 'layer ' + d.key})
        .style("fill", function(d,i) { return color(i); });

        var rects = layers.selectAll('rect')
        .data(function (d) {return d.values})
        .enter()
        .append('rect')
        .attr('x', function(d) {return x(d.y0 + d.y)})
        .attr("y", function(d) { return y(d.x); })
        .attr('height', y.rangeBand())
        .attr('width', function(d) { return x(d.y0) - x(d.y0 + d.y); })

        // draw an y axis
        var gAxis = svg.append("g").attr('class', 'axis');

        var yAxis = d3.svg.axis()
        .scale(y)
        .tickSize(0)
        .tickPadding(0)
        .orient('left');

        var gYAxis = gAxis.append('g')
        .attr('class', 'y axis')
        .attr('transform', 'translate('+(margin.left+labelWidth)+','+margin.top+')')
        .call(yAxis);

        // add y axis title
        gYAxis.append('text')
        .attr('class', 'title')
        .text('Sample Names')
        .attr('text-anchor', 'end');

        // Convert the sample id to sample names
        gAxis.selectAll('g .axis .tick text')
        .text(function (d) {
          return nameMap(d);
        })
        ;
        
        // draw on x axis
        var xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom');

        var gXAxis =gAxis.append('g')
        .attr('class', 'x axis')
        .call(xAxis)
        .attr('transform', 'translate('+(margin.left+labelWidth)+','+(height-legendHeight - xAxisHeight)+')');

        // draw x axis lable
        gXAxis.append('text')
        .attr('class', 'title')
        .attr('x', 0)
        .attr('y', 40)
        .text('Fraction of all reads');

        // draw the legend
        var gLegend = svg.append('g').attr('class', 'legend')
        .attr('transform', 'translate('+(margin.left + labelWidth)+','+ (margin.top + heightScale * sampleIds.length+xAxisHeight) + ')');

        var legendBoxes = gLegend.selectAll('rect').data(prodStatuses)
        .enter()
        .append('rect')
        .attr('height', 10)
        .attr('width', 10)
        .attr('x', 0)
        .attr('y', function(d) {return legendScale(d)})
        .style('fill', function(d,i) {return color(i)});

        var legendText = gLegend.selectAll('text').data(prodStatuses)
        .enter()
        .append('text')
        .attr('x', 20)
        .attr('y', function(d) {return legendScale(d)+10})
        .text(function(d) {return d});
        

    });
  }

  // public accessors
  plot.x = function(value) {
    if (!arguments.length) return xScale;
    xScale = value;
    return plot;
  }

  plot.colors = function(value) {
    if (!arguments.length) return colorScale;
    colorScale = value;
    return plot;
  }

  plot.sampleName = function(value) {
    if(!arguments.length) return nameMap;
    nameMap = value;
    return plot;
  }

  plot.eventBus = function(value) {
    if(!arguments.length) return eventBus;
    eventBus = value;
    return plot;
  }


  return plot;
}


