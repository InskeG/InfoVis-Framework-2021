<template>
  <div class="main-wrapper">
    <!---Navigation-->
    <Navbar
      v-bind:main_color="main_color"
      :logo="require('@/assets/images/logo/logo-palette.png')"
      :title="logotitle"
    />
    <!---Sidebar-->
    <SideBar parent=".main-wrapper" :sidebarLinks="sidebarLinks"/>
    <!---Page Container-->
    <div class="main-container-fluid">

    <router-view v-bind:main_color="main_color"></router-view>

    </div>
  </div>
</template>

<script>
import Navbar from '@/layout/full/header/Navbar.vue';
import SideBar from '@/layout/full/sidebar/SideBar.vue';
import sidebarLinks from '@/layout/full/sidebar/sidebarlinks.js';

export default {
  name: "MainContainer",
  components: {
    Navbar,
    SideBar
  },
  data:() => ({
    main_color: "#2962ff",
    logotitle: "ARTificial Intelligence",
    sidebarLinks: sidebarLinks,
  }),
  methods: {
    set_main_color(color) {
      console.log("Change color" + color);
      this.main_color = color;
    }
  },
}
</script>
