function createPlot() {
    var artists = d3.map(data, function(d){return d.artists;}).keys()
    var charact = d3.map(data, function(d){return d.characteristic;}).keys()
    var color_names = d3.map(colors, function(d){return d.characteristic;}).keys()

    // Build X scales and axis:
    var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(charact)
        .padding(0.05);
    svg.append("g")
        .attr("class", "heatmap_x_axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain").remove()

    // Build Y scales and axis:
    var y = d3.scaleBand()
        .range([ 0, height ])
        .domain(artists)
        .padding(0.05);
    svg.append("g")
        .attr("class", "heatmap_y_axis")
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove()

    // Build color scale
    //var myColor = d3.scaleLinear()
        //.range(["#f9e3f8", "#a4249e"])
        //.domain([0,1]);
    var myColor = function(c, v) {
        color_min = "#f9e3f8";
        color_max = "#a4249e";
        for (i = 0; i < 9; i++) {
            if (c == color_names[i]) {
                color_min = colors[i].color_min;
                color_max = colors[i].color_max;
            }
        }

        var returned_color = d3.scaleLinear()
            .range([color_min, color_max])
            .domain([0,1])

        return returned_color(v)
    }

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
            .style("left", (d3.mouse(this)[0] + 250) + "px")
            .style("top", (d3.mouse(this)[1] + 50) + "px")
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
            .style("fill", function(d) { return myColor(d.characteristic, d.value)} )
            .style("opacity", 0)
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)

    squares.transition()
        .duration(1000)
        .delay(function(d,i) { return Math.random() * 1200 } )
        .style("opacity", 0.8)
}


