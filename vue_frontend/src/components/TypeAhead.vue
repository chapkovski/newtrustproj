<template>
<div class="form-group required">
   <div class="controls  field-location">

          <vue-google-autocomplete
            id="id_birthplace"
            ref="address"
            classname="form-control"
            placeholder="Введите название"
            @placechanged="getAddressData"
            types="(cities)"
            name='birthplace'
          >
          </vue-google-autocomplete>
    </div>

</div>

</template>

<script>
import VueGoogleAutocomplete from "./VueAutocomplete";
export default {
  name: "HelloWorld",
  components: { VueGoogleAutocomplete },
  data: function() {
    return { address: "" ,
    retrieved_address:""};
  },
  methods: {
    getAddressData: function(addressData, place) {
        console.debug('PLACE', place.formatted_address);
      this.address = addressData;
      if (place && place.formatted_address){
      this.retrieved_address = place.formatted_address}
    },

  },

};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
