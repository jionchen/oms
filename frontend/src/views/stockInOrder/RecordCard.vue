<template>
  <div>
    <a-card>
      <a-row gutter="12" style="margin-bottom: 12px;">
        <a-col :span="12">
          <warehouse-select v-model="searchForm.warehouse" placeholder="仓库" @change="search" />
        </a-col>
        <a-col :span="12">
          <a-select v-model="searchForm.is_complete" placeholder="状态" allowClear style="width: 100%;" @change="search">
            <a-select-option :value="true">已完成</a-select-option>
            <a-select-option :value="false">未完成</a-select-option>
          </a-select>
        </a-col>
        <a-col :span="24" style="margin-top: 6px;">
          <a-input-search v-model="searchForm.search" placeholder="编号" allowClear @search="search" />
        </a-col>
      </a-row>
      <a-table :columns="recordColumns" :data-source="items" :loading="loading" :pagination="pagination"
        :customRow="customRow" :rowClassName="rowClassName" size="small">
        <div slot="status" slot-scope="value, item">{{item.is_complete ? '已完成' : '未完成'}}</div>
        <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
      </a-table>
    </a-card>
  </div>
</template>

<script>
  import { stockInOrderList } from '@/api/warehouse'
  import { recordColumns } from './columns.js'
  import moment from 'moment'

  export default {
    name: 'RecordCard',
    components: {
      WarehouseSelect: () => import('@/components/WarehouseSelect/WarehouseSelect'),
    },
    props: ['items', 'selectedItem'],
    data() {
      return {
        moment,
        recordColumns,
        loading: false,
        searchForm: { page: 1, search: '', warehouse: undefined, is_complete: undefined },
        pagination: { current: 1, total: 0, pageSize: 15 },
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        stockInOrderList(this.searchForm)
          .then(resp => {
            this.pagination.total = resp.data.count;
            this.$emit('updateItems', resp.data.results);
          })
          .catch(err => {
            this.$message.error(this.errorToString(err));
          })
          .finally(() => {
            this.loading = false;
          });
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
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