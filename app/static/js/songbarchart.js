function addToList(artist) {
    var artist_name = artist.replace(/[\s\.$]/g, '');
    var list_element = d3.select(".artist-list")
                         .append("li")
                         .attr("class", "artist-list-element")
                         .attr("id", "list" + artist_name);

    list_element.html(artist);
    var button = list_element.append("input")
                .attr("onClick", "removeArtist('" + artist + "')")
                .attr("class", "artist-list-button")
                .attr("type", "button")
                .attr("name", "delete" + artist_name)
                .attr("value", "x");

}

function addArtist(formObject) {
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
        var new_artist_barchart = data["barchart"];
        var new_artist_heatmap = data["heatmap"];
        var new_artist_popularity = data["popularity"];
        if (manual_artists) {
            y_variables.push(artist);
        } else {
            artist_offset = 0;
            y_to_i = {};
            manual_artists = true;
            barchart_data = {};
            heatmap_data = [];
            y_variables = [artist];
            d3.selectAll(".artist-list-element")
              .remove();
            popularity = {};
        }
        addToList(artist);
        y_to_i[artist] = artist_offset;
        artist_offset += 1;

        // if (mini_chart_height > 110) {
        //     mini_chart_height = 110;
        // }
        barchart_data = Object.assign({}, barchart_data, new_artist_barchart);
        popularity = Object.assign({}, popularity, new_artist_popularity);
        heatmap_data = heatmap_data.concat(new_artist_heatmap);

        remakePlot();
    });
    return false;
}

function filterArtists() {
    var fetch_url = "/filter_data?"

    for (var key_index in x_variables) {
        var key = x_variables[key_index];
        var min_string = "min_" + key;
        var max_string = "max_" + key;
        var min_key = characteristics_range[key].min;
        var max_key = characteristics_range[key].max;

        fetch_url = fetch_url + min_string + "=" + min_key + "&";
        fetch_url = fetch_url + max_string + "=" + max_key + "&";
    }

    fetch_url = fetch_url.slice(0, -1);

    fetch(fetch_url)
    .then(function(response) { return response.json(); })
    .then((data) => {
        barchart_data = data["barchart"];
        heatmap_data = data["heatmap"];
        popularity = data["popularity"];
        y_variables = data["artists"];

        artist_offset = 0;
        y_to_i = {};

        d3.selectAll(".artist-list-element")
        .remove();

        for (var key in y_variables) {
            var artist = y_variables[key];
    		y_to_i[artist] = artist_offset++;
            addToList(artist);
    	}

        if (manual_artists) {
            manual_artists = false;
        }

        remakePlot();
    });
    return false;
}

function removeArtist(artist) {
    var artist_selector = artist.replace(/[\s\.$]/g, '');
    if (!y_variables.includes(artist)) {
        d3.select("#list" + artist_selector)
            .remove();
        return;
    }
    if (!manual_artists) {
        manual_artists = true;
    }
    var j = y_to_i[artist];
    delete y_to_i[artist];
    for (var object_artist in y_to_i) {
        if (y_to_i[object_artist] > j) {
            y_to_i[object_artist]--;
        }
    }
    artist_offset -= 1;
    y_variables = y_variables.filter(function(value, index, arr) { return value != artist });
    delete barchart_data[artist];
    heatmap_data = heatmap_data.filter(function(value, index, arr) { return value.artists != artist });
    d3.select("#list" + artist_selector)
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
                                .attr("transform", "translate(0," + 16 + ")");


    for (var artist in barchart_data) {
        var n = y_to_i[artist];
        createRowChart(n * (mini_chart_height), n, chart_group_bar_charts, artist);
    }
}

function createRowChart(translation, id, chart_group_bar_charts, artist, colors) {
    var mini_artist_group = chart_group_bar_charts.append("g")
        .attr("id", "mini_artist_group" + id)
        .attr("transform", "translate(" + 35 + "," + (translation + 8) + ")");

    // Top x axis
    if (id === 0) {
        mini_artist_group.append("g")
                        .attr("id", "barChartAxisTop")
                        .call(d3.axisTop(x_1));
    }

    // Left -100 - 100 y axis, only show 0 - 100 ticks
    var yAxisTicks = y_2.ticks(5).filter(tick => tick >= 0);

    mini_artist_group.append("g")
        // .call(d3.axisLeft(y_2).ticks(3).tickFormat(function(x) { return x >= 0 ? x + "%" : ""; }));
           .call(d3.axisLeft(y_2).tickValues(yAxisTicks).tickSizeOuter(0));

    var data = barchart_data[artist]
    var map = d3.map(data);
    var j = 0;
    var line = d3.line();
    // Loop over all the attributes of songs
    for (var key_attr in x_variables) {
        // Create vertical separator lines
        if ((id === 0) && (j !== 0)) {
            var line_x = mini_chart_width * j + 30 + x_2.bandwidth() - 1;
            var points = [[line_x, 0], [line_x, mini_chart_height * y_variables.length]];
            chart_group_bar_charts.append("path")
                       .attr("class", "vertline")
                       .attr("transform", "translate(0,8)")
                       .attr("d", line(points))
       }
        var mini_chart_group = mini_artist_group.append("g")
            .attr("id", "mini_chart_group" + id + j)
            .attr("transform", "translate(" + (mini_chart_width * j) + "," + 0 + ")");

        createBarChart(x_variables, key_attr, map, mini_chart_group, artist);

        j += 1;
    }
}

function createBarChart(x_variables, key_attr, map, mini_chart_group, artist) {
    var attr = x_variables[key_attr];

    var bar_song_mouseover = function(d) {
        current_key = d.key;
        current_artist = d3.select(this).attr("artist");

        d3.selectAll(".bar_song")
            .each(function(d) {
                if (d.key != current_key || d3.select(this).attr("artist") != current_artist) {
                    d3.select(this).attr("class", "non_hover_bar")
                }
            });

        tooltip_bar
            .style("opacity", 1)
    }

    var toValue = function(c, v) {
        if (c == "tempo") {
            return (v * (max_temp_art - min_temp_art) + min_temp_art).toFixed(1).toString() + " BPM"
        } else {
            return (v * 100).toFixed(1).toString() + "%"
        }
    }

    var bar_song_mousemove = function(d) {
        current_key = d.key;
        current_artist = d3.select(this).attr("artist");

        tooltip_bar
            .html(d3.select(this).attr("artist") + " - " + d.value.name +
                "<table><tr><td>popularity:</td><td>" + d.value.popularity + ".0%</td></tr> <br />" +
                "<tr><td>" + x_variables[key_attr] + ":</td><td>" + toValue(x_variables[key_attr],d.value[attr]) + "</td></tr></table>")
            .style("left", (d3.event.pageX - 50) + "px")
            .style("top", (d3.event.pageY - 110) + "px")
    }

    var bar_song_mouseleave = function(d) {
        d3.selectAll(".non_hover_bar")
            .attr("class", "bar_song");
        tooltip_bar
            .style("opacity", 0)
            .html(" ");
    }

    // Horizontal axis for the bars
    mini_chart_group.append("g")
    .attr("transform", "translate(" + 0 + "," + mini_chart_height / 2 + ")")
    .attr("class", "rowChartAxis")
    .call(d3.axisBottom(x_2).tickFormat("").tickSize(0));

    // Creating the bars
    mini_chart_group.selectAll("#bar")
    .data(map.entries())
    .enter()
    .append("rect")
    .attr("x", function (d) { return x_2(d.key)})
    .attr("y", function (d) { return y_2(d.value[attr] * 100)  })
    .attr("width", x_2.bandwidth())
    .attr("height", function(d) { return (Math.max(mini_chart_height / 2 - y_2(d.value[attr] * 100), 0) * 2); })
    .attr("class", "bar_song")
    .attr("artist", artist)
    .on("mouseover", bar_song_mouseover)
    .on("mousemove", bar_song_mousemove)
    .on("mouseleave", bar_song_mouseleave);
    // .style("fill", function(d) { return myColor(attr, d.value[attr])} );

    var tooltip_bar = d3.select("#barchart")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip");
}
