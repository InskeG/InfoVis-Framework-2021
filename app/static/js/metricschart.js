function addAxes(translation, id, chart_group, artist) {

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
        console.log(attr);
        console.log(x_2("1"));

        mini_chart_group.append("g")
        .attr("transform", "translate(" + 0 + "," + mini_chart_height / 2 + ")")
        .call(d3.axisBottom(x_2).tickFormat(""));

        mini_chart_group.selectAll("#bar")
        .data(map.entries())
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", function (d) { return x_2(d.key)})
        .attr("y", function (d) { return y_2(d.value[attr] * 100)  })
        .attr("width", x_2.bandwidth() - 5)
        .attr("height", function(d) { return (mini_chart_height / 2 - y_2(d.value[attr] * 100)) * 2; });

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
