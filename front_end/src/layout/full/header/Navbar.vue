<template>
	<header class="gridx">
		<vs-navbar
      v-model="indexActive"
      :color="topbarColor"
      class="topnavbar" text-color="rgba(255,255,255,0.7)" active-text-color="rgba(255,255,255,1)">
      <!---
      Template logo
      -->
      <div slot="title" class="themelogo">
        <img :src="logo" v-if="logo" alt="Dashboard"/>
        <span class="logo-text" v-if="title">{{ title }}</span>
      </div>
      <!---
      Mobile toggle
      -->
      <div slot="title">
        <div class="hiddenDesktop cursor-pointer" @click.stop="activeSidebar"><vs-icon icon="menu"></vs-icon></div>
      </div>


      <vs-spacer></vs-spacer>

      <!---
      Craete new dd
      -->
      <vs-dropdown  vs-trigger-click left class="cursor-pointer pr-2 pl-2 ml-1 mr-1">
         <a class="text-white-dark" href="#"><vs-icon icon="notifications"></vs-icon></a>
        <vs-dropdown-menu class="topbar-dd">
          <vs-dropdown-item>Action</vs-dropdown-item>
          <vs-dropdown-item>Another Action</vs-dropdown-item>
          <vs-dropdown-item>Something</vs-dropdown-item>
          <vs-dropdown-item>Here</vs-dropdown-item>
        </vs-dropdown-menu>
      </vs-dropdown>
      <vs-dropdown  vs-trigger-click left class="cursor-pointer pr-2 pl-2 ml-1 mr-1">
         <a class="text-white-dark" href="#"><vs-icon icon="mode_comment"></vs-icon></a>
        <vs-dropdown-menu class="topbar-dd">
          <vs-dropdown-item>Action</vs-dropdown-item>
          <vs-dropdown-item>Another Action</vs-dropdown-item>
          <vs-dropdown-item>Something</vs-dropdown-item>
          <vs-dropdown-item>Here</vs-dropdown-item>
        </vs-dropdown-menu>
      </vs-dropdown>
    </vs-navbar>

	</header>

</template>

<script>
export default {
	name : 'Navbar',
  props: {
      topbarColor: {
          type: String,
          default: "#2962ff",
      },
      title: {
            type: String,
      },
      logo: {
          type: String
      },
  },
  data:()=>({
    indexActive: 0,
    showToggle: false

  }),

  methods: {
      //This is for sidebar trigger in mobile
      activeSidebar() {
          this.$store.commit('IS_SIDEBAR_ACTIVE', true);
      }

  }
}
</script>
