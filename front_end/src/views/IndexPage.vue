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
        <vs-card class="cardx" v-if="fetched.statistics">
          <div slot="header"><h3>Interessante data</h3></div>
          <div>
            alskjhd lksjh sfajkh asjfh lkasfh
            alskjhd lksjh sfajkh asjfh lkasfh
            alskjhd lksjh sfajkh asjfh lkasfh
            alskjhd lksjh sfajkh asjfh lkasfh
            alskjhd lksjh sfajkh asjfh lkasfh
          </div>
        </vs-card>
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
            <pie-chart :data="chartData" :options="chartOptions"></pie-chart>
          </div>
            <div id="my_dataviz"></div>
          </div>
        </vs-card>
      </vs-col>

      <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
        <vs-card class="cardx" v-if="fetched.summary">
          <div slot="header"><h3>{{ data.genre }} on Wikipedia</h3></div>
          <div>
            {{ data.summary }}
          </div>
        </vs-card>
      </vs-col>
    </vs-row>

    <vs-row type="flex" vs-justify="center" vs-align="center" vs-w="12">
      <vs-card class="cardx">
        <div slot="header">
            <h3>Pick a <span v-if="fetched">new</span> style!</h3>
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
      fetched: {
        img_generated: false,
        col_generated: false,
        summary: false,
        statistics: false,
        more_statistics: false,
      },
      image: "@/assets/images/big/img2.jpg",
      chartOptions: {
        hoverBorderWidth: 20
      },
      chartData: {
        hoverBackgroundColor: "blue",
        hoverBorderWidth: 10,
        labels: [ "#e5856d", "#5e2812", "#e56b18", "#f6bab7", "#973f28" ],
        datasets: [
          {
            label: "Data One",
            backgroundColor: [ "#e5856d", "#5e2812", "#e56b18", "#f6bab7", "#973f28" ],
            data: [ 0.27, 0.13764444444444446, 0.15853333333333333, 0.2235111111111111, 0.21031111111111112 ]
          }
        ]
      },
      timeline: TimelinesChart()
    }
  },
  components: {
    PieChart
  },
  methods: {
    async get_info(genre) {
      // this.$vs.loading();

      this.$parent.socket.emit("collect_info", {
        genre: genre,
        year: 1993,
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
          this.chartData.labels = data.colors;
          this.chartData.datasets = [{
            label: "Data One",
            backgroundColor: data.colors,
            data: data.percentages,
          }];
        }
      );
      */
    }
  },
  mounted: function() {
    this.$parent.socket.on("set_image", (data) => {
      this.image = data.generated;
      this.fetched.img_generated = true;
    });

    this.$parent.socket.on("set_color_pie", (data) => {
      window.console.log(data);
      this.fetched.col_generated = true;
    });

    window.addEventListener("resize", () => {
        this.timeline.width(document.getElementById('timeline').clientWidth + 60);
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
          .width(timeline_data.clientWidth)
          .maxHeight(5000)
          .leftMargin(0)
          .rightMargin(60)
          .zQualitative(true)
          .timeFormat('%Y')
          .showGroupTooltip(false)
          .showLineTooltip(false)
          .onZoom((a, b) => console.log(a, b))
          .onLegendClick((s) => {
            if (filter === s.innerHTML) {
              // Deselect all filters
              filter = null;
              d3.selectAll('.series-segment')
                .attr('class', (d) => { return `series-segment ${d.val}`})
                .style('fill-opacity', .8);

              d3.selectAll('.color-slot')
                .style('fill-opacity', 1);

              setZoomToFilter();
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

              setZoomToFilter(zoomStart, zoomEnd);
            }
          })
          .onSegmentClick((s) => {
            console.log(s);
          })(container);

        function setZoomToFilter(start=null, end=null) {
          this.timeline.zoomX(start && end ? [start, end] : [null, null]);
        }
      });
    });
  },
}
</script>
