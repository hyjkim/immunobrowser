function scatterNav() {
  var margin = {top: 50, right: 50, bottom: 50, left: 50},
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
      jWidth = 100;


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
    var sampleCircles = vRows.selectAll("circle")
      .data(function(d) {return d.values}, 
          function(d) {return d[1]})
      .enter()
      .append("circle")
      .attr("cx", X)
      .attr("cy", Y)
      .attr("r", R)
      .attr("fill", Color)
      .attr("class", "inactive");

    // set up axes and labels
    var xAxis = d3.svg.axis()
      .scale(xScale)
      .orient("bottom")
      .ticks(xScale.range().length);

    gEnter.append("g")
      .attr("class", "axis xAxis")
      .attr("transform", "translate(0," + (d3.max(yScale.range()) + ")"))
      .call(xAxis);

    var yAxis = d3.svg.axis()
      .scale(yScale)
      .orient("left")
      .ticks(yScale.range().length);

    gEnter.append("g")
      .attr("class", "axis yAxis")
      .call(yAxis);

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
        thisTooltip.attr("class", "active");

        //highlight associated circles
        var thisV = d.values[0][0];
        var thisJ = d.values[0][1];
        d3.selectAll("circle")
        .filter(function(d) {
          return (thisV == d[0]) && (thisJ == d[1]);
        })
      .attr("class", "active");

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
      sampleCircles.attr("class", "inactive");

      //dev
      sampleTooltips.attr("class", "inactive");
    });


    // V histogram
    // this should probably be a function to facillitate updates

    // Make the svg that holds the plot
    var vHistSvg = selection.append("svg")
      .attr("class", "v-hist")
      .attr("height", vHeight)
      .attr("width", width);

    var vHistInner = vHistSvg.append("g").attr("class", "inner")
      .attr("transform", 
          "translate(" + margin.left + ",20)")
      .datum(data);



    // highlight circles when x-axis tick label is highlighted
    var xLabels = d3.selectAll("g.xAxis g.tick");
    xLabels
      .on("mouseover", function() {
        var vGene = d3.select(this).datum();
        d3.select(this).attr("fill", "blue");
        d3.selectAll("g.v-" +vGene+ " circle").attr("class", "active");
      })
    .on("mouseout", function () {
      xLabels.attr("fill", null);
      sampleCircles.attr("class", "inactive");
    });

    // highlight circles when y-axis tick labels are highlighted
    var yLabels = d3.selectAll("g.yAxis g.tick");
    yLabels
      .on("mouseover", function() {
        var jGene = d3.select(this).datum();
        d3.select(this).attr("fill", "blue");
        d3.selectAll("circle")
        .filter(function(d) {return d[1] == jGene})
        .attr("class", "active");

      // Try with a filtered dataset
      var filteredTestData = data.filter(function (d) {
        return d[1] == jGene
      });

      vHistInner.datum(filteredTestData).call(vHist);

      })
    .on("mouseout", function () {
      xLabels.attr("fill", null);
      sampleCircles.attr("class", "inactive");
      yLabels.attr("fill", null);
//      vHistInner.datum(data).call(vHist);
    });

    vHistInner.call(vHist);

    // J histogram

    // slider?
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

    // Make the series
    var vSeriesOld = vNest.map(function(d) {
      return d.values;
    });

    var vNestHash = vNest.map(function(sampleData) {
      var tmp = {};
      sampleData.values.forEach(function(d) {
        tmp[d.key] = d.values;
      });
      return tmp;
    });

    var vSeries = vNest.map(function(sampleData, i) {
      var sampleDataMap = d3.map(vNest);
      return xScale.domain().map(function (d) {
        if (d in vNestHash[i]) {
          return {key: d, values: vNestHash[i][d]};
        }
        else {
          return {key: d, values: 0};
        }
      })
    });

    console.log(vSeriesOld);
    console.log(vSeries);
    console.log(vNestHash);

    // calculate the scale
    var vHistScale = d3.scale
      .linear()
      .domain([0, d3.max(vNest, function(sample) {
        return d3.max(sample.values, function (d) {
          return d.values;
        })
      })
          ])
      .range([0, vHeight-margin.bottom]);

    var vLine = d3.svg.line()
      .x(function(d) {return xScale(d.key)})
      .y(function(d,i) {console.log("Line: "+d.key + " " + d.values); return vHistScale(d.values)});

    // Make the actual lines
    selection.selectAll(".line")
      .data(vSeries)
      .enter()
      .append("path")
      .attr("class", "line")
      .attr("stroke-width", 1)
      .attr("stroke", function(d,i) {return colorScale(i)})
      //        .attr("stroke", "black")
      .attr("fill", "none");

      // Update the lines
      selection.selectAll(".line")
      .attr("d", vLine);

    // Add some points
    var vG= selection.selectAll("g.points")
      .data(vSeries);

      vG
      .enter()
      .append("g")
      .attr("class", function(d,i) {
        return "sample-" + i + " points";
      })
    .attr("fill", function(d,i) {return colorScale(i)})

      var vPoints = vG
      .selectAll("circle")
      .data(function(d) {return d});

    // Delete old circles
    vPoints.exit().remove();

    // Create new circles
    vPoints
      .enter()
      .append("circle")
      .attr("r", 5)
      .attr("class", "inactive");

    // Plot the circles
    selection.selectAll("circle")
      .attr("cx", function(d) { return xScale(d.key)})
      .attr("cy", function(d,i ) { console.log("Points: "+d.key + " " + d.values); return vHistScale(d.values)});

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
        d3.select(this).attr("class", "active");
//        tooltip.style("visibility", "visibile");
//        tooltip.text("test");
      })
    .on("mousemove", function()  {
//      return tooltip.style("top",
//        (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
    })
    .on("mouseout", function()  {
      vPoints.attr("class", "inactive");
//      tooltip.html("");
//      tooltip.style("visibility", "hidden");
    })
    .on("click", function(d) {
      alert(d.key + " " + d.values);
    });

    // and some tooltips


  }


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

  return nav;
}


