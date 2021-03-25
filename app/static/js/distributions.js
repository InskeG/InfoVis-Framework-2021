function createDistributionPlots(selected_char, svg) {

    //filter data on characteristic
    data = distplot_data.filter(function(element) {
        return element.characteristic === selected_char;
    })
    Promise.resolve(data).then(function(data) {

        // add the x Axis
        var x = d3.scaleLinear()
            .domain([0, 100])
            .range([0, width])


        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .attr("class", "displot_x_axis")
            .call(d3.axisBottom(x));

        // Compute kernel density estimation
        var kde = kernelDensityEstimator(kernelEpanechnikov(4), x.ticks(100))
        var density = kde(data.map(function(d) {
            return d.value * 100;
        }))
        //determine max height for graph
        var max_density = Math.max.apply(Math, density.map(function(o) {
            return o[1];
        }))
        // add y axis
        var y = d3.scaleLinear()
            .range([height, 0])
            .domain([0, max_density]);

        svg.append("g")
            .call(d3.axisLeft(y).ticks(5))
            .attr("class", "displot_y_axis");

        svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("class", "displot_y_text")
        .text(selected_char);


        // add area to fill graph
        var area = d3.area()
            .x(function(d) {
                return x(d[0]);
            })
            .y0(height)
            .y1(function(d) {
                return y(d[1]);
            });

        svg.append("path")
            .datum(density)
            .attr("class", "displot_area_fill")
            .attr("d", area);

        //add slider
        var sliderRange = d3
            .sliderBottom()
            .min(0)
            .max(100)
            .width(width)
            .ticks(1)
            .default([0, 100])
            .fill('#6c757d')
            .on('onchange', val => {
                d3.select('p#value-range').text(val.map(d3.format('.2%')).join('-'));
                characteristics_range[selected_char] = {"min":val[0],"max":val[1]}
            });

        var gRange = d3
            .select('#slider_' + selected_char)
            .append('svg')
            .attr('width', width + 50)
            .attr('height', slider_height)
            .append('g')
            .attr('transform', 'translate(30,5)');

        gRange.call(sliderRange);

        d3.select('#value-range').text(
            sliderRange
            .value()
            .map(d3.format('.2%'))
            .join('-')
        );

    });


    // Function to compute density
    function kernelDensityEstimator(kernel, X) {
        return function(V) {
            return X.map(function(x) {
                return [x, d3.mean(V, function(v) {
                    return kernel(x - v);
                })];
            });
        };
    }

    function kernelEpanechnikov(k) {
        return function(v) {
            return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
        };
    }

}