<template>
  <div>
    <div
      class="alert alert-info"
      :class="{ flashing: animated }"
      @animationend="animated = false"
      v-html='currentKey'
    >
      
    </div>
  </div>
</template>

<script>
export default {
  created() {
    window.addEventListener("keypress", this.doCommand);
  },
  destroyed() {
    window.removeEventListener("keypress", this.doCommand);
  },
  data() {
    return {
      currentKey: "&nbsp;",
      show: true,
      animated: false,
    };
  },

  methods: {
    doCommand(e) {
      this.currentKey = String.fromCharCode(e.keyCode).toLowerCase();
      this.animated = true;
    },
  },
};
</script>

<style lang="scss">
.flashing {
  animation: flash 0.05s;
}

@keyframes flash {
  0% {
    background-color: none;
  }
  50% {
    background-color: green;
  }
  100% {
    background-color: none;
  }
}
</style>
