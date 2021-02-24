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

    if (id === 0) {
        mini_artist_group.append("g")
                        .call(d3.axisTop(x_1));
    }

    mini_artist_group.append("g")
        .call(d3.axisLeft(y_2).ticks(4));

    var data = song_data[artist]
    var map = d3.map(data);
    // var stackGen = d3.stack()
    //               .keys(x_variables)
    //               .order(d3.stackOrderNone)
    //               .offset(d3.stackOffsetNone);
    // console.log(song_data[artist]);
    // var stack = stackGen(song_data[artist]);
    var j = 0;
    for (var key_attr in x_variables) {
        var mini_chart_group = mini_artist_group.append("g")
            .attr("id", "mini_chart_group" + id + j)
            .attr("transform", "translate(" + (mini_chart_width * j) + "," + 0 + ")");

        mini_chart_group.append("g")
            .call(d3.axisLeft(y_2).ticks([]));

        var attr = x_variables[key_attr];

        mini_chart_group.append("g")
        .attr("transform", "translate(" + 0 + "," + mini_chart_height / 2 + ")")
        .call(d3.axisBottom(x_2).tickFormat(""));

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
        // .attr("transform", "translate(0," + 20 + ")")
        .select(".domain").remove();

    var i = 0;
    for (var artist in song_data) {
        addAxes(i * (mini_chart_height), i, chart_group, artist);
        i += 1;
        // console.log(song_data[artist]);
    }

    // for (var i = 0; i < 9; i++) {
    //     addAxes(i * (chart_height + 15) + 10, i);
    // }

    // var map = d3.map(song_data);
    // console.log(map.entries());
    // chart_group.selectAll("#bar")
    //            .data(map.entries())
    //            .enter()
    //            .append("rect")
    //            .attr("class", "bar")
    //            .attr("x", function (d) { return x(d.key)})
    //            .attr("y", function (d) { return y(d.value) })
    //            .attr("width", x.bandwidth() - 5)
    //            .attr("height", function(d) { return chart_height - y(d.value); })

}
