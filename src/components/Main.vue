<template>
  <b-container class="bv-example-row">
    <b-row>
      <b-col><partial :content="left_content"></partial></b-col>
      <b-col><Q :content="q_content"></Q></b-col>
      <b-col><partial :content="right_content"></partial></b-col>
    </b-row>
    <b-row>
      <b-col>
        <div
          class="alert alert-info"
          :class="{ flashing: animated }"
          @animationend="animated = false"
          v-html="currentKey"
        ></div>
      </b-col>
    </b-row>
    <b-row>
      <b-alert
        v-model="error"
        class="position-fixed fixed-top m-0 rounded-0"
        style="z-index: 2000;"
        variant="danger"
        dismissible
        >Wrong answer!</b-alert
      >
    </b-row>
  </b-container>
</template>

<script>
import { v4 as uuidv4 } from "uuid";
import Q from "./Q.vue";
import partial from "./Partial.vue";
export default {
  components: {
    Q,
    partial,
  },
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
      error: false,
      wrong_key_errors: [],
      animated: false,
      allowedKeys: ["a", "s"],
      maxToasts: 3,
      delay: 1000,
      typeCorrespondance: { a: "left", s: "right" },
      questions: [
        {
          left: "Fat",
          right: "Slim",
          q: "question content",
          correct: "left",
        },
        {
          left: "NEW something here",
          right: "NEW something here on the right",
          q: "NEW question content",
          correct: "right",
        },
      ],
      qpointer: 0,
    };
  },
  computed: {
    left_content() {
      return this.questions[this.qpointer].left;
    },
    right_content() {
      return this.questions[this.qpointer].right;
    },
    q_content() {
      return this.questions[this.qpointer].q;
    },
    right_answer() {
      return this.questions[this.qpointer].correct;
    },
    input_is_correct() {
      return this.right_answer === this.typeCorrespondance[this.currentKey];
    },
  },
  methods: {
    hitButton(e) {
      this.error = false;
      this.currentKey = String.fromCharCode(e.keyCode).toLowerCase();
      this.animated = true;
      if (!this.allowedKeys.includes(this.currentKey)) {
        this.makeWrongLetterToast(this.currentKey);
        return;
      }
      if (this.input_is_correct) {
        this.qpointer = (this.qpointer + 1) % this.questions.length;
      } else {
        this.error = true;
      }
    },

    makeWrongLetterToast() {
      const newError = {
        letter: this.currentKey,
        visible: true,
        id: uuidv4(),
      };
      this.wrong_key_errors.push(newError);
      this.$bvToast.toast("This letter is not allowed", {
        title: `You typed   ${newError.letter}`,
        id: newError.id,
        solid: true,
        variant: "warning",
        autoHideDelay: this.delay,
        toaster: "b-toaster-bottom-left",
      });
      if (this.errors.length > this.maxToasts) {
        const remEl = this.wrong_key_errors.shift();
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
