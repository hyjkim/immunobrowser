// Todo: change all events to use an eventBus
//   subscribe all common events to the same name
//   see if you need data
//   call change events on various listeners
//   call revert events on mouseout
//     data could be useful for call to
//     revert changes onto to specific items
//     and call only a subset of subscriptions
//     or data could be used as the selector
//     onto which the activation or deactivation
//     is applied.

//     now i have nav.activate and nav.inactivate
//     these take in a selection
//     and i could pass these data to it in order
//     for them to be uncalled
    
//     or i could just specify the callback to call
//     on the selection to begin with. still data
//     might be useful elsewhere.

//     I may remove the data requirement on the call back
//     for now or make it optional

function sharedClones() {
  var margin = {top: 20, right: 20, bottom: 20, left: 50},
  width = 500,
  height = 300,
  colorScale = function () { return null },
  //colorScale = d3.scale.category10(),
  xScale = d3.scale.ordinal(),
  yScale = d3.scale.linear(),
  eventBus = EventBus.new_eventBus();

  function plot(selection) {
    selection.each(function (data) {
      // Get max frequency
      var max_freq = d3.max(data, function(d) {
        return d3.max(d3.map(d.value.clonofilters).entries(), function (freq) {
          return freq.value;
        });
      });
      // get x domain
      var cfids = data.map(function(d) {
        return d3.map(d.value.clonofilters).keys();
      });
      cfids = d3.set([].concat.apply([], cfids)).values();
      // set scales
      xScale.domain(cfids)
      .rangePoints([0, width - margin.left - margin.right], 1);
      yScale.domain([0,max_freq]).range([height - margin.top - margin.bottom,0]);

      // get the svg and create it if necessary
      var svg = selection.selectAll('svg').data([data]);
      svg.enter().insert("svg");
      svg.attr("width", width)
      .attr("height", height);

      var gInner = svg.append("g").data([data])
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


      // create a g for amino acid groups
      var gAmino = gInner.selectAll('g.Inner')
        .data(function(d) {return d});
        gAmino.enter().append('g')
          .attr("class",function(d) {return "aa-"+d.key})

      // draw lines
      var line = d3.svg.line()
        .x(function (d) {return xScale(d.key)})
        .y(function (d) {return yScale(d.value)});

      var path = gAmino.selectAll(".line")
      .data(function(d) {return [d3.map(d.value['clonofilters']).entries()]});

      path.enter().append("path")
      .attr("class", "line inactive")
      .attr("stroke-width", 1)
      .attr("stroke", "#000000")
      .attr("fill", "none");

    gAmino.selectAll(".line")
      .attr("d", function(d) {return line(d)});

       
      // draw circles
      var circles = gAmino.selectAll('circle')
      .data(function(d) {return d3.map(d.value['clonofilters']).entries()});
      circles.enter().append('circle')
      .attr('cx',function(d) {return xScale(d.key)})
      .attr('cy', function(d) {return yScale(d.value)})
      .attr('r', 10)
//      .attr('class', 'inactive')
//      .attr('class', function(d) {return "cf-" + d.key + "-inactive"})
      .attr('class', function(d) {return "cf-" + d.key })
      .attr("fill", function(d) {return colorScale(d.key)});

      // Add interactivity to eventBus
      var activate = function (selection) {
        selection.classed('active', true);
      }
      var inactivate = function (selection) {
        selection.classed('active', false);
      }

      eventBus.subscribe('activate',activate);
      eventBus.subscribe('inactivate',inactivate);

      // selecting individual circles
      circles.on('mouseover', function () {
        eventBus.publish('activate', d3.select(this));
      })
      .on('mouseout', function () {
        eventBus.publish('inactivate', circles);
      })

      // selecting samples
      cfids.forEach(function (cfid) {
        //eventBus.subscribe('activate cf-'+cfid, activateSample().selection(circles.selectAll('.cf-'+cfid)));
        cfcircles = d3.selectAll('circle.cf-'+cfid)
        eventBus.subscribe('activate cf-'+cfid, function () {
          cfcircles.classed('active', true);
        });
        eventBus.subscribe('inactivate cf-'+cfid, function () {
          cfcircles.classed('active', false);
        });

      });

      //amino acid highlighting functionality
      var amino = d3.select(".amino")
        .on("mouseover", function() {
          console.log(d3.select(this));
        });

      // draw x axis
      var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom");

      gInner.append("g")
        .attr("class", "axis xAxis")
        .attr("transform", "translate(0," + (d3.max(yScale.range()) + ")"))
        .call(xAxis);

      // draw y axis
      var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");

      gInner.append("g")
        .attr("class", "axis yAxis")
        .call(yAxis);

    });
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

  plot.color = function(value) {
    if(!arguments.length) return colorScale;
    colorScale = value;
    return plot;
  }

  plot.eventBus = function(value) {
    if(!arguments.length) return eventBus;
    eventBus = value;
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


