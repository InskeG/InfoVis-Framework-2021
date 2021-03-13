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

        <vs-card class="cardx" v-if="fetched.histograms">
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
        <div class="col-8">
          <v-container>
                <v-row>
                    <v-combobox class="col-5" v-model="pending_add_artists" :items="all_artists" label="Select artist(s)"
                                hide-selected small-chips multiple>
                        <template v-slot:prepend-inner>
                            <v-progress-circular id="add-spinner" :size="20" :width="3"
                                                 style="display: none;" indeterminate color="primary">
                            </v-progress-circular>
                        </template>
                        <template v-slot:append>
                            <v-btn height="auto" @click="addArtists" text>Add</v-btn>
                        </template>
                    </v-combobox>
                    <v-combobox class="col-5 ml-4" v-model="pending_remove_artists" :items="artists_on_timeline"
                                label="Remove artist(s) from timeline" hide-selected small-chips multiple>
                        <template v-slot:prepend-inner>
                            <v-progress-circular id="remove-spinner" :size="20" :width="3"
                                                 style="display: none;" indeterminate color="primary">
                            </v-progress-circular>
                        </template>
                        <template v-slot:append>
                            <v-btn height="auto" @click="removeArtists" text>Remove</v-btn>
                        </template>
                    </v-combobox>
                 </v-row>
          </v-container>
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
        histograms: false,
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
        labels: [
          {
            // text: "Test",
            x: "0%",
            width: "100%",
            gradientColors: `
              #FF0000 #FF8000 #FFFF00 #80FF00
              #00FF00 #00FF80 #00FFFF #007FFF
              #0000FF #7F00FF #FF00FF #FF0080
              #FF0000
            `,
            gradientStops: ".001 .083 .167 .25 .333 .417 .5 .583 .667 .75 .833 .917 1",
            fillAngle: 0,
          }
        ],
      },
      chart_key: 0,
      pie_key: 0,
      hist_key: 0,
      all_artists: [],
      pending_add_artists: [],
      timeline: TimelinesChart(),
      artists_on_timeline: [],
      pending_remove_artists: [],
      artPeriods: [
          {"name": "Medieval", "timeRange": [new Date(500, 1, 1), new Date(1400, 1, 1)]},
          {"name": "Renaissance", "timeRange": [new Date(1400, 1, 1), new Date(1600, 1, 1)]},
          {"name": "Mannerism", "timeRange": [new Date(1527, 1, 1), new Date(1580, 1, 1)]},
          {"name": "Baroque", "timeRange": [new Date(1600, 1, 1), new Date(1750, 1, 1)]},
          {"name": "Rococo", "timeRange": [new Date(1699, 1, 1), new Date(1780, 1, 1)]},
          {"name": "Neoclassicism", "timeRange": [new Date(1750, 1, 1), new Date(1850, 1, 1)]},
          {"name": "Romanticism", "timeRange": [new Date(1780, 1, 1), new Date(1850, 1, 1)]},
          {"name": "Realism", "timeRange": [new Date(1848, 1, 1), new Date(1900, 1, 1)]},
          {"name": "Art Nouveau", "timeRange": [new Date(1890, 1, 1), new Date(1910, 1, 1)]},
          {"name": "Impressionism", "timeRange": [new Date(1865, 1, 1), new Date(1885, 1, 1)]},
          {"name": "Post-impressionism", "timeRange": [new Date(1885, 1, 1), new Date(1910, 1, 1)]},
          {"name": "Fauvism", "timeRange": [new Date(1900, 1, 1), new Date(1935, 1, 1)]},
          {"name": "Expressionism", "timeRange": [new Date(1905, 1, 1), new Date(1920, 1, 1)]},
          {"name": "Cubism", "timeRange": [new Date(1907, 1, 1), new Date(1914, 1, 1)]},
          {"name": "Surrealism", "timeRange": [new Date(1917, 1, 1), new Date(1950, 1, 1)]},
          {"name": "Modern", "timeRange": [new Date(1950, 1, 1), new Date(2022, 1, 1)]},
      ]
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
    },
    renderTimeline(data) {
      let container = document.getElementById('timeline');
      container.innerHTML = "";
      let filter = null;

      this.timeline
        .data(this.parseTimeLineData(data))
        .width(container.offsetWidth)
        .maxHeight(5000)
        .leftMargin(0)
        .rightMargin(0)
        .zQualitative(true)
        .timeFormat('%Y')
        .artPeriods(this.artPeriods)
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
                .attr('class', (d) => {
                  return `series-segment ${d.val}`
                }).style('fill-opacity', .8);

              d3.selectAll('.color-slot').style('fill-opacity', 1);

              this.setZoomToFilter();
            } else {
              filter = s.innerHTML;
              this.$parent.socket.emit("get_artist_histograms", {artists: [filter]});

              this.$parent.socket.emit("generate_images", {
                type: "artists",
                amount: 1,
                class_idx: filter,
              });

              let zoomStart = null, zoomEnd = null;

              // Select specific filter
              d3.selectAll(`.series-segment.${s.innerHTML}`)
                .attr('class', (d) => {
                  return `series-segment ${d.val}`
                }).style('fill-opacity', .8)
                .each((d, i) => {
                  if (i === 0) zoomStart = d.timeRange[0]
                  if (!zoomEnd || d.timeRange[1] > zoomEnd) zoomEnd = d.timeRange[1]
                });
              d3.selectAll(`.color-slot.${s.innerHTML}`)
                .style('fill-opacity', 1);
              // Deselect all not selected
              d3.selectAll(`.series-segment:not(.${s.innerHTML})`)
                .attr('class', (d) => {
                  return `series-segment ${d.val} disabled`
                }).style('fill-opacity', .1);
              d3.selectAll(`.color-slot:not(.${s.innerHTML})`)
                .style('fill-opacity', .2);
              this.setZoomToFilter(zoomStart, zoomEnd);
            }
          }, 1000);  // Hackerman to the rescue
        })
        .onArtPeriodTickClick((period) => {
          console.log("Period selected", period);
          this.setZoomToFilter(period.timeRange[0], period.timeRange[1]);
          // this.get_info(period.text);
          // TODO: Generate GAN based on selected art period

          var start_year = period.timeRange[0].getFullYear();
          var end_year = period.timeRange[1].getFullYear();
          var avg_year = 0.5 * (start_year + end_year);
          var century = Math.round(avg_year / 100);

          this.$parent.socket.emit("generate_images", {
            type: "centuries",
            amount: 1,
            class_idx: century,
          });
        })
        .onSegmentClick((s) => {
          console.log("Painting selected", s);
          // TODO: Generate GAN based on selected art piece
          this.$parent.socket.emit("generate_images", {
            type: "artists",
            amount: 1,
            class_idx: s.val,
          });
        })(container);
    },
    setZoomToFilter(start = null, end = null) {
      this.timeline.zoomX(start && end ? [start, end] : [null, null]);
    },
    addArtists() {
      if (this.pending_add_artists.length > 0) {
        this.artists_on_timeline = this.artists_on_timeline.concat(this.pending_add_artists);
        console.log(this.artists_on_timeline);
        this.pending_add_artists = [];

        document.getElementById('add-spinner').style.display = "block";

        this.$parent.socket.emit('get_timeline_data', this.artists_on_timeline, true, (data) => {
          document.getElementById('add-spinner').style.display = "none";
          this.artists_on_timeline = data['artists'];
          this.renderTimeline(data['timelineData']);
        });
      }
    },
    removeArtists() {
      if (this.pending_remove_artists.some(e => this.artists_on_timeline.includes(e))) {
        this.artists_on_timeline = this.artists_on_timeline.filter(
          e => !this.pending_remove_artists.includes(e)
        );
        this.pending_remove_artists = [];

        document.getElementById('remove-spinner').style.display = "block";

        this.$parent.socket.emit('get_timeline_data', this.artists_on_timeline, (data) => {
          document.getElementById('remove-spinner').style.display = "none";
          this.renderTimeline(data['timelineData']);
        });
      }
    },
    parseTimeLineData(data) {
      data.forEach(
        group => group.data.forEach(
          label => label.data.forEach((painting) => {
            painting.timeRange[0] = new Date(
              painting.timeRange[0]['year'],
              painting.timeRange[0]['month'],
              1
            );
            painting.timeRange[1] = new Date(
              painting.timeRange[1]['year'],
              painting.timeRange[1]['month'],
              1
            );
          })
        )
      );
      return data;
    },
  },
  async created() {
    this.$parent.socket.emit("get_all_artists", (all_artists) => this.all_artists = all_artists);
  },
  mounted: function () {
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
      this.fetched.histograms = true;
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

    this.$parent.socket.on("images_generated", (data) => {
      console.log("Received generated image", data);
      this.image = data.images[0].image;
      this.fetched.img_generated = true;
    });

    window.addEventListener("resize", () => {
        this.timeline.width(document.getElementById('timeline').clientWidth);
    })

    window.addEventListener("load", () => {
        this.$parent.socket.emit('get_timeline_data', (data) => {
            this.artists_on_timeline = data['artists'];
            this.renderTimeline(data['timelineData']);
        });
    });
  }
}
</script>
