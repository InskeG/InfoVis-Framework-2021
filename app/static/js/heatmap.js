function createPlot() {
    var artists = d3.map(data, function(d){return d.artists;}).keys()
    var charact = d3.map(data, function(d){return d.characteristic;}).keys()
    var color_names = d3.map(colors, function(d){return d.characteristic;}).keys()

    // Build X scales and axis:
    var x = d3.scaleBand()
        .range([ 10, width_heatmap-10 ])
        .domain(charact)
        .padding(0.05);
    svg.append("g")
        .attr("class", "heatmap_x_axis")
        .attr("transform", "translate(0,0)")
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain").remove()

    // Build Y scales and axis:
    var width_transform = width_heatmap + 78;
    var y = d3.scaleBand()
        .range([ padding.top+5, fullheight - 20 ])
        .domain(artists)
        .padding(0.05);
    svg.append("g")
        .attr("class", "heatmap_y_axis")
        .attr("transform", "translate("+width_transform+",-8)")
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove()


    // Build color scale
    var myColor = d3.scaleLinear()
        .range(["#121212", "#1ED760"])
        .domain([0,1]);

    //create a tooltip
    var tooltip = d3.select("#heatmap")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")

    // Three functions that change the tooltip when user hovers / moves / leaves a cell
    var mouseover = function(d) {
        tooltip
            .style("opacity", 1)
    }

    var toValue = function(c, v) {
        if (c == "tempo") {
            return (v * 155.7211 + 31.7663).toFixed(1).toString() + " BPM"
        } else {
            return (v * 100).toFixed(1).toString() + "%"
        }
    }

    var mousemove = function(d) {
        tooltip
            .html("Average " + d.characteristic + " of " + d.artists + ":<br>" + toValue(d.characteristic,d.value))
            .style("left", (d3.mouse(this)[0] + 20) + "px")
            .style("top", (d3.mouse(this)[1] + 60) + "px")
    }

    var mouseleave = function(d) {
        tooltip
            .style("opacity", 0)
    }

    // add the squares
    let squares = svg.selectAll()
        .data(data, function(d) {return d.characteristic+':'+d.artists;})
        .enter()
        .append("rect")
            .attr("class", "heatmap_rect")
            .attr("x", function(d) { return x(d.characteristic) })
            .attr("y", function(d) { return y(d.artists) })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("width", x.bandwidth() )
            .attr("height", y.bandwidth() )
            //.style("fill", function(d) { return myColor(d.characteristic, d.value)} )
            .style("fill", function(d) { return myColor(d.value)} )
            .style("opacity", 0)
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)

    squares.transition()
        .duration(1000)
        .delay(function(d,i) { return Math.random() * 1200 } )
        .style("opacity", 1)


    //HEATMAP LEGEND
    const [color_begin,color_end] = myColor.range()
    var defs = svg.append("defs");
    var linearGradient = defs.append("linearGradient")
        .attr("id", "linear-gradient")

    linearGradient // determines whether legend is horizontal or vertical. For horizontal, change y2 => 0, x2 => 100%
        .attr("x1", "0%")
        .attr("x2", "100%")
        .attr("y1", "0%")
        .attr("y2", "0%")

    // begin
    linearGradient.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", color_begin)

    // end
    linearGradient.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", color_end)

    var svg2 = d3.select("#heatmap") // HTML tag
    .append("svg")
    .attr("width", width_heatmap+5)
    .attr("height", 40)
    .append("g")
    .attr("transform",
        "translate(10,0)");

    var legendScale = d3.scaleLinear()
        .domain([0, 1])
        .range([0,width_heatmap-padding.left-padding.left-5]);

    formatter =d3.format(".0%");

    svg2.append("g")
        .attr("class", "legend_axis")
        .attr("transform", "translate(0,14)")
        .call(d3.axisBottom(legendScale)
        .ticks(2)
        .tickFormat(formatter));

    svg2.append("rect")
        .attr("width", width_heatmap-padding.left-padding.left-5)
        .attr("height", "13")
        .style("fill", "url(#linear-gradient)")
        //.attr("stroke","#555");

}


