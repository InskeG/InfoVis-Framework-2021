import {select, selectAll} from 'd3-selection';
import Kapsule from 'kapsule';
import tinycolor from 'tinycolor2';
import {fitToBox} from 'svg-text-fit';
import {gradient} from 'svg-utils';

var ContinuousLegend = Kapsule({
    props: {
        width: {},
        height: {},
        scale: {},
        label: {}
    },
    init: function init(el, state) {
        state.gradient = gradient()(el);
        state.el = select(el); // Build dom

        state.box = state.el.append('rect').attr('x', 0).attr('y', 0).attr('rx', 3).attr('ry', 3).attr('stroke', 'black').attr('stroke-width', 0.5);
        state.unitLabel = state.el.append('text').attr('class', 'legendText').style('text-anchor', 'middle').style('dominant-baseline', 'central');
        state.labelFitText = fitToBox()(state.unitLabel.node());
        state.startLabel = state.el.append('text').style('text-anchor', 'start').style('dominant-baseline', 'central');
        state.startLabelFitText = fitToBox()(state.startLabel.node());
        state.endLabel = state.el.append('text').style('text-anchor', 'end').style('dominant-baseline', 'central');
        state.endLabelFitText = fitToBox()(state.endLabel.node());
    },
    update: function update(state) {
        state.gradient.colorScale(state.scale);
        state.box.attr('width', state.width).attr('height', state.height).style('fill', "url(#".concat(state.gradient.id(), ")"));
        state.unitLabel.text(state.label).attr('x', state.width * 0.5).attr('y', state.height * 0.5).style('text-anchor', 'middle').style('dominant-baseline', 'central').style('fill', tinycolor(state.scale((state.scale.domain()[state.scale.domain().length - 1] - state.scale.domain()[0]) / 2)).isLight() ? '#444' : '#CCC');
        state.labelFitText.bbox({
            width: state.width * 0.8,
            height: state.height * 0.9
        });
        state.startLabel.text(state.scale.domain()[0]).attr('x', state.width * 0.02).attr('y', state.height * 0.5).style('fill', tinycolor(state.scale(state.scale.domain()[0])).isLight() ? '#444' : '#CCC');
        state.startLabelFitText.bbox({
            width: state.width * 0.3,
            height: state.height * 0.7
        });
        state.endLabel.text(state.scale.domain()[state.scale.domain().length - 1]).attr('x', state.width * 0.98).attr('y', state.height * 0.5).style('fill', tinycolor(state.scale(state.scale.domain()[state.scale.domain().length - 1])).isLight() ? '#444' : '#CCC');
        state.endLabelFitText.bbox({
            width: state.width * 0.3,
            height: state.height * 0.7
        });
    }
});

var DiscreteLegend = Kapsule({
    props: {
        width: {},
        height: {},
        scale: {},
        label: {},
        onLegendClick: {}
    },
    init: function init(el, state) {
        state.el = select(el);
    },
    update: function update(state) {
        let filters = [];
        if (!select(`.series-segment.disabled`).empty()) {
            selectAll(`.series-segment:not(.disabled)`)
                .each((s) => !filters.includes(s.val) && filters.push(s.val));
        }

        var colorBinWidth = state.width / state.scale.domain().length;
        var slot = state.el.selectAll('.color-slot').data(state.scale.domain());
        slot.exit().remove();

        var newSlot = slot.enter()
            .append('g')
            .attr('class', (d) => `color-slot ${d}`)
            .style('fill-opacity', (d) => filters.length && !filters.includes(d) ? .2 : 1);

        newSlot.append('rect').attr('y', 0).attr('rx', 0).attr('ry', 0).attr('stroke-width', 0);
        newSlot.append('text').style('text-anchor', 'middle').style('dominant-baseline', 'central');
        newSlot.append('title'); // Update

        slot = slot.merge(newSlot);

        if (state.onLegendClick) {
            state.el.selectAll('.color-slot').selectAll('text').style('cursor', 'pointer')
                .on('click', s => state.onLegendClick(s.target));
        }

        slot.select('rect').attr('width', colorBinWidth).attr('height', state.height).attr('x', function (d, i) {
            return colorBinWidth * i;
        }).attr('fill', function (d) {
            return state.scale(d);
        });
        slot.select('text').text(function (d) {
            return d;
        }).attr('x', function (d, i) {
            return colorBinWidth * (i + .5);
        }).attr('y', state.height * 0.5).style('fill', function (d) {
            return tinycolor(state.scale(d)).isLight() ? '#333' : '#DDD';
        }).each(function () {
            fitToBox().bbox({
                width: colorBinWidth * 0.9,
                height: state.height * 0.8
            })(this);
        });
        slot.select('title').text(function (d) {
            return "".concat(d, " ").concat(state.label);
        });
    }
});

var legend = Kapsule({
    props: {
        width: {},
        height: {},
        scale: {},
        label: {},
        onLegendClick: {}
    },
    init: function init(el, state) {
        state.legend = select(el).append('g').attr('class', 'legend');
    },
    update: function update(state) {
        if (!state.scale) return; // Check if ordinal or continuous scale

        var isOrdinal = !state.scale.hasOwnProperty('interpolate') && !state.scale.hasOwnProperty('interpolator'); // Only continuous scales can be interpolated

        state.legend.html(''); // Wipe it

        (isOrdinal ? DiscreteLegend : ContinuousLegend)().width(state.width).height(state.height).scale(state.scale).label(state.label).onLegendClick(state.onLegendClick)(state.legend.node());
    }
});

export default legend;
