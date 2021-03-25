function createHeatMapPlot() {
    var spotifyColor = "#1ED760";
    var charact = d3.map(heatmap_data, function(d){return d.characteristic;}).keys()
    var color_names = d3.map(colors, function(d){return d.characteristic;}).keys()
    chart_group_heatmap = svgHeatMap.append("g")
    				 .attr("class", "chart_group");

    // Build X scales and axis:
    var x = d3.scaleBand()
        .range([ 10, width_heatmap-10 ])
        .domain(charact)
        .padding(0.05);
    chart_group_heatmap.append("g")
        .attr("class", "heatmap_x_axis")
        .attr("transform", "translate(0,0)")
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain").remove();


    chart_group_heatmap.append("g")
        .attr("class", "heatmap_y_axis")
        .attr("transform", "translate("+width_transform+",-8)")
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove();


    // Build color scale
    var myColor = d3.scaleLinear()
        .range(["#121212", spotifyColor])
        .domain([0,1]);

    //create a tooltip


    // Three functions that change the tooltip when user hovers / moves / leaves a cell
    var mouseover = function(d) {
        tooltip
            .style("opacity", 1)
    }

    var toValue = function(c, v) {
        if (c == "tempo") {
            return (v * (max_temp - min_temp) + min_temp).toFixed(1).toString() + " BPM"
        } else {
            return (v * 100).toFixed(1).toString() + "%"
        }
    }

    var mousemove = function(d) {
        tooltip
            .html("Average " + d.characteristic + " of " + d.artists + ":<br />" + toValue(d.characteristic,d.value))
            .style("left", (d3.event.pageX + 20) + "px")
            .style("top", (d3.event.pageY - 60) + "px")
    }

    var mousemove_pop = function(d) {
        if (popularity[d][0]) {
            popul = popularity[d][0]
        } else {
            popul = popularity[d]
        }

        tooltip
            .html("Average popularity of " + d + ":<br />" + popul.toFixed(1) + "%")
            .style("left", (d3.event.pageX + 20) + "px")
            .style("top", (d3.event.pageY - 60) + "px")
    }

    var mouseleave = function(d) {
        tooltip
            .style("opacity", 0)
            .html(" ")
    }

    var pop_map = d3.map(popularity);
    var x_pop = d3.scaleLinear().range([0, 75]).domain([0, 100]);

    // console.log(pop_map)
    for (var pop_artist in popularity) {
        d3.select(".heatmap_y_axis").selectAll(".tick")
          .filter(function(d) { return d === pop_artist})
          .append("rect")
          .attr("x", "-40")
          .attr("y", "12")
          .attr("width", x_pop(popularity[pop_artist]))
          .attr("height", "10")
          .style("fill", spotifyColor)
          .attr("class", "popularity")
          .on("mouseover", mouseover)
          .on("mousemove", mousemove_pop)
          .on("mouseleave", mouseleave);

        d3.select(".heatmap_y_axis").selectAll(".tick")
          .filter(function(d) { return d === pop_artist})
          .append("rect")
          .attr("x", -40 + x_pop(popularity[pop_artist]))
          .attr("y", "12")
          .attr("width", 75 - x_pop(popularity[pop_artist]))
          .attr("height", "10")
          .style("fill", "darkGrey")
          .on("mouseover", mouseover)
          .on("mousemove", mousemove_pop)
          .on("mouseleave", mouseleave);
    }

    // add the squares
    chart_group_heatmap.selectAll()
        .data(heatmap_data, function(d) {return d.characteristic+':'+d.artists;})
        .enter()
        .append("rect")
            .attr("class", "heatmap_rect")
            .attr("x", function(d) { return x(d.characteristic) })
            .attr("y", function(d) { return y(d.artists) })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("width", x.bandwidth() )
            .attr("height", y.bandwidth() )
            .style("opacity", 1)
            .style("fill", function(d) { return myColor(d.value)} )
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)




    //HEATMAP LEGEND
    const [color_begin,color_end] = myColor.range()
    var defs = svgHeatMap.append("defs");
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


    var chart_group_heatmap_legend = svgLegendHeatMap.append("g")
    .attr("transform",
        "translate(10,0)")
    .attr("class", "chart_group");

    var legendScale = d3.scaleLinear()
        .domain([0, 1])
        .range([0,width_heatmap-padding.left-padding.left-5]);

    formatter = d3.format(".0%");

    chart_group_heatmap_legend.append("g")
        .attr("class", "legend_axis")
        .attr("transform", "translate(0,14)")
        .call(d3.axisBottom(legendScale)
        .ticks(2)
        .tickFormat(formatter));

    chart_group_heatmap_legend.append("rect")
        .attr("width", width_heatmap-padding.left-padding.left-5)
        .attr("height", "13")
        .style("fill", "url(#linear-gradient)")
        //.attr("stroke","#555");

    var chart_group_pop_legend = svgLegendPop.append("g")
    .attr("class", "chart_group");

    var legend_pop = chart_group_pop_legend.append("g")
    legend_pop.append("rect")
              .attr("x", "32")
              .attr("width", "75")
              .attr("height", "10")
              .style("fill", "darkGrey")

    legend_pop.append("text")
              .attr("x", "110")
              .attr("y", "7.5")
              .attr("dy", "0.1em")
              .attr("fill", "CurrentColor")
              .style("font-size", "70%")
              .html("0%");

    legend_pop = chart_group_pop_legend.append("g")
    legend_pop.append("rect")
              .attr("x", "32")
              .attr("y", "15")
              .attr("width", "75")
              .attr("height", "10")
              .style("fill", spotifyColor);

    legend_pop.append("text")
            .attr("x", "110")
            .attr("y", "22.5")
            .attr("dy", "0.1em")
            .attr("fill", "CurrentColor")
            .style("font-size", "70%")
            .html("100%");

}
