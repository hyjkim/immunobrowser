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
      .attr("class", "line shared-clones")
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
      .attr('class', function(d) {return "cf-" + d.key });

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


      // Make the table header
      var table = selection.append('table')
      .attr('class', 'table');
      var tableHeader = table.append('thead').append('tr');
      tableHeader.append('th').text('Shared Amino Acid Sequence');

      // draw table
      table.data(selection.data(), function(d) {
      return d;
      });
      var aminoAcidRows = table.selectAll('tr').data(function(d){return d}).enter()
      .append('tr')
      .attr('class', function(d) {return 'aa-'.concat(d.key)})

      var aminoAcidCells =  aminoAcidRows.append('td')
      .html(function(d) {
        return '<a href="/amino_acid/'+d.key+'">'+d.value.sequence+'</a>';
      })
      ;

      var sampleCells = aminoAcidRows.selectAll('td')
      .data(function(d) {return d3.map(d.value.clonofilters).entries()}, function(d) {return d.key})
      .enter()
      .append('td')
      .text(function(d) {return d.value})
      .attr("class", function(d) {return 'cf-'+d.key});

      // Add interactivity to eventBus
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

      // selecting samples
      cfids.forEach(function (cfid) {
        cfcircles = selection.selectAll('circle.cf-'+cfid)
        cfcells = selection.selectAll('td.cf-'+cfid)
        subscribeActivation(cfcircles, 'cf-'+cfid);
        subscribeActivation(cfcells, 'cf-'+cfid);
      });

      // subscribe amino_acids circles, lines and rows to highlight
      gAmino.each(function (d) {
        var circles = d3.select(this).selectAll('circle');
        var lines = d3.select(this).selectAll('path');
        subscribeActivation(circles, 'aa-'+d.key);
        subscribeActivation(lines, 'aa-'+d.key);
      });

      //subscribe all amino_acids rows
      aminoAcidRows.data().forEach(function(d) {
        var aminoAcids = selection.selectAll('.aa-'+d.key+' td');
        subscribeActivation(aminoAcids, 'aa-'+d.key)
      });

      // publish-highlight events
      var aminoAcidEvents = function(selection) {
        selection.each(function (d) {
          d3.select(this).on("mouseover", function() {
            eventBus.publish('activate aa-'+ d.key, 1);
          });
          d3.select(this).on("mouseout", function() {
            eventBus.publish('inactivate aa-'+ d.key, 1);
          });
        });
      }
      aminoAcidEvents(aminoAcidRows);
      aminoAcidEvents(gAmino);

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
