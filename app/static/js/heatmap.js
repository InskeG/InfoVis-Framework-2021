function createPlot() {
    var artists = d3.map(data, function(d){return d.artists;}).keys()
    var charact = d3.map(data, function(d){return d.characteristic;}).keys()

    // Build X scales and axis:
    var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(charact)
        .padding(0.05);
    svg.append("g")
        .style("font-size", 10)
        .style('color', '#fff')
        //.style('stroke', '#4523ff')
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain").remove()

    // Build Y scales and axis:
    var y = d3.scaleBand()
        .range([ 0, height ])
        .domain(artists)
        .padding(0.05);
    svg.append("g")
        .style("font-size", 12)
        .style('color', '#fff')
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove()

    // Build color scale
    var myColor = d3.scaleLinear()
        .range(["#f9e3f8", "#a4249e"])
        .domain([0,1]);

    // add the squares
    svg.selectAll()
        .data(data, function(d) {return d.characteristic+':'+d.artists;})
        .enter()
        .append("rect")
              .attr("x", function(d) { return x(d.characteristic) })
              .attr("y", function(d) { return y(d.artists) })
              .attr("rx", 4)
              .attr("ry", 4)
              .attr("width", x.bandwidth() )
              .attr("height", y.bandwidth() )
              .style("fill", function(d) { return myColor(d.value)} )
              .style("stroke-width", 4)
              .style("stroke", "none")
              .style("opacity", 0.8)
}


