<template>
  <div class="main-wrapper">
    <!---Navigation-->
    <Navbar
      v-bind:main_color="main_color"
      :logo="require('@/assets/images/logo/logo-palette.png')"
      :title="logotitle"
    />
    <div v-bind:main_color="main_color" class="main-container-fluid">

    <router-view v-bind:main_color="main_color"></router-view>

    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';

import Navbar from '@/layout/full/header/Navbar.vue';

export default {
  name: "MainContainer",
  components: {
    Navbar
  },
  data:() => ({
    // main_color: "#061765",
    main_color: "#31B59E",
    logotitle: "ARTificial Intelligence",
    socket: null,
    timeline_data: null
  }),
  methods: {
    set_main_color(color) {
      // console.log("Change color" + color);
      this.main_color = color;
    }
  },
  created: function() {
    // const socket = io.connect("http://localhost:5000");
    this.socket = io("http://localhost:5000");

    this.socket.on("connect", () => {
    });

    this.socket.on("change_color", (color) => {
      this.set_main_color(color);
    });
  },
}
</script>
