function sharedClones() {
  var margin = {top: 20, right: 20, bottom: 20, left: 20},
  width = 600,
  height = 400,
  xScale = d3.scale.ordinal(),
  yScale = d3.scale.linear().domain([0,1]);

  function plot(selection) {
    selection.each(function (data) {
      // set scales

      var svg= selection.selectAll('svg').data([data]);
      svg.enter().insert("svg");
      svg.attr("width", width)
      .attr("height", height);

      var gInner = svg.selectAll('g.Inner')
        .data(function(d) {return d});
        gInner.enter().append('g').attr("class",function(d) {return d.key});

      var circles = gInner.selectAll('circle').data(function(d) {console.log(d3.map(d.value['clonofilters']).entries());return d3.map(d.value['clonofilters']).entries()});
      circles.enter().append('circle')
      .attr('x',function(d) {return d.key})
      .attr('y', function(d) {return d.value});

/*
      var gAminoAcid = gInner.selectAll('g.amino-acid').data(function(d){console.log(d); return d });
      gAminoAcid.enter().append('g').attr('class', 'amino-acid');

*/
    });
  }

  function aaTable(selection){

  }

  plot.width = function(value) {
    if(!arguments.length) return width;
    width = value;
    return plot;
  }

  plot.height = function(value) {
    if(!arguments.length) return height;
    height = value;
    return plot;
  }

  plot.x = function(value) {
    if(!arguments.length) return xScale;
    xScale = value;
    return plot;
  }
  plot.y = function(value) {
    if(!arguments.length) return yScale;
    yScale = value;
    return plot;
  }


  return plot;
}

function functionality() {
  var margin = {top: 10, right: 10, bottom: 10, left: 100},
      width = 600,
      height = 200,
      heightScale = 40,
      //      xScale = d3.scale.linear().domain([0,1]),
      colorScale = d3.scale.ordinal(),
      nameMap = function(d) {return d};

  function plot (selection) {
    selection.each (function (data) {
//      xScale
//      .range([0, width - margin.left - margin.right]);
//
   // Get sample IDs
    var sampleIds = data.map(function (d) {return d.key});

    // Scale height 
    height = sampleIds.length * heightScale;

    // Make svg and set some attributes

    var svg = d3.select(this).selectAll("svg").data(d3.select(this).data());

    svg.enter().append("svg");
    svg.attr("width", width)
      .attr("height", height);

    var gInner = svg.append('g')
      .attr("class", "inner")
      .attr("transform", 'translate(' + margin.left + ',' + (height - margin.top ) +') rotate(-90)');

    console.log(data);

     // get set of productivity statuses
    var prodStatuses = d3.set([].concat.apply([],data.map(function (d) {
      return d3.map(d.values).keys();
    }))).values();

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

    console.log(dataMap);


    var x = d3.scale.ordinal()
      .domain(sampleIds)
      .rangeRoundBands([0, height - margin.top - margin.bottom], 0.1);
      //.rangeRoundBands([0, width - margin.left - margin.right]);

    var y = d3.scale.linear()
      .domain([0,1])
      .range([width - margin.left - margin.right, 0]);
      //.range([height - margin.top - margin.bottom, 0], 0.1);

    var color = d3.scale.category10();

    var stackMax = 1;
    var stack = d3.layout.stack()
      .values(function (d) { return d.values });

    console.log(stack(dataMap));


    var layers = gInner.selectAll('.layer')
      .data(stack(dataMap))
        .enter()
        .append('g')
        .attr('class', function (d) {return 'layer ' + d.key})
        .style("fill", function(d, i) { return color(i); });

    var rects = layers.selectAll('rect')
      .data(function (d) {return d.values})
      .enter()
      .append('rect')
      .attr('x', function(d) {return x(d.x)})
      //.attr('y', function(d) {return y(d.y)})
      .attr("y", function(d) { return y(d.y0 + d.y); })
      .attr('width', x.rangeBand())
      .attr("height", function(d) { return y(d.y0) - y(d.y0 + d.y); });
      //.attr("height", function(d) { return y(d.y); });


    // draw an x axis
    var xAxis = d3.svg.axis()
      .scale(x)
      .tickSize(0)
      .tickPadding(0)
      .orient('top');

    gInner.append('g')
      .attr('class', 'x axis')
//      .attr('transform', 'rotate(90)')
      .call(xAxis);

    // Convert the sample id to sample names
    gInner.selectAll('g .axis .tick text')
      .text(function (d) {
        return nameMap(d);
      })
      .attr('transform', 'rotate(90)')
    ;

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
      sampleIds = [];

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
        d3.selectAll("g.v-" +vGene+ " circle").attr("class", "active");

        var filteredTestData = data.filter(function (d) {
          return d[0] == vGene
        });
        jHistInner.datum(filteredTestData).call(jHist);
      })
    .on("mouseout", function () {
      xLabels.attr("fill", null);
      sampleCircles.attr("class", "inactive");
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
        .attr("class", "active");

      // Redraw v histograms with a filtered dataset
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

    jPath.exit().remove();

    jPath
      .enter()
      .append("path")
      .attr("class", "line")
      .attr("stroke-width", 1)
      .attr("stroke", function(d) {return colorScale(d.key)})
      .attr("fill", "none");

    selection.selectAll(".line")
      .attr("d", function(d) {return jLine(d.values)});

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
      .attr("r", 5)
      .attr("class", "inactive");

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
        //        tooltip.style("visibility", "visibile");
        //        tooltip.text("test");
      })
    .on("mousemove", function()  {
      //      return tooltip.style("top",
      //        (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
    })
    .on("mouseout", function()  {
      jPoints.attr("class", "inactive");
      //      tooltip.html("");
      //      tooltip.style("visibility", "hidden");
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
        return "sample-" + i + " points";
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
      .attr("r", 5)
      .attr("class", "inactive");

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

  return nav;
}


