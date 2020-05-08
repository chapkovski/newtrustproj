<template>
  <div>
    Are you currently employed?

No
 
Yes
    <input type="radio" id="one" value="One" v-model="picked" />
    <label for="one">One</label>
    <br />
    <input type="radio" id="two" value="Two" v-model="picked" />
    <label for="two">Two</label>
    <br />
    <span>Picked: {{ picked }}</span>
  </div>
</template>

<script>
export default {
  name: "Occupation",
  
  data() {
    return {
      picked: null,
    };
  },
  methods: {},
};
</script>
