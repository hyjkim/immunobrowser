function sharedClones() {
  var margin = {top: 20, right: 20, bottom: 20, left: 50},
  width = 500,
  height = 300,
  xScale = d3.scale.ordinal(),
  yScale = d3.scale.linear(),
  eventBus = EventBus.newEventBus();

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
      .attr('class', function(d) {return "cf-" + d.key });

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

  plot.eventBus = function(value) {
    if(!arguments.length) return eventBus;
    eventBus = value;
    return plot;
  }

  return plot;
}
