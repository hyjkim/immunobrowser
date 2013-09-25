var comparisonRefresh = function () {
  var ajaxLoader = "/static/img/ajax-loader.gif";
  var filterFormDiv = d3.select("div#filter-forms");
  var navDiv = d3.select("#scatter-content");
  var spectratypeDiv = d3.select("#spectratype-content");
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
  var unsubscribeTokens = [];
  var eventBus = EventBus.newEventBus();


  // Function to get search terms from url
  function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
  }


  // update the forms
  var init = function() {
    if (comparisonId) refresh();
    else $('.view').hide();
    addSample();
    setupNav();
    setNavHeight();
    enableTooltips();

    // Enables back button for navigation
    //    window.addEventListener("popstate", function(e) { loadPage(location.pathname); });
  }

  var refresh = function() {
    clearEventBus(); // Should clear eventBus of events that will disappear
    $('#compare-intro').hide();
    showComparisonViews();
    filterFormRefresh();
    clonofilterColorsRefresh();
    drawScatterNav();
    drawFunctionality();
    drawSharedClones();
    drawSpectratype();
  }

  var showComparisonViews = function () {
    $(".view").show();
  };

  var clearEventBus = function() {
    unsubscribeTokens.forEach(function (token) {
      eventBus.unsubscribe(token);
    });
    unsubscribeTokens = [];
  }

  var setupNav = function () {

    var hideButton = $('button#hide-all');
    var showButton = $('button#show-all');

    // Set up buttons for navbar
    hideButton.click(function () {
      //      $('.filter-form .accordion-body').collapse('hide');
      eventBus.publish('hide all', 1);
    });
    showButton.click(function () {
      //      $('.filter-form .accordion-body').collapse('show');
      eventBus.publish('show all', 1);
    });
    // Resize the scrollable divs when the window is resized
    $(window).resize(function () {
      setNavHeight();
    });
  }

  var setNavHeight = function () {
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
      addSampleToggle.prop('disabled', false);

      $.post('/dashboard/add_samples_v2',
        postData, function (compId) {

          // Load filter forms
          /*
          $.get("/compare/" + compId + "/filter_forms",
          function(filterForms) {
          $('div#filter-forms').html(filterForms)
          refresh();
          });
          */

          // Update global comparisonId variable
          comparisonId = compId
          refresh();

          // Modify url bar
          // Should modify this javascript to use 
          // a django template tag for 'dashboard.views.compare_v2'
          window.history.pushState(null, '', '/compare/' + compId);
        });


    });

  }

  var enableTooltips = function () {
    $('[id^=tooltip]').popover();
  }

  var clonofilterColorsRefresh = function () {
    var url = '/compare/'+comparisonId+'/clonofilter_colors';
    $.get(url, function (d) {
      clonofilterColors.text(d);
    });
  }

  // Parses the cfid from a glyph, removes it and refreshes the 
  // filterform div
  var removeClonofilter = function() {
    cfId = $(this).attr('id').match(/\d+/)[0];
    postData = [{'name':'comparison', 'value': comparisonId},
    {'name':'clonofilter', 'value': cfId}];
    $.post('/dashboard/remove_clonofilter',
      postData, function (compId) {
        comparisonId = compId;
        window.history.pushState(null, '', '/compare/' + compId);
        // Load filter forms
        $.get("/compare/" + compId + "/filter_forms",
          function(filterForms) {
            $('div#filter-forms').html(filterForms)
            filterFormRefresh();
          });
      });
  }

  var filterFormRefresh = function () {
    var url = '/compare/'+comparisonId+'/filter_forms';
    $.get(url,
      function (d) {
        filterFormDiv.html(d);

        // Adds hide and show filter collapse functions to eventBus
        // Closures for show and hide event
        var showFilter = function (s, g, i) {
          var selection = s;
          var inner = i;
          var glyph = g;
          var show = function() {
            inner.collapse('show');
            glyph.removeClass('glyphicon-chevron-right');
            glyph.addClass('glyphicon-chevron-down');
          }
          return show;
        }

        var hideFilter = function (s, g, i) {
          var selection = s;
          var inner = i;
          var glyph = g;
          var hide = function() {
            inner.collapse('hide');
            glyph.removeClass('glyphicon-chevron-down');
            glyph.addClass('glyphicon-chevron-right');
          }
          return hide;
        }

        // binds close glyph icon to removeClonofilter function
        $('.glyphicon-remove').click(removeClonofilter);
        // Subscribe form filters to individual and global hide and show events
        $('.filter-form').each(function () {
          var cfid = $(this).attr('id').replace('filter-','');
          var glyph = $(this).find('span.toggle');
          var inner = $(this).find('div.filter-body');

          unsubscribeTokens.push(eventBus.subscribe('hide ' + cfid, hideFilter($(this), glyph, inner)));
          unsubscribeTokens.push(eventBus.subscribe('hide all', hideFilter($(this), glyph, inner)));
          unsubscribeTokens.push(eventBus.subscribe('show ' + cfid, showFilter($(this), glyph, inner)));
          unsubscribeTokens.push(eventBus.subscribe('show all', showFilter($(this), glyph, inner)));

          glyph.on("click", function() {
            console.log(glyph);
            if(glyph.hasClass('glyphicon-chevron-right')) {
              eventBus.publish('show ' + cfid, 1);
            }
            else {
              eventBus.publish('hide ' + cfid, 1);
            }
          });
        });

        // Hide all the filters on load (this fixes a bug that hides samples
          // when 'show all' event is initiated upon first loading
          eventBus.publish('hide all', 1);

          // Sets up an event to refresh when update is clicked
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
            unsubscribeTokens.push(eventBus.subscribe("activate " + cfid, function (selection) {
              selection.addClass('active');
            }));
            unsubscribeTokens.push(eventBus.subscribe("inactivate " + cfid, function (selection) {
              selection.removeClass('active');
            }));
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
  }

  var drawSpectratype = function () {
    navDiv.html('<img src="'+ajaxLoader+'">');
    d3.json('/compare/'+comparisonId+'/spectratype_ajax', function(d) {
      var specData = d;
      spectratypeDiv.datum(d);

      spectratypeDiv.html('');

      var spectratypePlot = spectratype().eventBus(eventBus);
      spectratypeDiv.call(spectratypePlot);
    });
  }

  var drawScatterNav = function() {
    var vdjFreq, vList, jList, sampleNames;
    navDiv.html('<img src="'+ajaxLoader+'">');

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
      .range([0, 40]);

      my_names = nameMap(sampleNames);

      navDiv.html('');

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
    functDiv.html('<img src="'+ajaxLoader+'">');
    d3.json('/compare/'+comparisonId+'/functionality_ajax', function(d) {
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
    // Load shared clones info from url
    //
    var sharedPage = parseInt(getURLParameter('shared_page')) || 1;
    var sharedPerPage = parseInt(getURLParameter('shared_perpage')) || 10;
    var sharedParams = $.param({
      'page': sharedPage,
      'per_page': sharedPerPage,
    });
    var url = '/compare/'+comparisonId+'/shared_clones_ajax?'+sharedParams;
    sharedClonesDiv.html('<img src="'+ajaxLoader+'">');
    console.log(url);

    // Make ajax query
    d3.json(url, function(d) {
      var aminoAcids = d3.map(d['aminoAcids'])
      var sampleNames = d['sampleNames']

      sharedClonesDiv.html('');

      var mySharedClones = sharedClones()
      .eventBus(eventBus);

      sharedClonesDiv
      .datum(aminoAcids.entries())
      .call(mySharedClones);

      // draw Shared Clones navigation
      var sharedNumPages = d['numPages'];
      var sharedCount = d['count'];

      var sharedClonesNav = sharedClonesDiv.append('div')
      .attr('id', 'shared-clones-nav');

      if (sharedPage > 1) {
        var prev_params = $.param({
          'shared_page': (sharedPage - 1),
          'shared_perpage': sharedPerPage,
        });
        sharedClonesNav.append('span')
        .html('<a href="?'+prev_params+'">Prev</a> ');
      }

      sharedClonesNav.append('span')
      .html('Page ' + sharedPage + 
      ' of ' + sharedNumPages);

    if (sharedPage < sharedNumPages) {
      var next_params = $.param({
        'shared_page': (sharedPage + 1),
        'shared_perpage': sharedPerPage,
      });

      sharedClonesNav.append('span')
      .html(' <a href="?'+next_params+'">Next</a>');
    }

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
