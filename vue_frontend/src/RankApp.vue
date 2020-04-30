<template>
  <div class="row d-flex">
    <div class="col-6 d-flex flex-column citylist-container">
      <draggable
        class="list-group source citylist"
        :list="list1"
        v-bind="options"
        @change="listchanged"
      >
        <div
          class="list-group-item draggable-item d-flex"
          v-for="(element) in list1"
          :key="element.name"
        >
          <div class="item-wrapper d-flex">
            <div class="city-label">{{ element.label }}</div>
          </div>
          <div class="drag-handler">
            <ion-icon name="move-outline"></ion-icon>
          </div>
        </div>
      </draggable>
    </div>

    <div class="col-6 d-flex flex-column citylist-container">
      <draggable
        class="list-group destination citylist "
        :list="list2"
        @change="listchanged"
        v-bind="options"
      >
        <div
          class="list-group-item draggable-item d-flex"
          v-for="(element, index) in list2"
          :key="element.name"
        >
          <div class="item-wrapper d-flex">
            <div
              class="badge badge-secondary d-flex flex-column m-0 p-0 badger"
            >
              <div>{{ index +1 }}</div>
            </div>

            <div class="city-label"> {{ element.label }}</div>
          </div>
          <div class="drag-handler">
            <ion-icon name="move-outline"></ion-icon>
          </div>
        </div>
      </draggable>
    </div>
    <div v-for="(input, index) in list2" :key="index">
      <input :value="index" :name="input.name" type="hidden" />
    </div>
  </div> 
</template>

<script>
import draggable from "vuedraggable";
import ionIcon from 'ionicons'
import _ from "lodash";
export default {
  components: { draggable, ionIcon },
  name: "Rank",
  data() {
    return {
      error: false,
      list1: _.clone(this.originalList),
      list2: [],
      options: {
        group: "people",
        ghostClass: "ghost",
      },
    };
  },
  methods: {
    listchanged() {
      this.error = false;
      window.listFilled = this.list2.length === this. originalList.length;
    },
  },
};
</script>
