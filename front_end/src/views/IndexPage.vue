

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

        <vs-card class="cardx" v-if="fetched">
          <div slot="header"><h3>Dominant colors artists use in art pieces over the years</h3></div>

            <zingchart ref="myChart" :data="line_chart_data" @node_mouseover="handleNodeHighlight"></zingchart>
            Last visted: {{lastVisited}}
        </vs-card>

        <vs-card class="cardx">
          <zingchart ref="style_hist" :data="style_hist_data"/>
        </vs-card>
      </vs-col>


    </vs-row>

    <vs-row type="flex" vs-justify="center" vs-align="center" vs-w="12">
      <vs-card class="cardx">
        <div slot="header"><h3>
          Pick a <span v-if="fetched">new</span> style!
        </h3></div>
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
import PieChart from "./PieChart.js";
/*eslint no-unused-vars: 0*/
import zingchart from 'zingchart';
import zingchartVue from 'zingchart-vue';


export default {
  name: 'Index',
  props: {
    main_color: {
      type: String,
    },
    logo: {
        type: String
    },
  },
  computed: {
    style_hist_data() {
      return {
        type: 'area',
        plot: {
          aspect: "spline",
          marker: {
            'visible': false,
          },
        },
        series: this.style_hist_values,
      };
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
      line_chart_data: {
        type: 'line',
        series: [
          {
            values: [2,4,5,7,4,3,6,5]
          }
        ]

      },
      lastVisited: '',
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
      style_hist_values: [
        {values: [1, 2, 3, 4, 3, 4, 3, 2, 1]},
        {values: [5, 4, 3, 2, 1, 2, 3, 4, 5]},
        {values: [2, 3, 4, 3, 2, 3, 4, 2, 1]},
      ],
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
      console.log(data);
      this.fetched.col_generated = true;
    });

    zingchart.bind("style_hist", "setseriesdata", (data) => {
      console.log("Updating data");
    });

    this.$parent.socket.on("get_style_hists", (data) => {
      console.log("Updating style hists");

      var series_data = {
        type: "area",
        plot: {
          aspect: "spline",
          marker: {
            'visible': false,
          },
        },
        series: []
      };

      for (var art_type in data) {
        // series_data['series'].push({values: data[art_type]});
        console.log(data[art_type]);
        // zingchart.exec("style_hist", "setseriesvalues", {
        this.style_hist_values[0].values = data[art_type];

        break;
      }

      // console.log(series_data);
      // this.$refs.style_hist.setseriesdata(series_data);
      // this.$refs.style_hist.update();

      console.log(this.$refs.style_hist);
      this.$refs.style_hist.update();
    });

  },
}
</script>
