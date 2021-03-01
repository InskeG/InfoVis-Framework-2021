function myColor(c, v) {
    var color_names = d3.map(colors, function(d){return d.characteristic;}).keys();

    color_min = colors[c].color_min;
    color_max = colors[c].color_max;

    var returned_color = d3.scaleLinear()
        .range([color_min, color_max])
        .domain([0,1]);

    return returned_color(v);
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

    // Left -100 - 100 y axis
    mini_artist_group.append("g")
        .call(d3.axisLeft(y_2).ticks(4));

    var data = song_data[artist]
    var map = d3.map(data);
    var j = 0;
    var line = d3.line();
    // Loop over all the attributes of songs
    for (var key_attr in x_variables) {
        if ((id === 0) && (j !== 0)) {
            var line_x = mini_chart_width * j + 30;
            var points = [[line_x, 0], [line_x, chart_height]];
            console.log(points);
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
        .style("fill", function(d) { return myColor(attr, d.value[attr])} );

        j += 1;
    }


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
