function scatterNav2() {
  var margin = {top: 50, right: 30, bottom: 30, left: 60},
      width = 700,
      height = 500,
      histHeight = 100,
      nameMap = function(d) {return d[3]},
      tooltip,
      eventBus = EventBus.newEventBus(),
      rScale = d3.scale.linear(),
      vScale = d3.scale.ordinal(),
      jScale = d3.scale.ordinal();

  var plot = function(selection) {
    if (typeof tooltip ==='undefined') {
      tooltip = selection
        .append("div")
        .style("visibility", "hidden")
        .style("z-index", "10")
        .style("position", "absolute")
        .style("background", "white")
        .style("class", "scatter-tooltip")
        ;
    }

    selection.each(function(data) {
      // set the scales
      vScale
      .rangePoints([0, width - histHeight - margin.left - margin.right]);
    jScale
      .rangePoints([height - histHeight - margin.top - margin.bottom, 0]);
    // format the data
    var nestedData = d3.nest()
      .key(function(d) {return d[3]})
      .key(function(d) {return d[0]})
      .sortKeys(d3.ascending)
      .entries(data);

    // add the svg and create it if it doesn't exist
    var svg = d3.select(this).selectAll("svg#scatter").data([nestedData]);
    svg.enter().append("svg");
    svg.attr("width", width)
      .attr("height", height)
      .attr("id", "scatter");

    // Draw the circles
    var gScatter = svg.append("g").attr("class", "scatter")
      .attr("transform",
          "translate(" + margin.left + "," + margin.top +")")
      .datum(nestedData);
    scatter(gScatter);

    // Draw tooltips for frequency circles
    circleTooltips(gScatter, data);

    // draw v and j Hists
    var jHistInner = svg.append("g").attr("class", "j-hist")
      .attr("transform", 
          "translate("+(width-histHeight)+","+margin.top+")")
      .datum(data);
    jHistInner.call(jHist);

    var vHistInner = svg.append("g").attr("class", "v-hist")
      .attr("transform", 
          "translate(" + margin.left + ","+(height-histHeight)+")")
      .datum(data);
    vHistInner.call(vHist);


    // Add eventBus listeners to highlight all elements related
    // to a sample
    eventBus.subscribe('activate', function(selection) {
      selection.classed('active', true);
    });

    eventBus.subscribe('inactivate', function(selection) {
      selection.classed('active', false);
    });

    //subscribe all samples
    var cfids = nestedData.map(function(d) {return d.key});
    cfids.forEach(function (cfid) {
      cfcircles = selection.selectAll('circle.cf-'+cfid)
      var classToggle = function (selection, addOrRemove) {
        var cfcircles = selection;
        return function () {
          cfcircles.classed('active', addOrRemove);
        }
      }
      eventBus.subscribe('activate cf-'+cfid, classToggle(cfcircles, true));
    eventBus.subscribe('inactivate cf-'+cfid, classToggle(cfcircles, false));

    });

    });

  };

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
      .tickSize(-(height-margin.top-margin.bottom-histHeight),0,0);

    selection.append("g")
      .attr("class", "axis xAxis")
      .attr("transform", "translate(0," + (d3.max(jScale.range()) + ")"))
      .call(xAxis);

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
      .attr("class", "tooltips")
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
        .text("V family: " + thisV);
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
      })
    .on("mousemove", function() {
      return tooltip.style("top",
        (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");

    })
    .on("mouseout", function() {
      tooltip.html("");
      sampleCircles
      .classed("active", false);
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
      .range([0, histHeight-margin.bottom]);


    var vSeries = makeSeries(vNest, vScale);
    var vLine = d3.svg.line()
      .x(function(d) {return vScale(d.group)})
      .y(function(d) {
        return vHistScale(d.freq)});

    // Make the actual lines
    var vPath = selection.selectAll(".line")
      .data(vSeries);

    vPath.exit().remove();

    vPath.enter()
      .append("path")
      .attr("class", "line")
      .attr("stroke-width", 1)
      .attr("fill", "none");

    // Update the lines
    selection.selectAll(".line")
      .attr("d", function(d) {return vLine(d.values)})
      .attr('class', function(d) {return "cf-"+d.key});

    // Add some points
    var vG = selection.selectAll("g.points")
      .data(vSeries,
          function(d) {return d.key});

    vG.exit().remove();

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

    // Delete old circles
    vPoints.exit().remove();

    // Create new circles
    vPoints
      .enter()
      .append("circle")
      .attr("r", 5);

    // Plot the circles
    selection.selectAll("circle")
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
      .data(jSeries,
          function(d) {return d.key} 
          );

    // remove old lines
    jPath.exit().remove();

    // create new lines
    jPath
      .enter()
      .append("path")
      .attr("class", "line")
      .attr("stroke-width", 1)
      .attr("fill", "none");

    // update lines
    selection.selectAll(".line")
      .attr("d", function(d) {return jLine(d.values)})
      .attr('class', function(d) {return "cf-"+d.key});

    // set up groups to hold circles
    var jG = selection.selectAll("g.points")
      .data(jSeries,
          function(d) {return d.key}
          );

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

    // Delete old circles
    jPoints.exit().remove();

    // Create new circles
    jPoints
      .enter()
      .append("circle")
      .attr("r", 5);

    // Plot the circles
    selection.selectAll("circle")
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
  return plot;
}

function scatterNav() {
  var margin = {top: 50, right: 30, bottom: 30, left: 60},
      width=600,
      height = 400,
      xValue = function(d) {return d[0]},
      yValue = function(d) {return d[1]},
      xScale = d3.scale.ordinal(),
      yScale = d3.scale.ordinal(),
      rScale = d3.scale.linear(),
      colorScale = d3.scale.category10(),
      nameMap = function(d) {return d[3]},
      vHeight = 100,
      jWidth = 100,
      sampleIds = [],
      sampleCircles;

  function nav (selection) {
    selection.each(function(data) {
      // update the x-scale to include margins
      xScale
      .rangePoints([0, width - margin.left - margin.right]);

    // update the y-scale to include margins
    yScale
      .rangePoints([height -
        margin.top -
        margin.bottom, 0]);

    // select the svg element
    var nestedData = d3.nest()
      .key(function(d) {return d[3]})
      .key(function(d) {return d[0]})
      .sortKeys(d3.ascending)
      .entries(data);

    // set the sample Ids
    sampleIds = nestedData.map(function(d) {return d.key});

    var svg = d3.select(this).selectAll("svg").data([nestedData]);

    // create if it doesn't exist
    svg.enter().append("svg");

    // update the svg dimensions
    svg.attr("width", width)
      .attr("height", height);

    // update the inner dimensions
    var gEnter = svg.append("g").attr("class", "inner")
      .attr("transform", 
          "translate(" + margin.left + "," + margin.top +")");


    // plot the cicles that make up the scatterplot
    // make a group for each sample
    var sampleRows = gEnter.selectAll("g")
      .data(nestedData, function(d) {return d.key})
      .enter()
      .append("g")
      .attr("class", function(d) {
        return "sample-"+d.key
      });

    // make a group for each v gene
    var vRows = sampleRows.selectAll("g")
      .data(function(d) {return d.values}, function(d) {return d.key})
      .enter()
      .append("g")
      .attr("class", function(d) {return "v-"+d.key})
      ;

    // now actually plot the circles
    sampleCircles = vRows.selectAll("circle")
      .data(function(d) {return d.values}, 
          function(d) {return d[1]})
      .enter()
      .append("circle")
      .attr("cx", X)
      .attr("cy", Y)
      .attr("r", R)
      //      .attr("fill", Color)
      .attr("class", function(d) {return "cf-"+d[3].toString()})
      .classed('inactive', true);

    // set up axes and labels
    var xAxis = d3.svg.axis()
      .scale(xScale)
      .orient("bottom")
      .ticks(xScale.range().length)
      .tickSize(-height+margin.top+margin.bottom,0,0);

    gEnter.append("g")
      .attr("class", "axis xAxis")
      .attr("transform", "translate(0," + (d3.max(yScale.range()) + ")"))
      .call(xAxis);

    var yAxis = d3.svg.axis()
      .scale(yScale)
      .orient("left")
      .ticks(yScale.range().length)
      .tickSize(-width,0,0)
      ;

    gEnter.append("g")
      .attr("class", "axis yAxis")
      .call(yAxis);

    // draw a grid



    // set up tooltips
    // generate the tooltip div
    var tooltip = selection
      .append("div")
      .style("visibility", "hidden")
      .style("z-index", "10")
      .style("position", "absolute")
      .style("background", "white")
      .style("class", "scatter-tooltip")
      ;

    // make transparent rectangles of equal sizes
    // that lay on top of sample circles
    var sampleTooltipHeight = (d3.max(yScale.range()) / yScale.domain().length);
    var sampleTooltipWidth = (d3.max(xScale.range()) / xScale.domain().length);

    var tooltipData = d3.nest()
      .key(function(d) {return d[0]})
      .sortKeys(d3.ascending)
      .key(function(d) {return d[1]})
      .sortKeys(d3.ascending)
      .entries(data);

    var sampleTooltips = gEnter
      .append("g")
      .attr("class", "tooltips")
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
        return X(d.values[0]) - sampleTooltipWidth / 2;
      })
    .attr("y", function (d) {
      return Y(d.values[0]) - sampleTooltipHeight / 2;
    })
    .style("opacity", 0)
      ;

    // add tooltip functionality to the circles
    sampleTooltips
      .on("mouseover", function (d) {
        // dev
        var thisTooltip = d3.select(this);
        //        thisTooltip.attr("class", "active");

        //highlight associated circles
        var thisV = d.values[0][0];
        var thisJ = d.values[0][1];
        d3.selectAll("circle")
        .filter(function(d) {
          return (thisV == d[0]) && (thisJ == d[1]);
        })
      .classed("active", true)
        .classed("inactive", false);

      //generate and display tooltip

      tooltip.append("div")
        .text("V family: " + thisV);
      tooltip.append("div")
        .text("J: " + thisJ);

      var sampleContainer = tooltip.append("div");

      var sampleDivs = sampleContainer.selectAll("div")
        .data(d.values)
        .enter()
        .append("div")
        .style("border-color", function (d) {
          return Color(d);
        })
      .style("border-width", 3)
        .style("border-style", "solid");

      sampleDivs
        .append("div")
        .text(function (d) {
          return "Sample: " + SampleName(d);
        });

      sampleDivs
        .append("div")
        .text(function (d) {
          return "Frequency: " + d[2];
        });

      tooltip.style("visibility", "visible");
      })
    .on("mousemove", function() {
      return tooltip.style("top",
        (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");

    })
    .on("mouseout", function() {
      tooltip.html("");
      sampleCircles.classed("active", false)
      .classed("active", false);
    });


    // J histogram 
    var jHistSvg = selection.append("svg")
      .attr("class", "hist-j")
      .attr("height", height)
      .attr("width", jWidth);

    var jHistInner = jHistSvg.append("g").attr("class", "inner")
      .attr("transform", 
          "translate(0,"+margin.top+")")
      .datum(data);


    // V histogram

    // Make the svg that holds the plot
    var vHistSvg = selection.append("svg")
      .attr("class", "hist-v")
      .attr("height", vHeight)
      .attr("width", width);

    var vHistInner = vHistSvg.append("g").attr("class", "inner")
      .attr("transform", 
          "translate(" + margin.left + ",10)")
      .datum(data);



    // highlight circles when x-axis tick label is highlighted
    var xLabels = d3.selectAll("g.xAxis g.tick");
    xLabels
      .on("mouseover", function() {
        var vGene = d3.select(this).datum();
        d3.select(this).attr("fill", "blue");
        d3.selectAll("g.v-" +vGene+ " circle")
        .classed("active", true);

      var filteredTestData = data.filter(function (d) {
        return d[0] == vGene
      });
      jHistInner.datum(filteredTestData).call(jHist);
      })
    .on("mouseout", function () {
      xLabels.attr("fill", null);
      sampleCircles.classed("active", false);
      //      jHistInner.datum(data).call(jHist);
    });

    // highlight circles when y-axis tick labels are highlighted
    var yLabels = d3.selectAll("g.yAxis g.tick");
    yLabels
      .on("mouseover", function() {
        var jGene = d3.select(this).datum();
        d3.select(this).attr("fill", "blue");
        d3.selectAll("circle")
        .filter(function(d) {return d[1] == jGene})
        .classed("active", true);

      // Redraw v histograms with a filtered dataset
      var filteredTestData = data.filter(function (d) {
        return d[1] == jGene
      });

      vHistInner.datum(filteredTestData).call(vHist);
      })
    .on("mouseout", function () {
      xLabels.attr("fill", null);
      sampleCircles
      .classed('active', false);
    yLabels.attr("fill", null);
    //      vHistInner.datum(data).call(vHist);
    })

    jHistInner.call(jHist);
    vHistInner.call(vHist);

    // slider?
    });
  }

  // j hist plot
  function jHist(selection) {
    var jNest = d3.nest()
      .key(function(d) {return d[3]})
      .key(function(d) { return d[1] })
      .rollup(function(leaves) {
        return d3.sum(leaves, function (d){
          return d[2]
        })
      })
    .entries(selection.datum());

    var jSeries = makeSeries(jNest, yScale);

    // calculate the scale
    var jHistScale = histScale(jNest)
      .range([0, jWidth]);

    var jLine = d3.svg.line()
      .x(function(d) {return jHistScale(d.freq)})
      .y(function(d) {return yScale(d.group)});

    // Make the actual lines
    var jPath = selection.selectAll(".line")
      .data(jSeries,
          function(d) {return d.key} 
          );

    // remove old lines
    jPath.exit().remove();

    // create new lines
    jPath
      .enter()
      .append("path")
      .attr("class", "line")
      .attr("stroke-width", 1)
      .attr("stroke", function(d) {return colorScale(d.key)})
      .attr("fill", "none");

    // draw paths
    selection.selectAll(".line")
      .attr("d", function(d) {return jLine(d.values)});

    // set up groups to hold circles
    var jG = selection.selectAll("g.points")
      .data(jSeries,
          function(d) {return d.key}
          );

    jG.enter()
      .append("g")
      .attr("class", function(d,i) {
        return "sample-" + i + " points";
      })
    .attr("fill", function(d) {return colorScale(d.key)})

      var jPoints = jG
      .selectAll("circle")
      .data(function(d) {return d.values},
          function(d) {return [d.group, d.sample]}
          );

    // Delete old circles
    jPoints.exit().remove();

    // Create new circles
    jPoints
      .enter()
      .append("circle")
      .attr("r", 5);

    // Plot the circles
    selection.selectAll("circle")
      .attr("cy", function(d) { return yScale(d.group)})
      .attr("cx", function(d,i ) { return jHistScale(d.freq)});

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

    gAxis  .attr("transform", "translate(0," + (d3.max(yScale.range()) + ")"))

      // Add some tooltips
      jPoints
      .on("mouseover", function()  {
        d3.select(this).attr("class", "active");
      })
    .on("mousemove", function()  {
    })
    .on("mouseout", function()  {
      jPoints.attr("class", "inactive");
    })
    .on("click", function(d) {
      alert(d.key + " " + d.values);
    });


  }

  // v hist plot
  // Given a dataset, generates a vHist
  function vHist(selection) {
    // process the data
    var vNest = d3.nest()
      .key(function(d) {return d[3]})
      .key(function(d) { return d[0] })
      .rollup(function(leaves) {
        return d3.sum(leaves, function (d){
          return d[2]
        })
      })
    .entries(selection.datum());
    var vSeries = makeSeries(vNest, xScale);

    // calculate the scale
    var vHistScale = histScale(vNest)
      .range([0, vHeight-margin.bottom]);

    var vLine = d3.svg.line()
      .x(function(d) {return xScale(d.group)})
      .y(function(d) {
        return vHistScale(d.freq)});

    // Make the actual lines
    var vPath = selection.selectAll(".line")
      .data(vSeries);

    vPath.exit().remove();

    vPath.enter()
      .append("path")
      .attr("class", "line")
      .attr("stroke-width", 1)
      .attr("stroke", function(d) {return colorScale(d.key)})
      .attr("fill", "none");

    // Update the lines
    selection.selectAll(".line")
      .attr("d", function(d) {return vLine(d.values)});

    // Add some points
    var vG = selection.selectAll("g.points")
      .data(vSeries,
          function(d) {return d.key});

    vG.exit().remove();

    vG.enter()
      .append("g")
      .attr("class", function(d,i) {
        return "cf-" + i + " points";
      })
    .attr("fill", function(d) {return colorScale(d.key)})

      var vPoints = vG
      .selectAll("circle")
      .data(
          function(d) {return d.values},
          function(d) {return [d.group, d.sample]}
          );

    // Delete old circles
    vPoints.exit().remove();

    // Create new circles
    vPoints
      .enter()
      .append("circle")
      .attr("r", 5);

    // Plot the circles
    selection.selectAll("circle")
      .attr("cx", function(d) { return xScale(d.group)})
      .attr("cy", function(d,i ) { return vHistScale(d.freq)});


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

    // Add some tooltips
    vPoints
      .on("mouseover", function()  {
        d3.select(this).classed("active", true);
        //        tooltip.style("visibility", "visibile");
        //        tooltip.text("test");
      })
    .on("mousemove", function()  {
      //      return tooltip.style("top",
      //        (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
    })
    .on("mouseout", function()  {
      vPoints.classed("active", false);
      //      tooltip.html("");
      //      tooltip.style("visibility", "hidden");
    })
    .on("click", function(d) {
      alert(d.key + " " + d.values);
    });

    // and some tooltips
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

  /*
   * Public Accessor functions
   */

  // The x-accessor for the circle generator
  function X(d) {
    return xScale(d[0]);
  }

  // the y-accessor for the circle generator
  function Y(d) {
    return yScale(d[1]);
  }

  // the radius accessor for the circle generator
  function R(d) {
    return rScale(d[2]);
  }

  // the color accessor for the circle generator
  function Color(d) {
    return colorScale(d[3]);
  }

  function SampleName(d) {
    return nameMap(d[3]);
  }

  // setters and getters for chart config
  nav.width = function (value) {
    if (!arguments.length) return width;
    width = value;
    return nav;
  }

  nav.height = function(value) {
    if (!arguments.length) return height;
    height = value;
    return nav;
  }

  nav.padding = function(value) {
    if (!arguments.length) return padding;
    padding = value;
    return nav;
  }

  nav.x = function(value) {
    if (!arguments.length) return xScale;
    xScale = value;
    return nav;
  }

  nav.y = function(value) {
    if (!arguments.length) return yScale;
    yScale = value;
    return nav;
  }

  nav.r = function(value) {
    if (!arguments.length) return rScale;
    rScale = value;
    return nav;
  }

  nav.color = function(value) {
    if(!arguments.length) return colorScale;
    colorScale = value;
    return nav;
  }

  nav.sampleName = function(value) {
    if(!arguments.length) return nameMap;
    nameMap = value;
    return nav;
  }

  nav.circles = function () {
    return sampleCircles;
  }

  // Modifies a subset of elements 
  // Takes in a d3 selection and changes all elements to active state
  nav.activate = function (selection) {
    selection.classed("active", true);
  }
  nav.inactivate = function (selection) {
    selection.classed("active", false);
  }


  return nav;
}


