  $(function() {


    $.getJSON(
    '{% url 'dashboard.views.menu_json' %}',
    function(data) {
      // Get csrf token
      var csrftoken = $.cookie('csrftoken');

      // set header
      function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      }
      function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
      }
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        }
      });

      // build jqTree
      var $tree = $('#tree1');
      $tree.tree({
        data: data,
      });

      // Gets and loads a comparison id

      // submit array of primary keys to add_samples view
      $(":button").click(function() {
        $selectedNodes = $tree.tree('getSelectedNodes');
        var selectedNodeKeys = [];
        $.each($selectedNodes, function(index, node) {
          selectedNodeKeys.push(node.pk);
        });
        if (selectedNodeKeys.length  > 1) {
          console.log(JSON.stringify(selectedNodeKeys))
          $.post("{% url 'dashboard.views.add_samples' %}", {
            sample_ids: JSON.stringify(selectedNodeKeys),
            }, function(comparison_id) {
            $('div#main').html("<img src=/static/img/ajax-loader.gif>");
            $.get("/compare/" + comparison_id, function(comparison) {
              $('div#main').html(comparison)
            });
            $.get("/compare/" + comparison_id + "/filter_forms",
            function(filter_forms_html) {
              $('div#filter_forms_div').html(filter_forms_html)
            });
            $('a#filter_form_toggle').click()
            
            var stateObj = { foo: "bar" };
            console.log(stateObj);
            history.pushState(stateObj, "comparison" + comparison_id,
            "dashboard/compare/"+comparison_id);
            console.log(stateObj);

          });
        }
        else {
          alert("Please select more than one sample for comparison");
        }

      });

      // modify default tree behavior
      $tree.bind('tree.click',
      function(e) {
        e.preventDefault();
        var selected_node = e.node;

        if($tree.tree('isNodeSelected', selected_node)) {
          $tree.tree('removeFromSelection', selected_node);
        }
        else {
          if(selected_node.children.length == 0) {
            $tree.tree('addToSelection', selected_node);
          }
        }

        if(!selected_node.is_open) {
          $tree.tree('toggle', selected_node);
          $.each(selected_node.children, function(index, child_node) {
            $tree.tree('addToSelection', child_node);
          });
        }
        else {
          var num_selected_children = 0;
          $.each(selected_node.children, function(index, child_node) {
            if($tree.tree('isNodeSelected', child_node)) {
              num_selected_children++;
            }
          });
        }
        if (num_selected_children == selected_node.children.length) {
          $.each(selected_node.children, function(index, child_node) {
            $tree.tree('removeFromSelection', child_node);
          });
        }
        else {
          $.each(selected_node.children, function(index, child_node) {
            $tree.tree('addToSelection', child_node);
          });
        }
      });
      console.log(data);
    }
    );
  });

