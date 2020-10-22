<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24" :lg="6" style="margin-bottom: 16px;">
        <record-card :items="items" :selectedItem="selectedItem" @updateItems="updateItems" @selectItem="selectItem" />
      </a-col>
      <a-col :span="24" :lg="18" style="margin-bottom: 16px;">
        <detail-card :selectedItem="selectedItem" />
      </a-col>
    </a-row>
  </div>
</template>

<script>
  export default {
    name: 'SalesOrder',
    components: {
      RecordCard: () => import('./RecordCard.vue'),
      DetailCard: () => import('./DetailCard.vue'),
    },
    data() {
      return {
        items: [],
        selectedItem: {},
      };
    },
    methods: {
      updateItems(items) {
        this.items = items;
      },
      selectItem(item) {
        this.selectItem = item;
      },
    },
  }
</script>

<style scoped>
</style>