function scatterNav2() {
  var margin = {top: 30, right: 30, bottom: 30, left: 60},
  scatterMargin = {top: 0, right: 30, bottom: 90, left: 30},
  width = 700,
  height = 500,
  histHeight = 100,
  nameMap = function(d) {return d[3]},
  tooltip,
  eventBus = EventBus.newEventBus(),
  rScale = d3.scale.linear(),
  vScale = d3.scale.ordinal(),
  jScale = d3.scale.ordinal(),
  cfids;

  var plot = function(selection) {
    if (typeof tooltip ==='undefined') {
      tooltip = selection
      .append("div")
      .style("visibility", "hidden")
      .style("z-index", "10")
      .style("position", "absolute")
      .style("background", "white")
      .attr("class", "scatter-tooltip")
      ;
    }

    selection.each(function(data) {
      // set the scales
      vScale
      .rangePoints([0, width - histHeight - margin.left - margin.right]);
      jScale
      .rangePoints([height - histHeight - margin.top - scatterMargin.bottom, 0]);
      // format the data
      var nestedData = d3.nest()
      .key(function(d) {return d[3]})
      .key(function(d) {return d[0]})
      .sortKeys(d3.ascending)
      .entries(data);

      cfids = nestedData.map(function(d) {return d.key});

      // add the svg and create it if it doesn't exist
      var svg = d3.select(this).selectAll("svg#scatter").data([nestedData]);
      svg.enter().append("svg");
      svg.attr("width", width)
      .attr("height", height)
      .attr("id", "scatter");

      // Draw the circles
      var gScatter = svg.append("g").attr("class", "scatter")
      .attr("transform","translate(" + (margin.left ) + "," + (margin.top + histHeight) +")")
      .datum(nestedData);
      scatter(gScatter);

      // Draw tooltips for frequency circles
      circleTooltips(gScatter, data);

      // draw v and j Hists
      var jHistInner = svg.append("g").attr("class", "j-hist")
      .attr("transform", "translate("+(width-histHeight)+","+ (margin.top + histHeight) +")")
      .datum(data);

      var vHistInner = svg.append("g").attr("class", "v-hist")
      .attr("transform",  "translate(" + (margin.left ) + ","+margin.top+")")
      .datum(data);


      // highlight circles when y-axis tick labels are highlighted
      selection.selectAll("g.yAxis g.tick")
      .each(function () {
        var label = d3.select(this);
        var thisData = d3.select(this).datum();
        var circles = selection.selectAll("circle")
        .filter(function(d) {return d[1] == thisData});
        label.on("mouseover", function () {
          label.style("font-weight", "bold");
          circles.classed("active", true);
          var filteredTestData = data.filter(function (d) {
            return d[1] == thisData;
          });

          vHistInner.datum(filteredTestData).call(vHist);
        })
        .on("mouseout", function () {
          label.style("font-weight", null);
          circles.classed("active", false);
          vHistInner.datum(data).call(vHist);
        });
      });

      // Do the same for X
      selection.selectAll("g.xAxis g.tick")
      .each(function () {
        var label = d3.select(this);
        var thisData = d3.select(this).datum();
        var circles = selection.selectAll("circle")
        .filter(function(d) {return d[0] == thisData});
        label.on("mouseover", function () {
          label.style("font-weight", "bold");
          circles.classed("active", true);
          var filteredTestData = data.filter(function (d) {
            return d[0] == thisData;
          });

          jHistInner.datum(filteredTestData).call(jHist);
        })
        .on("mouseout", function () {
          label.style("font-weight", null);
          circles.classed("active", false);
          jHistInner.datum(data).call(jHist);
        });
      });


      jHistInner.call(jHist);
      vHistInner.call(vHist);

    cfids.forEach(function (cfid) {
      cfelements = selection.selectAll('.cf-'+cfid)
      eventBus.subscribe('activate cf-'+cfid, classToggle(cfelements, true));
      eventBus.subscribe('inactivate cf-'+cfid, classToggle(cfelements, false));
    });


    });
  };

  var classToggle = function (selection, addOrRemove) {
    var cfelements = selection;
    return function () {
      cfelements.classed('active', addOrRemove);
    }
  }

  var scatter = function(selection){
    var sampleRows = selection.selectAll("g")
    //.data(function(d) {return d.key})
    .data(function(d) {return d})
    .enter()
    .append("g")
    .attr("class", function(d) {
      return "cf-"+d.key
    });
    var vRows = sampleRows.selectAll("g")
    .data(function(d) {return d.values}, function(d) {return d.key})
    .enter()
    .append("g")
    .attr("class", function(d) {return "v-"+d.key});
    sampleCircles = vRows.selectAll("circle")
    .data(function(d) {return d.values}, 
    function(d) {return d[1]})
    .enter()
    .append("circle")
    .attr("cx", V)
    .attr("cy", J)
    .attr("r", R)
    //      .attr("fill", Color)
    .attr("class", function(d) {return "cf-"+d[3].toString()})
    .classed('inactive', true);

    // Draw the axes
    // set up axes and labels
    var xAxis = d3.svg.axis()
    .scale(vScale)
    .orient("bottom")
    .ticks(vScale.range().length)
    .tickSize(-(height-margin.top-scatterMargin.bottom-histHeight),0,0);

    selection.append("g")
    .attr("class", "axis xAxis")
    .attr("transform", "translate(0," + (d3.max(jScale.range()))+ ")")
    .call(xAxis)
    .selectAll("text")  
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", ".15em")
    .attr("transform", function(d) {
      return "rotate(-65)" 
    });

    var yAxis = d3.svg.axis()
    .scale(jScale)
    .orient("left")
    .ticks(jScale.range().length)
    .tickSize(-(width-histHeight-margin.left-margin.right),0,0);

    selection.append("g")
    .attr("class", "axis yAxis")
    .call(yAxis);

  };

  var circleTooltips = function(selection, data) {
    // Draw overlaying boxes for tooltips
    //
    // make transparent rectangles of equal sizes
    // that lay on top of sample circles
    var sampleTooltipWidth = (d3.max(vScale.range()) / vScale.domain().length);
    var sampleTooltipHeight = (d3.max(jScale.range()) / jScale.domain().length);

    var tooltipData = d3.nest()
    .key(function(d) {return d[0]})
    .sortKeys(d3.ascending)
    .key(function(d) {return d[1]})
    .sortKeys(d3.ascending)
    .entries(data);

    var sampleTooltips = selection
    .append("g")
    .attr("class", "tooltip")
    .selectAll("g")
    .data(tooltipData)
    .enter()
    .append("g")
    .attr("class", function (d) {
      return "v-"+d.key
    })
    .selectAll("rect")
    .data(function(d) {
      return d.values
    })
    .enter()
    .append("rect")
    .attr("width", sampleTooltipWidth)
    .attr("height", sampleTooltipHeight)
    .attr("x", function (d) {
      return V(d.values[0]) - sampleTooltipWidth / 2;
    })
    .attr("y", function (d) {
      return J(d.values[0]) - sampleTooltipHeight / 2;
    })
    .style("opacity", 0)
    ;

    sampleTooltips
    .on("mouseover", function (d) {
      // dev
      var thisTooltip = d3.select(this);

      //highlight associated circles
      var thisV = d.values[0][0];
      var thisJ = d.values[0][1];
      d3.selectAll("circle")
      .filter(function(d) {
        return (thisV == d[0]) && (thisJ == d[1]);
      })
      .classed("active", true);

      //generate and display tooltip
      tooltip.append("div")
      .text("V: " + thisV);
      tooltip.append("div")
      .text("J: " + thisJ);

      var sampleContainer = tooltip.append("div");

      var sampleDivs = sampleContainer.selectAll("div")
      .data(d.values)
      .enter()
      .append("div")
      .attr("class", function(d) {return "cf-"+d[3]});

      sampleDivs
      .append("div")
      .text(function (d) {
        return SampleName(d);
      });

      sampleDivs
      .append("div")
      .text(function (d) {
        return "Frequency: " + d[2];
      });

      tooltip.style("visibility", "visible");

      // highlight associated axis label
      // This is hugely inefficient
      selection.selectAll("g.xAxis g.tick")
      .filter(function (d) { return d == thisV;})
      .style("font-weight", "bold");

      selection.selectAll("g.yAxis g.tick")
      .filter(function (d) {  return d == thisJ;})
      .style("font-weight", "bold");

    })
    .on("mousemove", function() {
      tooltip
      .style("top",(d3.mouse(this)[1]+ 125)+"px")
      .style("left",(d3.mouse(this)[0]+125)+"px");
    })
    .on("mouseout", function() {
      tooltip.html("");
      sampleCircles
      .classed("active", false);

      selection.selectAll("g.xAxis g.tick")
      .style("font-weight", null);

      selection.selectAll("g.yAxis g.tick")
      .style("font-weight", null);

    });


  };

  var vHist = function(selection) {
    var vNest = d3.nest()
    .key(function(d) {return d[3]})
    .key(function(d) { return d[0] })
    .rollup(function(leaves) {
      return d3.sum(leaves, function (d){
        return d[2]
      })
    })
    .entries(selection.datum());

    // calculate the scale
    var vHistScale = histScale(vNest)
    .range([histHeight-margin.bottom, 0]);


    var vSeries = makeSeries(vNest, vScale);
    var vLine = d3.svg.line()
    .x(function(d) {return vScale(d.group)})
    .y(function(d) {return vHistScale(d.freq)});

    // Make the actual lines
    var vPath = selection.selectAll(".line")
    .data(vSeries, function(d) {return d.key});

    vPath.exit().style('visibility', 'hidden');

    vPath.enter()
    .append("path")
    .attr("stroke-width", 1)
    .attr("fill", "none")
    .attr('class', function(d) {return "cf-"+d.key})
    .classed('line', true);

    // Update the lines
    vPath
    .style('visibility', 'visible')
    .attr("d", function(d) {return vLine(d.values)});

    // Add some points
    var vG = selection.selectAll("g.points")
    .data(vSeries, function(d) {return d.key} );

//    vG.exit().remove();

    vG.enter()
    .append("g")
    .attr("class", function(d,i) {
      return "cf-" + i + " points";
    });

    var vPoints = vG
    .selectAll("circle")
    .data(
      function(d) {return d.values},
      function(d) {return [d.group, d.sample]}
    );

    // hide old circles
    vPoints.exit().style('visibility', 'hidden');

    // Create new circles
    vPoints
    .enter()
    .append("circle")
    .attr("r", 5);

    // Plot the circles
    selection.selectAll("circle")
    .style('visibility', 'visible')
    .attr("cx", function(d) { return vScale(d.group)})
    .attr("cy", function(d,i ) { return vHistScale(d.freq)})
    .attr('class', function(d) {return "cf-"+d.sample});

    // Plot the axis
    var yAxis = d3.svg.axis()
    .scale(vHistScale)
    .orient("left")
    .ticks(3);

    var gAxis = selection.select("g.yAxis");
    if (gAxis.empty()) {
      gAxis = selection
      .append("g")
      .attr("class", "axis yAxis");
    }
    gAxis.call(yAxis);

  };

  var jHist = function(selection) {
    var jNest = d3.nest()
    .key(function(d) {return d[3]})
    .key(function(d) { return d[1] })
    .rollup(function(leaves) {
      return d3.sum(leaves, function (d){
        return d[2]
      })
    })
    .entries(selection.datum());

    // calculate the scale
    var jHistScale = histScale(jNest)
    .range([0, histHeight]);

    var jSeries = makeSeries(jNest, jScale);
    var jLine = d3.svg.line()
    .x(function(d) {return jHistScale(d.freq)})
    .y(function(d) {return jScale(d.group)});

    // Make the actual lines
    var jPath = selection.selectAll(".line")
    .data(jSeries, function(d) {return d.key} );

    // hide old lines
    jPath.exit().style('visibility', 'visible');

    // create new lines
    jPath.enter()
    .append("path")
    .attr("stroke-width", 1)
    .attr("fill", "none")
    .attr('class', function(d) {return "cf-"+d.key})
    .classed('line', true);

    // update lines
    jPath
    .style('visibilty', 'visible')
    .attr("d", function(d) {return jLine(d.values)});

    // set up groups to hold circles
    var jG = selection.selectAll("g.points")
    .data(jSeries,
      function(d) {return d.key}
    );

//  jG.exit.remove();

    jG.enter()
    .append("g")
    .attr("class", function(d,i) {
      return "sample-" + i + " points";
    })
    ;

    var jPoints = jG
    .selectAll("circle")
    .data(function(d) {return d.values},
    function(d) {return [d.group, d.sample]}
    );

    // Hide old circles
    jPoints.exit().style('visibilty', 'hidden');

    // Create new circles
    jPoints
    .enter()
    .append("circle")
    .attr("r", 5);

    // Plot the circles
    selection.selectAll("circle")
    .style('visibility', 'visible')
    .attr("cy", function(d) { return jScale(d.group)})
    .attr("cx", function(d,i ) { return jHistScale(d.freq)})
    .attr('class', function(d) {return "cf-"+d.sample});

    // Plot the axis
    var xAxis = d3.svg.axis()
    .scale(jHistScale)
    .orient("bottom")
    .ticks(2);

    var gAxis = selection.select("g.xAxis");
    if (gAxis.empty()) {
      gAxis = selection
      .append("g")
      .attr("class", "axis xAxis");
    }
    gAxis.call(xAxis);

    gAxis  .attr("transform", "translate(0," + (d3.max(jScale.range()) + ")"))

/*
    // events
    cfids.forEach(function (cfid) {
      cfelements = selection.selectAll('.cf-'+cfid)
      eventBus.subscribe('activate cf-'+cfid, classToggle(cfelements, true));
      eventBus.subscribe('inactivate cf-'+cfid, classToggle(cfelements, false));
    });
    */

  }

  function makeSeries(nest, scale) {
    var hash = nest.map(function(sampleData) {
      var tmp = {};
      sampleData.values.forEach(function(d) {
        tmp[d.key] = d.values;
      });
      return tmp;
    });

    return nest.map(function(sampleData, i) {
      var sampleDataMap = d3.map(nest);
      return {
        key: sampleData.key,
        values: scale.domain().map(function (d) {
          if (d in hash[i]) {
            return {
              group: d,
              freq: hash[i][d],
              sample: sampleData.key
            };
          }
          else {
            return {
              group: d, 
              freq: 0, 
              sample: sampleData.key
            };
          }
        }
        )}
    });
  }

  function histScale(nest) {
    return d3.scale
    .linear()
    .domain([0, d3.max(nest, function(sample) {
      return d3.max(sample.values, function (d) {
        return d.values;
      })
    })
    ])

  }


  var V = function(d) {
    return vScale(d[0]);
  }

  // the y-accessor for the circle generator
  var J = function(d) {
    return jScale(d[1]);
  }

  // the radius accessor for the circle generator
  var R = function(d) {
    return rScale(d[2]);
  }

  function SampleName(d) {
    return nameMap(d[3]);
  }

  plot.v = function(value) {
    if (!arguments.length) return xScale;
    vScale = value;
    return plot;
  }

  plot.j = function(value) {
    if (!arguments.length) return yScale;
    jScale = value;
    return plot;
  }

  plot.r = function(value) {
    if (!arguments.length) return rScale;
    rScale = value;
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

  plot.width = function(value) {
    if(!arguments.length) return width;
    width = value;
    return plot;
  }
  return plot;
}
