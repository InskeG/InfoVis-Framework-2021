
function addToList(artist) {
    var list_element = d3.select(".artist-list")
                         .append("li")
                         .attr("class", "artist-list-element")
                         .attr("id", "list" + artist.replace(/\s/g, ''));

    list_element.html(artist);
    var button = list_element.append("button")
                .attr("onClick", "removeArtist('" + artist + "')")
                .attr("class", "artist-list-button")
                .attr("type", "button")
                .attr("name", "delete" + artist.replace(/\s/g, ''));

    button.html("x");
}

function addArtist(formObject) {
    var new_artist_barchart;
    var artist = formObject.artist.value;
    var fetch_url = "/metrics_data?artist=" + artist;
    if (manual_artists && (y_variables.includes(artist) || y_variables.length == 10)) {
        return false;
    }
    fetch(fetch_url)
    .then(function(response) { return response.json(); })
    .then((data) => {
        if (Object.keys(data).length === 0 && data.constructor === Object) {
            return false;
        }
        new_artist_barchart = data["barchart"];
        new_artist_heatmap = data["heatmap"];
        console.log(new_artist_heatmap);
        if (manual_artists) {
            y_variables.push(artist);
        } else {
            i = 0;
            y_to_i = {};
            manual_artists = true;
            barchart_data = {};
            heatmap_data = [];
            y_variables = [artist];
            d3.selectAll(".artist-list-element")
              .remove();
        }
        addToList(artist);
        y_to_i[artist] = i++;

        // if (mini_chart_height > 110) {
        //     mini_chart_height = 110;
        // }
        barchart_data = Object.assign({}, barchart_data, new_artist_barchart);
        heatmap_data = heatmap_data.concat(new_artist_heatmap);

        remakePlot();
    });
    return false;
}

function removeArtist(artist) {
    if (!y_variables.includes(artist)) {
        console.log("cannot find artist");
        return;
    }
    console.log("found artist");
    var j = y_to_i[artist];
    delete y_to_i[artist];
    for (var object_artist in y_to_i) {
        if (y_to_i[object_artist] > j) {
            y_to_i[object_artist]--;
        }
    }
    i--;
    y_variables = y_variables.filter(function(value, index, arr) { return value != artist });
    console.log(y_variables);
    delete barchart_data[artist];
    heatmap_data = heatmap_data.filter(function(value, index, arr) { return value.artists != artist });
    d3.select("#list" + artist.replace(/\s/g, ''))
      .remove();

    remakePlot();
}

function remakePlot() {
    var num_artists = y_variables.length;

    y = d3.scaleBand()
        .range([padding.top + 5, (fullheight - 20) / 10 * num_artists])
        .domain(y_variables)
        .padding(0.05);

    removeOldPlot();
    createHeatMapPlot();
    createBarChartPlot();
}

function removeOldPlot() {
    d3.selectAll(".chart_group")
      .remove();
}

function createBarChartPlot() {
    var chart_group_bar_charts = svgBarCharts.append("g")
                                .attr("class", "chart_group")
                                .attr("transform", "translate(0," + 20 + ")");

    for (var artist in barchart_data) {
        var n = y_to_i[artist];
        createRowChart(n * (mini_chart_height), n, chart_group_bar_charts, artist);
    }
}

function createRowChart(translation, id, chart_group_bar_charts, artist, colors) {
    var mini_artist_group = chart_group_bar_charts.append("g")
        .attr("id", "mini_artist_group" + id)
        .attr("transform", "translate(" + 35 + "," + (translation) + ")");

    // Top x axis
    if (id === 0) {
        mini_artist_group.append("g")
                        .call(d3.axisTop(x_1));
    }

    // Left -100 - 100 y axis, only show 0 - 100 ticks
    mini_artist_group.append("g")
        .call(d3.axisLeft(y_2).ticks(5).tickFormat(function(x) { return x >= 0 ? x + "%" : ""; }));

    var data = barchart_data[artist]
    var map = d3.map(data);
    var j = 0;
    var line = d3.line();
    // Loop over all the attributes of songs
    for (var key_attr in x_variables) {
        // Create vertical separator lines
        if ((id === 0) && (j !== 0)) {
            var line_x = mini_chart_width * j + 30;
            var points = [[line_x, 0], [line_x, mini_chart_height * y_variables.length]];
            chart_group_bar_charts.append("path")
                       .attr("class", "vertline")
                       .attr("d", line(points))
                       .attr("stroke", "lightgrey");
       }
        var mini_chart_group = mini_artist_group.append("g")
            .attr("id", "mini_chart_group" + id + j)
            .attr("transform", "translate(" + (mini_chart_width * j) + "," + 0 + ")");

        createBarChart(x_variables, key_attr, map, mini_chart_group);

        j += 1;
    }
}

function createBarChart(x_variables, key_attr, map, mini_chart_group) {
    var attr = x_variables[key_attr];

    // var mouseover = function(d) {
    //     tooltip
    //         .style("opacity", 1)
    // }
    //
    // var toValue = function(c, v) {
    //     if (c == "tempo") {
    //         return (v * 155.7211 + 31.7663).toFixed(1).toString() + " BPM"
    //     } else {
    //         return (v * 100).toFixed(1).toString() + "%"
    //     }
    // }
    // console.log(attr)
    // var mousemove = function(d) {
    //     tooltip
    //         .html("Value of " + attr + " of song " + d.key + ":<br>" + toValue(attr, d.value[attr]))
    //         .style("left", (d3.event.pageX + 20) + "px")
    //         .style("top", (d3.event.pageY - 60) + "px")
    // }
    //
    // var mouseleave = function(d) {
    //     tooltip
    //         .style("opacity", 0)
    // }


    // Horizontal axis for the bars
    mini_chart_group.append("g")
    .attr("transform", "translate(" + 0 + "," + mini_chart_height / 2 + ")")
    .call(d3.axisBottom(x_2).tickFormat(""));

    // Creating the bars
    mini_chart_group.selectAll("#bar")
    .data(map.entries())
    .enter()
    .append("rect")
    .attr("x", function (d) { return x_2(d.key)})
    .attr("y", function (d) { return y_2(d.value[attr] * 100)  })
    .attr("width", x_2.bandwidth() - 1)
    .attr("height", function(d) { return (mini_chart_height / 2 - y_2(d.value[attr] * 100)) * 2; })
    .attr("class", "bar");
    // .on("mouseover", mouseover)
    // .on("mousemove", mousemove)
    // .on("mouseleave", mouseleave);
    // .style("fill", function(d) { return myColor(attr, d.value[attr])} );
}
