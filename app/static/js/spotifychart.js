function updatePlot() {
    var fetch_url = "/d3_plot_data";
    fetch(fetch_url)
        .then(function(response) { return response.json(); })
        .then((data) => {
            song_data = data;
            removeOldChart();
            createNewChart();
    });
}

function removeOldChart() {
    d3.select("#chart_group")
        .remove();
}

function createNewChart() {
    var chart_group = svgContainer.append("g")
        .attr("id", "chart_group")
        .attr("transform", "translate(" + 100 + "," + 50 + ")");


    chart_group.append("g")
        .attr("transform", "translate(" + 0 + "," + chart_height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("transform", "rotate(90)")
        .style("text-anchor", "start");
        // Code for vertical bar chart

    chart_group.append("g")
        .call(d3.axisLeft(y));

    var map = d3.map(song_data);

    chart_group.selectAll(".bar")
                .data(map.entries())
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", function (d) { return x(d.name)})
                .attr("y", function (d) { return y(d.valence) })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return chart_height - y(d.valence); })

    // text label for the x axis
    svgContainer.append("text")
                .attr("transform",
                        "translate(" + 50 + " ," +
                                    (chart_height / 2) + ")")
                .style("text-anchor", "middle")
                .style("font-size", "13px")
                .text("ratio");

    chart_group.append("text")
            .attr("class", "title")
            .attr("id", "chart-title")
            .attr("y", -25)
            .attr("x", chart_width / 2)
            .style("font-weight", "bold")
            .style("text-anchor", "middle")
            .text("Song data for Michael Jackson");

    // Code for vertical bar chart

};



/////////////////////////////////////////////////////////////////
//////// EXAMPLE CODE FOR DIFFERENT SHAPE ELEMENTS IN D3 ////////

// var circle = svgContainer.append("circle")
// 						.attr("cx", 30)
// 						.attr("cy", 30)
// 						.attr("r", 20);

//  var rectangle = svgContainer.append("rect")
// 							.attr("x", 10)
// 							.attr("y", 10)
// 							.attr("width", 50)
// 							.attr("height", 100);


// var ellipse = svgContainer.append("ellipse")
// 							.attr("cx", 50)
// 							.attr("cy", 50)
// 							.attr("rx", 25)
// 							.attr("ry", 10)
// 							.attr("fill", "red")
// 							.attr("id", "ellipse");

// d3.select("#ellipse").attr("fill","green");


// var line = svgContainer.append("line")
//                          .attr("x1", 5)
//                          .attr("y1", 5)
//                          .attr("x2", 50)
//                          .attr("y2", 50)
//                          .attr("stroke-width", 2)
//                          .attr("stroke", "blue");

// var arc = d3.arc()
//     .innerRadius(40)
//     .outerRadius(100)
//     .startAngle(0)
//     .endAngle(3);

// svgContainer.append("path")
// 	.attr("transform", "translate(" + 100 + "," + 100 + ")")
//     .attr("d", arc)
//     .attr("fill", "red")
//     .attr("class", "arc")
//     .on("click", function(d) {
//     	d3.select(".arc").attr("fill","blue");
//     });

/////////////////////////////////////////////////////////////////
