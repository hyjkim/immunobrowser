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
var comparisonRefresh = function () {
  var filterFormDiv = d3.select("div#filter-forms");
  var navDiv = d3.select("#scatter-content");
  var functDiv = d3.select("#functionality-content");
  var sharedClonesDiv = d3.select("#shared-clones-content");
  var clonofilterColors = d3.select("style#clonofilter-colors");
  var addSampleToggle = $("button#add-sample");
  var sampleCancel = $('div#sample-compare :button');
  var sampleSubmit = $('div#sample-compare :submit');
  var sampleCompareDiv = $('div#sample-compare');
  var sampleForm = $('div#sample-compare form');
  var sideNav = $('div#sidenav');
  var comparisonId;
  var eventBus = EventBus.newEventBus();

  // update the forms
  var init = function() {
    if (comparisonId) refresh();
    addSample();
    setupNav();

    // Resize the scrollable divs when the window is resized
    $(window).resize(function () {
      setupNav();
    });
  }

  var refresh = function() {
    filterFormRefresh();
    clonofilterColorsRefresh();
    drawScatterNav();
    drawFunctionality();
    drawSharedClones();
  }

  var setupNav = function () {
    var contentHeight = $(window).height() - $('nav#topnav').height();
    sideNav.css('max-height', contentHeight);
    sideNav.css('height', contentHeight);
    $('#subcontent').css('max-height', contentHeight);
    $('#subcontent').css('height', contentHeight);
  }

  // enable add sample functionality
  var addSample = function () {
    addSampleToggle.click(function () {
        sampleCompareDiv.show();
        addSampleToggle.prop('disabled', true);
        });
    // Hides add sample form when cancel button is clicked
    sampleCancel.click(function () {
        sampleCompareDiv.hide();
        addSampleToggle.prop('disabled', false);
        });

    sampleSubmit.click(function () {
        event.preventDefault();
        var postData = sampleForm.serializeArray();
        if (comparisonId) {
        postData.push({'name':'comparison', 'value': comparisonId});
        }

        sampleCompareDiv.hide();
        addSampleToggle.show();

        console.log(postData);

        $.post('/dashboard/add_samples_v2',
          postData, function (compId) {

          // Load filter forms
          $.get("/compare/" + compId + "/filter_forms",
            function(filterForms) {
            $('div#filter-forms').html(filterForms)
            refresh();
            });

          // Update global comparisonId variable
          comparisonId = compId

          // Modify url bar
          // Should modify this javascript to use 
          // a django template tag for 'dashboard.views.compare_v2'
          window.history.pushState(null, '', '/compare/' + compId);
          });


    });

  }

  var clonofilterColorsRefresh = function () {
    var url = '/compare/'+comparisonId+'/clonofilter_colors';
    $.get(url, function (d) {
        clonofilterColors.text(d);
        });
  }

  var filterFormRefresh = function () {
    var url = '/compare/'+comparisonId+'/filter_forms';
    $.get(url,
        function (d) {
        filterFormDiv.html(d);
        // Refresh everything when a the update button is clicked
        $('input#compare-update')
        .click(function() {
          var clonofilterForm = $('div#filter-forms form');
          //          event.preventDefault();
          var postData =clonofilterForm.serializeArray();
          if (comparisonId) {
          postData.push({'name':'comparison', 'value': comparisonId});
          }
          console.log(postData)

          $.post('/compare/'+comparisonId+'/update_clonofilters',
            postData, function (compId) {
            console.log(compId);
            comparisonId = compId;
            refresh();
            });

          });

    // add event to select all graphic elements associated with the clonofilter
    var filterForms = $('.filter-form');
    filterForms.each(function () {
        var cfid = $(this).attr('id').replace("filter-","");
        eventBus.subscribe("activate " + cfid, function (selection) {
          selection.addClass('active');
          });
        eventBus.subscribe("inactivate " + cfid, function (selection) {
          selection.removeClass('active');
          });
        });
    filterForms.on("mouseover",function(){
        var cfid = $(this).attr('id').replace("filter-","");
        eventBus.publish("activate " + cfid, $(this));
        })
    .on("mouseout", function() {
        var cfid = $(this).attr('id').replace("filter-","");
        eventBus.publish("inactivate " + cfid, $(this));
        });

        });
    // update the colors
  }

  var drawScatterNav = function() {
    var vdjFreq, vList, jList, sampleNames;

    d3.json('/compare/'+comparisonId+'/vdj_freq_ajax', function(d) {
        vdjFreq = d['vdjFreq'];
        vList = d['vList'];
        jList = d['jList'];
        sampleNames = d['sampleNames'];
        scatNav();
        });

    var scatNav = function () {
      

      var my_xScale = d3.scale
        .ordinal()
        .domain(vList);

      var my_yScale = d3.scale
        .ordinal()
        .domain(jList);

      var my_rScale = d3.scale.linear()
        .domain([0, d3.max(vdjFreq, function(d) {
              return d[2];
              })
            ])
        .range([0, 24]);

      my_names = nameMap(sampleNames);

      var my_nav = scatterNav()
        .x(my_xScale)
        .y(my_yScale)
        .r(my_rScale)
        .sampleName(my_names);


      navDiv.html('');

      navDiv
        .datum(vdjFreq)
        .call(my_nav)
        ;

      var scatNav2 = scatterNav2()
        .v(my_xScale)
        .j(my_yScale)
        .r(my_rScale)
        .eventBus(eventBus)
        .sampleName(my_names);

      navDiv
        .datum(vdjFreq)
        .call(scatNav2)
        ;

    }
  }

  var drawFunctionality = function () {
    d3.json('/compare/'+comparisonId+'/functionality_ajax', function(d) {
        console.log(d);
        var functData = d['functionality'];
        var sampleNames = d['sampleNames'];

        var my_names = nameMap(sampleNames);
        var functPlot = functionality2()
        .sampleName(my_names);

        // Remove existing stuff in the div
        functDiv.html('');

        functDiv
        .datum(functData)
        .call(functPlot)
        ;
        });
  }

  var drawSharedClones = function () {
    d3.json('/compare/'+comparisonId+'/shared_clones_ajax', function(d) {
      var aminoAcids = d3.map(d['aminoAcids'])
      var sampleNAmes = d['sampleNames']

      sharedClonesDiv.html('');

    var mySharedClones = sharedClones()
      .eventBus(eventBus);

    sharedClonesDiv
      .datum(aminoAcids.entries())
      .call(mySharedClones);
    });

    $.get('/compare/'+comparisonId+'/shared_clones', function(d) {
      sharedClonesDiv.append("div").html(d);
    });

  }

  var nameMap = function (n) {
    var names = n;
    return function(d) {
      return names[d];
    }
  };

  init.filterFormDiv = function(value) {
    if(!arguments.length) return filterFormDiv;
    filterFormDiv = value;
    return init;
  }

  init.comparisonId = function(value) {
    if(!arguments.length) return comparisonId;
    comparisonId = value;
    return init;
  }

  return init;
}

