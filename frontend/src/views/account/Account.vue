<template>
  <div>
    <a-card title="结算账户">
      <a-row gutter="16">
        <a-col :span="6">
          <a-input-search v-model="searchForm.search" placeholder="编号, 名称, 备注" allowClear @search="search" />
        </a-col>
        <a-col :span="6">
          <a-select v-model="searchForm.is_active" placeholder="状态" style="width: 100%;" allowClear @change="search">
            <a-select-option :value="true">激活</a-select-option>
            <a-select-option :value="false">冻结</a-select-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-space>
            <a-button>导入</a-button>
            <a-button>导出</a-button>
          </a-space>
        </a-col>
        <a-col :span="6">
          <div style="float: right;">
            <a-button type="primary" icon="plus" @click="openFormModal(form)">新增账户</a-button>
          </div>
        </a-col>
      </a-row>

      <div style="margin-top: 16px;">
        <a-table :columns="columns" :data-source="items" size="small" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="type" slot-scope="value">{{type[value]}}</div>
          <div slot="is_active" slot-scope="value">
            <a-tag :color="value ? 'green' : 'red'">{{value ? '激活' : '冻结'}}</a-tag>
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button size="small" @click="openFormModal(item)">
                <a-icon type="edit" />编辑
              </a-button>
              <a-popconfirm title="确定删除吗" @confirm="destroy(item.id)">
                <a-button type="danger" icon="delete" size="small">删除</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </div>
    </a-card>

    <form-modal v-model="visible" :form="targetItem" @create="create" @update="update" />
  </div>
</template>

<script>
  import { accountList, accountDestroy } from '@/api/account'
  import columns from './columns.js'

  export default {
    name: 'Account',
    components: {
      FormModal: () => import('./FormModal.vue')
    },
    data() {
      return {
        columns,
        searchForm: { search: '', page: 1, is_active: undefined, ordering: undefined },
        pagination: { current: 1, total: 0, pageSize: 15 },
        form: { is_active: true },
        items: [],
        loading: false,
        visible: false,
        targetItem: {},
        type: {
          cash: '现金',
          bank_accounts: '银行账户',
          alipay: '支付宝',
          wechat_pay: '微信支付',
          other: '其他',
        },
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        console.log(this.searchForm);
        accountList(this.searchForm)
          .then(resp => {
            this.pagination.total = resp.data.count;
            this.items = resp.data.results;
          })
          .catch(err => {
            this.$message.error(this.errorToString(err));
          })
          .finally(() => {
            this.loading = false;
          });
      },
      create(item) {
        this.items.splice(0, 0, item);
      },
      update(item) {
        this.items.splice(this.items.findIndex(i => i.id == item.id), 1, item);
      },
      destroy(id) {
        accountDestroy(id)
          .then(() => {
            this.items.splice(this.items.findIndex(item => item.id == id), 1);
            this.$message.success('删除成功');
          })
          .catch(err => {
            this.$message.error(this.errorToString(err));
          })
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
      },
      tableChange(pagination, filters, sorter) {
        this.searchForm.page = pagination.current;
        this.pagination.current = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
      openFormModal(item) {
        this.targetItem = { ...item };
        this.visible = true;
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>