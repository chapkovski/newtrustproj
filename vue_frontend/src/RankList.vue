<template>
 
    <div class="col-6 d-flex flex-column citylist-container">
      <draggable
        class="list-group source citylist"
        :list="itemslist"
        v-bind="options"
        @change="$emit('childlistchanged')">"
      >
        <div
          class="list-group-item draggable-item d-flex"
          v-for="(element) in itemslist"
          :key="element.name"
        > 
          <div class="item-wrapper d-flex" v-if='showRank'>
            <div class="city-label">{{ element.label }}</div>
          </div>
          <div class="drag-handler">
            <ion-icon name="move-outline"></ion-icon>
          </div>
        </div>
      </draggable>
    </div>

    
</template>

<script>
import draggable from "vuedraggable";
import ionIcon from 'ionicons'
import _ from "lodash";
export default {
  components: { draggable, ionIcon },
  name: "Rank",
  props: {
    itemslist: Array,
    showRank: Boolean,
  },
  data() {
    return {
      error: false,
      options: {
        group: "people",
        ghostClass: "ghost",
      },
    };
  }
};
</script>
