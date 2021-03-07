function myColor(c, v) {
    var color_names = d3.map(colors, function(d){return d.characteristic;}).keys();

    color_min = colors[c].color_min;
    color_max = colors[c].color_max;

    var returned_color = d3.scaleLinear()
        .range([color_min, color_max])
        .domain([0,1]);

    return returned_color(v);
}

function addArtist(formObject) {
    var new_artist;
    var artist = formObject.artist.value;
    var fetch_url = "/metrics_data?artist=" + artist;
    fetch(fetch_url)
    .then(function(response) { return response.json(); })
    .then((data) => {
        if (Object.keys(data).length === 0 && data.constructor === Object) {
            return false;
        }
        new_artist = data;
        if (manual_artists) {
            if (y_variables.includes(artist)) {
                return false;
            }
            y_variables.push(artist);
        } else {
            i = 0;
            y_to_i = {};
            manual_artists = true;
            song_data = {};
            y_variables = [artist];
        }
        y_to_i[artist] = i++;
        var num_artists = y_variables.length;
        mini_chart_height = chart_height / num_artists;
        if (mini_chart_height > 110) {
            mini_chart_height = 110;
            y_1 = d3.scaleBand().rangeRound([0, mini_chart_height * num_artists])
        }
        y_1.domain(y_variables);
        song_data = Object.assign({}, song_data, new_artist)
        removeOldPlot();
        createPlot();
    });
    return false;
}

function removeOldPlot() {
    d3.select("#chart_group")
      .remove();
}

function createPlot() {
    var chart_group = svgContainer.append("g")
        .attr("id", "chart_group")
        .attr("transform", "translate(" + 100 + "," + 20 + ")");

    chart_group.append("g")
        .call(d3.axisLeft(y_1).tickSize(0))
        .select(".domain").remove();

    for (var artist in song_data) {
        var i = y_to_i[artist];
        addAxes(i * (mini_chart_height), i, chart_group, artist);
    }
}

function addAxes(translation, id, chart_group, artist, colors) {

    var mini_artist_group = chart_group.append("g")
        .attr("id", "mini_artist_group" + id)
        .attr("transform", "translate(" + 30 + "," + (translation) + ")");

    // Top x axis
    if (id === 0) {
        mini_artist_group.append("g")
                        .call(d3.axisTop(x_1));
    }

    // Left -100 - 100 y axis, only show 0 - 100 ticks
    mini_artist_group.append("g")
        .call(d3.axisLeft(y_2).ticks(5).tickFormat(function(x) { return x >= 0 ? x + "%" : ""; }));

    var data = song_data[artist]
    var map = d3.map(data);
    var j = 0;
    var line = d3.line();
    // Loop over all the attributes of songs
    for (var key_attr in x_variables) {
        if ((id === 0) && (j !== 0)) {
            var line_x = mini_chart_width * j + 30;
            var points = [[line_x, 0], [line_x, mini_chart_height * y_variables.length]];
            chart_group.append("path")
                       .attr("class", "vertline")
                       .attr("d", line(points))
                       .attr("stroke", "lightgrey");
       }
        var mini_chart_group = mini_artist_group.append("g")
            .attr("id", "mini_chart_group" + id + j)
            .attr("transform", "translate(" + (mini_chart_width * j) + "," + 0 + ")");

        // Vertical bar inbetween the charts
        // mini_chart_group.append("g")
        //     .call(d3.axisLeft(y_2).ticks([]));

        var attr = x_variables[key_attr];

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
        .attr("width", x_2.bandwidth() - 5)
        .attr("height", function(d) { return (mini_chart_height / 2 - y_2(d.value[attr] * 100)) * 2; })
        .attr("class", "bar");
        // .style("fill", function(d) { return myColor(attr, d.value[attr])} );

        j += 1;
    }
}
