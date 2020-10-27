<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24" :lg="6" style="margin-bottom: 16px;">
        <record-card :items="items" :selectedItem="selectedItem" @updateItems="updateItems" @selectItem="selectItem" />
      </a-col>
      <a-col :span="24" :lg="18" style="margin-bottom: 16px;">
        <detail-card :selectedItem="selectedItem" @createItem="createItem" @destroyItem="destroyItem"
          @committedItem="committedItem" />
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
      createItem(item) {
        this.items.splice(0, 0, item);
      },
      updateItems(items) {
        this.items = items;
      },
      destroyItem(id) {
        this.items.splice(this.items.findIndex(item => item.id == id), 1);
      },
      selectItem(item) {
        this.selectedItem = { ...item };
      },
      committedItem(item) {
        this.items.splice(this.items.findIndex(order => order.id === item.id), 1, item);
        if (this.selectedItem.id == item.id) {
          this.selectedItem = { ...item };
        }
      },
    },
  }
</script>

<style scoped>
</style>