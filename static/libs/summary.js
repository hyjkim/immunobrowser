function summaryTable() {
  var sampleName = function (d) {return d},
  eventBus = EventBus.newEventBus();
  function table(selection) {
    selection.each(function (data){
      var table = selection.selectAll('table').data([d3.map(data).entries()]);
      table.enter().append('table').attr('class', 'table');
      var rows = table.selectAll('tr').data(function(d) { return d})
      .enter().append('tr')
      .attr('class', function(d) {return 'cf-'+d.key});
      rows.append('td').text(function(d) {return sampleName(d.key)});
      rows.append('td').text(function(d) {return d.value['reads']});
      rows.append('td').text(function(d) {return d.value['recombinations']});
      rows.append('td').text(function(d) {return d.value['aminoAcids']});
      rows.append('td').text(function(d) {return d3.round(d.value['entropy'], 2)});
      rows.append('td').append('a').attr('href', function(d) {return '/clonotypes?cf='+d.key}).text('View all clonotypes');

      rows.selectAll('td').attr('class', function (d) {return 'cf-' + d.key});

      var header = table.insert('tr', 'tr');
      header.append('th').text('Sample');
      header.append('th').text('Reads');
      header.append('th').text('Recombinations');
      header.append('th').text('Amino Acids');
      header.append('th').text('Entropy');
      header.append('th').text('All Clonotypes');

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

      rows.each(function(d) {
        subscribeActivation(d3.select(this).selectAll('td'), "cf-"+d.key);
      });
    });
  };

  table.sampleName = function(value) {
    if(!arguments.length) return sampleName;
    sampleName = value;
    return table;
  }

  table.eventBus = function(value) {
    if(!arguments.length) return eventBus;
    eventBus = value;
    return table;
  }
  return table;
}
