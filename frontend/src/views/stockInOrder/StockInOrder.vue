<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24" :lg="8" style="margin-bottom: 16px;">
        <record-card :items="items" :selectedItem="selectedItem" @updateItems="updateItems" @selectItem="selectItem" />
      </a-col>
      <a-col :span="24" :lg="16" style="margin-bottom: 16px;">
        <detail-card :selectedItem="selectedItem" @updateStockInGoods="updateStockInGoods" />
      </a-col>
    </a-row>
  </div>
</template>

<script>
  export default {
    name: 'StockInOrder',
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
        if (this.items.length > 0) {
          this.selectItem(this.items[0]);
        }
      },
      selectItem(item) {
        this.selectedItem = { ...item };
      },
      updateStockInGoods(stockInGoods) {
        for (let item of this.items) {
          if (item.id == stockInGoods.stock_in_order) {
            let isComplete = true;
            for (let index in item.goods_set) {
              if (item.goods_set[index].id == stockInGoods.id) {
                item.goods_set.splice(index, 1, stockInGoods);
              }

              if (item.goods_set[index].quantity_completed < item.goods_set[index].quantity) {
                isComplete = false;
              }
            }
            item.isComplete = isComplete;
            this.items = [...this.items];
            this.selectItem(item);
            break
          }
        }
      },
    },
  }
</script>

<style scoped>
</style>