<template>
  <div>
    <a-card>
      <a-table :columns="recordColumns" :data-source="items" :loading="loading" :pagination="pagination"
        :customRow="customRow" :rowClassName="rowClassName" size="small">
        <div slot="status" slot-scope="value, item">{{statusToString(item)}}</div>
        <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
      </a-table>
    </a-card>
  </div>
</template>

<script>
  import { salesOrderList } from '@/api/sales'
  import { recordColumns } from './columns.js'
  import moment from 'moment'

  export default {
    name: 'RecordCard',
    props: ['items', 'selectedItem'],
    data() {
      return {
        moment,
        recordColumns,
        loading: false,
        searchForm: { page: 1, is_return: true },
        pagination: { current: 1, total: 0, pageSize: 15 },
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        salesOrderList(this.searchForm)
          .then(resp => {
            this.pagination.total = resp.data.count;
            this.$emit('updateItems', resp.data.results);
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      statusToString(item) {
        let orderType = item.is_return ? '退货单' : '销售单';
        let orderStatus = item.is_done ? '已完成' : item.is_return ? '等待入库' : '等待出库';
        return `${orderType} - ${orderStatus}`
      },
      customRow(item) {
        return {
          on: {
            click: () => this.$emit('selectItem', item),
          },
        }
      },
      rowClassName(item) {
        if (item.id == this.selectedItem.id) {
          return 'table-selected'
        }
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
  .table-selected {
    background: #e6f7ff;
  }
</style>