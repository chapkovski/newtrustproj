<template>
  <div id="app">
       <TypeAhead :field_id='this.field_id' :field_name='this.field_name'></TypeAhead>
  </div>
</template>

<script>

import TypeAhead from './components/TypeAhead.vue'
export default {
  name: 'App',
  data(){
  return {
  field_id: window.field_id|| 'id_birthplace',
  field_name: window.field_name|| 'birthplace',
  }
  },
  components: {
    TypeAhead
  }
}
</script>


