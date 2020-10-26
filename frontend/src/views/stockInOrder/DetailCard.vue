<template>
  <div>
    <a-card>
      <div slot="title">{{selectedItem.number ? `入库单 - ${selectedItem.number}` : '入库单'}}</div>
      <a-table :columns="goodsColumns" :data-source="selectedItem.goods_set" :pagination="false" size="small">
        <div slot="action" slot-scope="value, item">
          <a-button type="link" size="small" :disabled="item.quantity_completed >= item.quantity"
            @click="stockIn(item)">添加入库</a-button>
        </div>
      </a-table>
      <!-- <a-button style="margin-top: 16px;" @click="printInvoice">生成入库单</a-button> -->
    </a-card>

    <stock-in-modal v-model="visible" :stockInGoods="stockInGoods" @update="update" />
  </div>
</template>

<script>
  import { goodsColumns } from './columns.js'

  export default {
    name: 'DetailCard',
    components: {
      StockInModal: () => import('./StockInModal.vue'),
    },
    props: ['selectedItem'],
    data() {
      return {
        goodsColumns,
        visible: false,
        stockInGoods: {},
      };
    },
    methods: {
      stockIn(item) {
        this.visible = true;
        this.stockInGoods = { ...item };
      },
      update(item) {
        this.$emit('updateStockInGoods', item);
      },
      // printInvoice() {
      //   window.open(`/invoice/stock_in?id=${this.selectedItem.id}`);
      // },
    },
  }
</script>

<style scoped>
</style>