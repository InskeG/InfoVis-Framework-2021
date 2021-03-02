
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


      <vs-card class="cardx" v-if="fetched.artist_options">
          <div slot="header"><h3>Dominant colors in art pieces over the years for specific artists</h3></div>


        <form id="line_chart">
            <select v-model="selected">
            <option v-for="option in artist_options" v-bind:key="option"> {{ option }}</option>

            </select>

            </form>
            
            <zingchart ref="myChart" :data="line_chart_data" @node_mouseover="handleNodeHighlight"></zingchart>

        </vs-card>


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
  data: () => {
    return {
      artist_options: [],
      selected: 'airstream',
      fetched: {
        img_generated: false,
        col_generated: false,
        summary: false,
        statistics: false,
        more_statistics: false,
        artist_options: false,
        line_chart: false
      },
      image: "@/assets/images/big/img1.jpg",
      chartOptions: {
        hoverBorderWidth: 20
      },
      line_chart_data: {
        type: 'line',
        plot: {
          tooltip: {
            text: "artist: %t \n year: %kt"
          }

        },
        series: [
        ],

           plotarea: {
          'margin-bottom': "40%",
          'margin-top': "5%"
        },
     
        legend: {
          layout: "1x6", //row x column
          x: "2%",
          y: "68%",

        }

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
      }
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
      this.chartData.labels = data.colors;
      this.chartData.datasets = [{
        label: "Data One",
        backgroundColor: data.colors,
        data: data.percentages,
      }];
      this.fetched.col_generated = true;
    });

    
    this.$parent.socket.on("set_selected_artist", (data) => {
      this.artist_options = data.artist_options;
      this.fetched.artist_options = true;
    });

    this.$parent.socket.on("line_chart", (data) => {
      this.line_chart_data.series = data.series;
      this.fetched.line_chart = true;
    })

    

   


  },
}
</script>
