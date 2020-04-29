<template>
  <div>
    <div
      class="alert alert-info"
      :class="{ flashing: animated }"
      @animationend="animated = false"
      v-html="currentKey"
    ></div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from "uuid";
export default {
  created() {
    window.addEventListener("keypress", this.hitButton);
  },
  destroyed() {
    window.removeEventListener("keypress", this.hitButton);
  },
  data() {
    return {
      currentKey: "&nbsp;",
      show: true,
      errors: [],

      animated: false,

      allowedKeys: ["a", "s"],
      maxToasts: 3,
    };
  },
  watch: {
    errors: function(newValue) {
      console.debug(JSON.stringify(newValue));
    },
  },
  methods: {
    toastHidden(e) {
      console.debug("hellow", e);
    },
    hitButton(e) {
      this.currentKey = String.fromCharCode(e.keyCode).toLowerCase();
      this.animated = true;
      if (!this.allowedKeys.includes(this.currentKey))
        this.makeToast(this.currentKey);
    },
    makeToast() {
      const newError = {
        letter: this.currentKey,
        visible: true,
        id: uuidv4(),
      }
      this.errors.push(newError);
      this.$bvToast.toast("Toast body content", {
        title: `Variant ${newError.letter}`,
        id: newError.id,
        solid: true,
        variant: 'danger'
      });
      if (this.errors.length >3) {
        const remEl = this.errors.shift();
         this.$bvToast.hide(remEl.id);
      }
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
