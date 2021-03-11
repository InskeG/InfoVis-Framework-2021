from data import *;

<template>
  <div>
    <vs-row type="flex" vs-justify="center" vs-align="center">
      <vs-card class="cardx" v-if="fetched.img_generated" fixedHeight vs-w="12">
        <div slot="media">
          <img v-bind:src="image">
        </div>
      </vs-card>
    </vs-row>

    <vs-row vs-justify="center">
      <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
        <vs-card class="cardx" v-if="fetched.more_statistics">
          <div slot="header"><h3>Meer statistieken</h3></div>
          <div>
            alskjhd lksjh sfajkh asjfh lkasfh
            Kijk deze krab nou. Zie hem krabben alsof er geen morgen is.
            Een ware inspiratie voor iedere liefhebber van geleedpotigen.
          </div>
        </vs-card>

        <vs-card class="cardx" v-if="fetched.col_generated">
          <div slot="header"><h3>Dominant Colors</h3></div>

          <div>
            <div id="app">
              <pie-chart
                :data="pie_data"
                :key="pie_key"
              />
            </div>
            <div id="my_dataviz"></div>
          </div>
        </vs-card>

        <vs-card class="cardx" v-if="fetched.artist_options" >
          <div slot="header"><h3>Dominant colors in art pieces over the years for specific artists</h3></div>

          <select v-model="selected" @change="get_line_graph()">
            <option v-for="option in artist_options" v-bind:key="option"> {{ option }}</option>
          </select>

          <zingchart
            ref="line_chart"
            :data="line_chart_data"
            :key="chart_key"
            @node_mouseover="handleNodeHighlight"
          />
        </vs-card>
      </vs-col>

      <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
        <vs-card class="cardx" v-if="fetched.summary">
          <div slot="header"><h3>{{ genre }} on Wikipedia</h3></div>
          <div>
            {{ summary }}
          </div>
        </vs-card>

        <vs-card class="cardx" v-if="fetched.related_terms">
          <div slot="header"><h3>Related terms</h3></div>
          <div>
            {{ related_terms }}
          </div>
        </vs-card>

        <vs-card class="cardx">
          <div slot="header"><h3>Usage of dominant colors by genres</h3></div>
          <zingchart
          ref="style_hist"
          :data="style_hist_data"
          :key="hist_key"
        />
        </vs-card>
      </vs-col>
    </vs-row>


    <vs-row type="flex" vs-justify="center" vs-align="center" vs-w="12">
      <vs-card class="cardx">
        <div slot="header">
            <h3>Pick a <span v-if="fetched.img_generated">new</span> style!</h3>
        </div>
        <div class="mt-3" id="timeline">
            Painting happy little trees...
        </div>
        <div class="d-flex align-items-center dropdownbtn-alignment">
          <vs-dropdown vs-trigger-click>
            <vs-button
              class="btn-alignment"
              type="filled"
              icon="expand_more"
              :color="main_color"
            >Pick a style!</vs-button>
            <vs-dropdown-menu>
              <vs-dropdown-item @click="get_info('Impressionism')">
                Impressionism
              </vs-dropdown-item>
              <vs-dropdown-item @click="get_info('Expressionism (fine arts)')">
                Expressionism
              </vs-dropdown-item>
              <vs-dropdown-item @click="get_info('Cubism')">
                Cubism
              </vs-dropdown-item>
              <vs-dropdown-item @click="get_info('Surrealism')">
                Surealism
              </vs-dropdown-item>
            </vs-dropdown-menu>
          </vs-dropdown>
        </div>
      </vs-card>
    </vs-row>
  </div>
</template>

<script>
import * as d3 from "d3";
import PieChart from "./PieChart.js";
/*eslint no-unused-vars: 0*/
import zingchart from 'zingchart';
import zingchartVue from 'zingchart-vue';
import TimelinesChart from "../timeline";

export default {
  name: 'Index',
  props: {
    main_color: {
      type: String,
    },
    logo: {
        type: String
    }
  },
  data: () => {
    return {
      artist_options: [],
      genre: 'Hallo',
      selected: 'airstream',
      summary: '',
      related_terms: '',
      fetched: {
        img_generated: false,
        col_generated: false,
        summary: false,
        related_terms: false,
        statistics: false,
        more_statistics: false,
        artist_options: false,
        line_chart: false,
      },
      image: "@/assets/images/big/img1.jpg",
      line_chart_data: {
        type: 'scatter',
        plot: {
          // aspect: "spline",
          tooltip: {
            text: "artist: %t \n year: %kt"
          },
          marker: {
            visible: true,
            style: ["#fff", "#aaa", "#000"],
          },
          animation: {
            effect: 1,
            sequence: 3,
            speed: 10,
          }
        },
        scaleX: {
          label: {
            "text": "Year",
          },
        },
        scaleY: {
          label: {
            "text": "Hue",
          },
        },
        series: [
        ],
        legend: {
          // layout: "1x6", //row x column
          // x: "2%",
          // y: "68%",
        }
      },
      pie_data: {
        hoverBackgroundColor: "blue",
        hoverBorderWidth: 10,
        labels: [ "#e5856d", "#5e2812", "#e56b18", "#f6bab7", "#973f28" ],
        datasets: [
          {
            label: "Data One",
            backgroundColor: [ "#e5856d", "#5e2812", "#e56b18", "#f6bab7", "#973f28" ],
            data: [0.27, 0.14, 0.16, 0.22, 0.21 ]
          }
        ]
      },
      style_hist_data: {
        type: 'area',
        plot: {
          aspect: "spline",
          marker: {
            visible: false,
          },
          animation: {
            effect: 4,
            sequence: 1,
            speed: 10,
          },
        },
        scaleX: {
          label: {
            "text": "Hue",
          },
        },
        scaleY: {
          label: {
            "text": "Density",
          },
        },
        series: [
          {values: [1, 2, 3, 4, 3, 4, 3, 2, 1]},
          {values: [5, 4, 3, 2, 1, 2, 3, 4, 5]},
          {values: [2, 3, 4, 3, 2, 3, 4, 2, 1]},
        ],
        legend: {},
      },
      chart_key: 0,
      pie_key: 0,
      hist_key: 0,
      timeline: TimelinesChart()
    }
  },
  components: {
    PieChart,
    zingchart: zingchartVue
  },
  methods: {
    handleNodeHighlight(e) {
      this.lastVisited = `Node: ${e.nodeindex} Value: ${e.value}`;
    },

    async get_line_graph() {
      var artist = this.selected;
      this.$parent.socket.emit("collect_line_chart", {
        'artist': artist,
      });
    },

    async get_info(genre) {
      // this.$vs.loading();
      this.genre = genre
      this.$parent.socket.emit("collect_info", {
        'genre': genre,
        'year': 1993,
      });

      /*
      fetch("http://localhost:5000/info/" + genre + "/1993")
        .then(response => response.json())
        .then(data => {
          this.data = data;
          this.fetched = true;
          this.$vs.loading.close();
          this.$parent.set_main_color(data.dom_color);
          this.image = data.image;
          this.pie_data.labels = data.colors;
          this.pie_data.datasets = [{
            label: "Data One",
            backgroundColor: data.colors,
            data: data.percentages,
          }];
        }
      );
      */
    },
    setZoomToFilter(start=null, end=null) {
      this.timeline.zoomX(start && end ? [start, end] : [null, null]);
    }
  },
  mounted: function() {
    this.$parent.socket.on("set_image", (data) => {
      window.scroll({top: 0, left: 0, behaviour: 'smooth'});
      this.image = data.generated;
      this.fetched.img_generated = true;
    });

    this.$parent.socket.on("set_color_pie", (data) => {
      this.pie_data.labels = data.colors;
      this.pie_data.datasets = [{
        label: "Data One",
        backgroundColor: data.colors,
        data: data.percentages,
      }];
      this.fetched.col_generated = true;
      this.pie_key += 1;
    });

    this.$parent.socket.on("get_style_hists", (data) => {
      this.style_hist_data.series = data.series;
      this.hist_key += 1;
    });

    this.$parent.socket.on("get_summary", (data) => {
      this.summary = data.summary;
      this.fetched.summary = true;
      this.related_terms = data.related_terms;
      this.fetched.related_terms = true;
    });

    this.$parent.socket.on("set_selected_artist", (data) => {
      this.artist_options = data.artist_options;
      this.fetched.artist_options = true;
    });

    this.$parent.socket.on("collect_line_chart", (data) => {
      this.line_chart_data.series = data.series;
      this.line_chart_data.plot.marker = data.plot.marker;
      console.log(this.line_chart_data);
      this.fetched.line_chart = true;
      this.chart_key += 1;
    });

    window.addEventListener("resize", () => {
        this.timeline.width(document.getElementById('timeline').clientWidth);
    })

    window.addEventListener("load", () => {
      let container = document.getElementById('timeline');
      container.innerHTML = "";

      this.$parent.socket.emit('get_timeline_data', (timeline_data) => {
        timeline_data.forEach(
          group => group.data.forEach(
            label => label.data.forEach((painting) => {
              painting.timeRange[0] = new Date(painting.timeRange[0]['year'], painting.timeRange[0]['month'], 1);
              painting.timeRange[1] = new Date(painting.timeRange[1]['year'], painting.timeRange[1]['month'], 1);
            })));

        let filter = null;

        this.timeline
          .data(timeline_data)
          .width(container.offsetWidth)
          .maxHeight(5000)
          .leftMargin(0)
          .rightMargin(0)
          .zQualitative(true)
          .timeFormat('%Y')
          .showGroupTooltip(false)
          .showLineTooltip(false)
          .onZoom((a, b) => console.log(a, b))
          .onLegendClick((s) => {
            this.setZoomToFilter();
            window.setTimeout(() => {
                if (filter === s.innerHTML) {
                  // Deselect all filters
                  filter = null;
                  d3.selectAll('.series-segment')
                    .attr('class', (d) => { return `series-segment ${d.val}`})
                    .style('fill-opacity', .8);

                  d3.selectAll('.color-slot')
                    .style('fill-opacity', 1);

                  this.setZoomToFilter();
                }
                else {
                  filter = s.innerHTML;
                  let zoomStart = null,
                      zoomEnd = null;

                  // Select specific filter
                  d3.selectAll(`.series-segment.${s.innerHTML}`)
                    .attr('class', (d) => { return `series-segment ${d.val}`})
                    .style('fill-opacity', .8)
                    .each((d, i) => {
                      if (i === 0) zoomStart = d.timeRange[0]
                      if (!zoomEnd || d.timeRange[1] > zoomEnd) zoomEnd = d.timeRange[1]
                    });

                  d3.selectAll(`.color-slot.${s.innerHTML}`)
                    .style('fill-opacity', 1);

                  // Deselect all not selected
                  d3.selectAll(`.series-segment:not(.${s.innerHTML})`)
                    .attr('class', (d) => { return `series-segment ${d.val} disabled`})
                    .style('fill-opacity', .1);

                  d3.selectAll(`.color-slot:not(.${s.innerHTML})`)
                    .style('fill-opacity', .2);

                  this.setZoomToFilter(zoomStart, zoomEnd);
                }
            }, 1000);  // Hackerman to the rescue
          })
          .onSegmentClick((s) => {
            console.log(s);
          })(container);
      });
    });
  },
}
</script>
