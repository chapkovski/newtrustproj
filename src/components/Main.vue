<template>
  <div>
    <div
      
      :class="{ flashing: animated }"
      @animationend="disanimate"
      @transitionend="disanimate"
      @click="animate"
    >
      {{currentKey}}
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
      currentKey:'',
      show: true,
      animated: false,
    };
  },

  methods: {
    doCommand(e) {
      this.currentKey = String.fromCharCode(e.keyCode).toLowerCase();
      this.animated = true;
    },
    disanimate() {
      console.debug("animation ends!");
      this.animated = false;
    },
    animate() {
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
