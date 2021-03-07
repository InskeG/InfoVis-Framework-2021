function createPlot() {
    var chart_group = svgContainer.append("g")
        .attr("id", "chart_group")
        .attr("transform", "translate(" + 100 + "," + 100 + ")");

    chart_group.append("g")
        .attr("transform", "translate(" + 0 + "," + chart_height + ")")
        .call(d3.axisBottom(x));

    chart_group.append("g")
        .call(d3.axisLeft(y));

    var map = d3.map(song_data);
    console.log(map.entries());
    chart_group.selectAll("#bar")
               .data(map.entries())
               .enter()
               .append("rect")
               .attr("class", "bar")
               .attr("x", function (d) { return x(d.key)})
               .attr("y", function (d) { return y(d.value * 100) })
               .attr("width", x.bandwidth() - 5)
               .attr("height", function(d) { return chart_height - y(d.value); })

}
