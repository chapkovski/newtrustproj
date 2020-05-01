<template>
  <div class="col-4 d-flex flex-column citylist-container">
    
    <draggable
      class="list-group source citylist"
      :list="itemslist"
      v-bind="options"
      @change="$emit('childlistchanged')"
    >
      <div
        class="list-group-item draggable-item d-flex"
        v-for="(element, index) in itemslist"
        :key="index"
      >
        <div
          class="badge badge-secondary d-flex flex-column m-0 p-0 badger"
          v-if="showRank"
        >
          <div>{{ index + 1 }}</div>
        </div>
        <div class="item-wrapper d-flex">
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
import ionIcon from "ionicons";
import _ from "lodash";
export default {
  components: { draggable, ionIcon },
  name: "RankList",
  props: {
    itemslist: Array,
    showRank: { type: Boolean, default: false },
    title: String,
  },
  data() {
    return {
      error: false,
      options: {
        group: "people",
        ghostClass: "ghost",
      },
    };
  },
};
</script>
<style>
[v-cloak] {
  display: none;
}

.item-wrapper {
  margin: -2px !important;
  padding: 2px;
  flex-grow: 1;
  border: 0.5px solid lightgray;
  -webkit-box-shadow: 1px 1px 2px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 1px 1px 2px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 1px 1px 2px 0px rgba(0, 0, 0, 0.75);
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 0.25rem;
}

.ghost {
  opacity: 0.5;
  background: blue;
  color: white;
}

.citylist {
  display: flex;
  flex-direction: column;
  border: 0.05rem solid lightgrey;
  border-radius: 0.25rem;
  min-height: 589px;
  flex-grow: 1;
}

.sortable-drag {
  cursor: move;
}

.city-label {
  flex-grow: 1;
  margin-left: 5px;
}

.draggable-item {
  cursor: pointer;
}

.draggable-item .drag-handler {
  cursor: move;
  display: flex;
  justify-content: center;
  align-items: center;
  align-content: center;
  margin-left: 10px;
  margin-right: -10px;
}

.drag-handler * {
  margin: 0px !important;
  padding: 0px !important;
}

.badger {
  padding: 0px;

  justify-content: center;
  align-content: center;
  min-width: 25px;
}

.citylist-container {
  flex-grow: 1;
}
</style>
