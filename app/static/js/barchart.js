function get_info_on_var(variable) {
    var rel_meta = meta_data.find(function(d) {
        return d.Variabele == variable;
    })

    var label = rel_meta['Label_1'];
    var definition = rel_meta['Definition'];

    return [label, definition]
}

function updateArea(selectObject) {
    selected_area = selectObject.value;
    updatePlot();
};

function updatePlot() {
    var fetch_url = "/d3_plot_data?area_name=" + selected_area;
    fetch(fetch_url)
        .then(function(response) { return response.json(); })
        .then((data) => {
            plot_data = data;
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
        .call(d3.axisBottom(x));
        // Code for vertical bar chart
        // .selectAll("text")
        // .attr("y", 0)
        // .attr("x", 9)
        // .attr("transform", "rotate(90)")
        // .style("text-anchor", "start");

    chart_group.append("g")
        .call(d3.axisLeft(y));

    var map = d3.map(plot_data[0]); 

    chart_group.selectAll(".bar")
    .data(map.entries())
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("x", 1)
    .attr("y", function (d) { return y(d.key) })
    .attr("width", function(d) { return x(d.value); })
    .attr("height", y.bandwidth())
    .on("mouseover", function(d, i) {
        var x_var = d.key;
        var value = d.value;
        var info = get_info_on_var(x_var);
        var label = info[0]
        var definition = info[1];

        displayTooltip("<b>Variable: </b>" + label + "<br /><b>Percentage: </b>" + 
            value + "%<br /><b>Explanation: </b>" + definition)

        //d3.select(this).attr("fill", "DarkOrange");
    })
    .on("mousemove", function(d, i) {
        var x_var = d.key;
        var value = d.value;
        var info = get_info_on_var(x_var);
        var label = info[0]
        var definition = info[1];

        displayTooltip("<b>Variable: </b>" + label + "<br /><b>Percentage: </b>" + 
            value + "%<br /><b>Explanation: </b>" + definition)

        //d3.select(this).attr("fill", "DarkOrange");
    })
    .on("mouseout", function(d) {
        hideTooltip();
        //d3.select(this).attr("fill", "steelblue");
    });

    // text label for the x axis
    svgContainer.append("text")             
    .attr("transform",
            "translate(" + (width/2 - (100/2)) + " ," + 
                        (chart_height + 100) + ")")
    .style("text-anchor", "middle")
    .style("font-size", "13px")
    .text("Percentage");

    chart_group.append("text")
            .attr("class", "title")
            .attr("id", "chart-title")
            .attr("y", -25)
            .attr("x", chart_width / 2)
            .style("font-weight", "bold")               
            .style("text-anchor", "middle")
            .text("Rental statistics of " + selected_area);

    // Code for vertical bar chart
    // chart_group.selectAll(".bar")
    //     .data(map.entries())
    //     .enter()
    //     .append("rect")
    //     .attr("class", "bar")
    //     .attr("x", function (d) { return x(d.key)})
    //     .attr("y", function (d) { return y(d.value) })
    //     .attr("width", x.bandwidth())
    //     .attr("height", function(d) { return chart_height - y(d.value); })
    //     .on("mouseover", function(d, i) {
    //         var x_var = d.key;
    //         var value = d.value;
    //         var info = get_info_on_var(x_var);
    //         var label = info[0]
    //         var definition = info[1];

    //         displayTooltip("<b>Variable: </b>" + label + "<br /><b>Percentage: </b>" + 
    //             value + "%<br /><b>Explanation: </b>" + definition)

    //         //d3.select(this).attr("fill", "DarkOrange");
    //     })
    //     .on("mousemove", function(d, i) {
    //         var x_var = d.key;
    //         var value = d.value;
    //         var info = get_info_on_var(x_var);
    //         var label = info[0]
    //         var definition = info[1];

    //         displayTooltip("<b>Variable: </b>" + label + "<br /><b>Percentage: </b>" + 
    //             value + "%<br /><b>Explanation: </b>" + definition)

    //         //d3.select(this).attr("fill", "DarkOrange");
    //     })
    //     .on("mouseout", function(d) {
    //         hideTooltip();
    //         //d3.select(this).attr("fill", "steelblue");
    //     });

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
