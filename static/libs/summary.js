function summaryTable() {
  function table(selection) {
    selection.each(function (data){
      console.log(selection);
      console.log(data);
      var table = selection.selectAll('table').data([data]);
      table.enter().append('table');

    });
    };

    return table();
}
