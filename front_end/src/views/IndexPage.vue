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
                more_statistics: false
            },
            image: "@/assets/images/big/img2.jpg",
            chartOptions: {
                hoverBorderWidth: 20
            },
            chartData: {
                hoverBackgroundColor: "blue",
                hoverBorderWidth: 10,
                labels: ["#e5856d", "#5e2812", "#e56b18", "#f6bab7", "#973f28"],
                datasets: [
                    {
                        label: "Data One",
                        backgroundColor: ["#e5856d", "#5e2812", "#e56b18", "#f6bab7", "#973f28"],
                        data: [0.27, 0.13764444444444446, 0.15853333333333333, 0.2235111111111111, 0.21031111111111112]
                    }
                ]
            },
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
        },
        parseTimeLineData(data) {
            data.forEach(
                group => group.data.forEach(
                        label => label.data.forEach((painting) => {
                            painting.timeRange[0] = new Date(painting.timeRange[0]['year'], painting.timeRange[0]['month'], 1);
                            painting.timeRange[1] = new Date(painting.timeRange[1]['year'], painting.timeRange[1]['month'], 1);
                        })));
            return data;
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
                                    })
                                    .style('fill-opacity', .8);

                            d3.selectAll('.color-slot')
                                    .style('fill-opacity', 1);

                            this.setZoomToFilter();
                        } else {
                            filter = s.innerHTML;
                            let zoomStart = null,
                                zoomEnd = null;

                            // Select specific filter
                            d3.selectAll(`.series-segment.${s.innerHTML}`)
                                    .attr('class', (d) => {
                                        return `series-segment ${d.val}`
                                    })
                                    .style('fill-opacity', .8)
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
                                    })
                                    .style('fill-opacity', .1);

                            d3.selectAll(`.color-slot:not(.${s.innerHTML})`)
                                    .style('fill-opacity', .2);

                            this.setZoomToFilter(zoomStart, zoomEnd);
                        }
                    }, 1000);  // Hackerman to the rescue
                })
                .onArtPeriodTickClick((period) => {
                    console.log(period);
                    this.setZoomToFilter(period.timeRange[0], period.timeRange[1]);
                    this.get_info(period.text);
                    // TODO: Generate GAN based on selected art period
                })
                .onSegmentClick((s) => {
                    console.log(s);
                    // TODO: Generate GAN based on selected art piece
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
                this.artists_on_timeline = this.artists_on_timeline.filter(e => !this.pending_remove_artists.includes(e))
                this.pending_remove_artists = [];

                document.getElementById('remove-spinner').style.display = "block";

                this.$parent.socket.emit('get_timeline_data', this.artists_on_timeline, (data) => {
                    document.getElementById('remove-spinner').style.display = "none";
                    this.renderTimeline(data['timelineData']);
                });
            }
        }
    },
    async created() {
        this.$parent.socket.emit("get_all_artists", (all_artists) => this.all_artists = all_artists);
    },
    mounted: function () {
        this.$parent.socket.on("set_image", (data) => {
            this.image = data.generated;
            this.fetched.img_generated = true;
        });

        this.$parent.socket.on("set_color_pie", (data) => {
            window.console.log(data);
            this.fetched.col_generated = true;
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
    },
}
</script>
