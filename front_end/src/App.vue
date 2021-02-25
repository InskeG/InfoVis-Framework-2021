<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  name: 'App',
  components: {
  },
  data: () => {
    return {
      socket: null
    }
  },
  methods: {

  },
  created: () => {
    window.console.log("Hallo!");
    // const socket = io.connect("http://localhost:5000");
    const socket = io("http://localhost:5000");

    socket.on("connect", () => {
      window.console.log("Connected!");
    });
  },
}
</script>
