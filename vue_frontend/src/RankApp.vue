<template>
  <div>
     <div class='alert alert-danger' v-if='error'>Перенесите все города в один из двух списков</div>
    <div class="row d-flex align-items-end ">
      <div class="col-4 ">{{originalListTitle}}</div>
      <div class="col-4">{{rankedListTitle}}</div>
      <div class="col-4">{{DNKListTitle}}</div>
    </div>
    <div class="row d-flex ">
      <RankList :itemslist="list1" @childlistchanged="listchanged"></RankList>

      <RankList
        :itemslist="list2"
        :showRank="true"
        @childlistchanged="listchanged"
      ></RankList>
      <RankList :itemslist="list3" @childlistchanged="listchanged"></RankList>
      <div v-for="(input, index) in list2" :key="index">
        <input :value="index" :name="input.name" type="hidden" />
      </div>
      <div v-for="(input, index) in list3" :key="index + 1000">
        <input :value="999" :name="input.name" type="hidden" />
      </div>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import RankList from "./RankList";
export default {
  components: { RankList },
  name: "Rank",
  data() {
    return {
      error:false,
      list1: _.clone(this.originalList),
      list2: [],
      list3: [],
      originalListTitle: window.originalListTitle,
      rankedListTitle: window.rankedListTitle,
      DNKListTitle: window.DNKListTitle,
      options: {
        group: "people",
        ghostClass: "ghost",
      },
    };
  },
  
  methods: {
  
    listchanged() {
      this.error = false;
      window.listFilled = this.list1.length === 0;
    },
  },
};
</script>
