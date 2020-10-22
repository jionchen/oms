<template>
  <div>
    <a-card title="销售单">
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
        <a-row>
          <a-col :span="8">
            <a-form-model-item prop="discount" label="整单折扣">
              <a-input-number v-model="form.discount" :precision="0" :min="0" :max="100" :step="5"
                :formatter="value => `${value}%`" :parser="value => value.replace('%', '')" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="date" label="日期">
              <a-date-picker v-model="form.date" :showToday="false" :allowClear="false" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="seller" label="销售员">
              <user-select v-model="form.seller" :userName="form.seller_name" />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="warehouse" label="仓库">
              <warehouse-select v-model="form.warehouse" :defaultItem="form" />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="account" label="结算账户">
              <account-select v-model="form.account" :defaultItem="form" />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="amount" label="实收金额">
              <a-input-number v-model="form.amount" :precision="2" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="client" label="客户">
              <client-select v-model="form.client" :defaultItem="form" />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="remark" label="备注">
              <a-input v-model="form.remark" allowClear />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item style="float: right;">
              <a-button type="primary" icon="plus">添加条目</a-button>
            </a-form-model-item>
          </a-col>
        </a-row>
      </a-form-model>
      <a-table :columns="goodsColumns" :data-source="dataSource" :pagination="false" size="small">
        <div slot="amount" slot-scope="value, item">
          {{NP.round(item.isTotal ? value : NP.times(item.quantity, item.retail_price), 2)}}
        </div>
        <div slot="action" slot-scope="value, item, index">
          <a-button-group v-if="!item.isTotal">
            <a-popover title="修改条目" trigger="click">
              <div slot="content">
                <a-form-model :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
                  <a-form-model-item label="单价">
                    <a-input-number v-model="item.retail_price" :precision="2" style="width: 100%;" />
                  </a-form-model-item>
                  <a-form-model-item label="备注">
                    <a-input v-model="item.remark" allowClear />
                  </a-form-model-item>
                </a-form-model>
              </div>
              <a-button type="primary" size="small">
                <a-icon type="edit" />
              </a-button>
            </a-popover>
            <a-button size="small" @click="item.quantity += 1">
              <a-icon type="plus" />
            </a-button>
            <a-button size="small" @click="item.quantity -= 1">
              <a-icon type="minus" />
            </a-button>
            <a-button type="danger" size="small" @click="form.goods_set.splice(index, 1)">
              <a-icon type="close" />
            </a-button>
          </a-button-group>
        </div>
      </a-table>

      <div style="margin-top: 16px;">
        <a-popconfirm v-if="form.id && !form.is_done" title="确定删除吗?" @confirm="destroy">
          <a-button type="danger" style="margin-right: 16px;">删除</a-button>
        </a-popconfirm>
        <a-popconfirm v-if="!form.id" title="确定结算吗?" @confirm="create">
          <a-button type="primary" :loading="buttonLoading">结算</a-button>
        </a-popconfirm>
        <a-button v-else @click="printInvoice">生成打印单据</a-button>
        <a-button style="float: right;" @click="resetForm">清空表单</a-button>
      </div>
    </a-card>
  </div>
</template>

<script>
  import {  } from '@/api/sales'
  import { goodsColumns } from './columns.js'
  import NP from 'number-precision'
  import rules from './rules.js'
  import moment from 'moment'

  export default {
    name: 'DetailCard',
    components: {
      UserSelect: () => import('@/components/UserSelect/UserSelect'),
      WarehouseSelect: () => import('@/components/WarehouseSelect/WarehouseSelect'),
      AccountSelect: () => import('@/components/AccountSelect/AccountSelect'),
      ClientSelect: () => import('@/components/ClientSelect/ClientSelect'),
    },
    props: ['selectedItem'],
    data() {
      return {
        NP,
        rules,
        moment,
        goodsColumns,
        loading: false,
        form: {},
      };
    },
    computed: {
      dataSource() {
        let totalQuantity = 0, totalAmount = 0;
        if (this.form.goods_set) {
          for (let item of this.form.goods_set) {
            totalQuantity += item.quantity;
            totalAmount = NP.times(item.quantity, item.retail_price);
          }
        }

        let totalItem = {
          name: '合计:',
          quantity: totalQuantity,
          amount: NP.times(totalAmount, this.form.discount ? this.form.discount : 100, 0.01),
          isTotal: true,
        };

        return this.form.goods_set ? [...this.form.goods_set, totalItem] : [totalItem];
      }
    },
    methods: {
      initialize() {
        this.resetForm();
      },
      printInvoice() {
        window.open(`/invoice/purchase?id=${this.purchaseForm.id}`);
      },
      resetForm() {
        this.form = {
          date: moment().startOf('day').format(),
          warehouse: null,
          account: null,
          seller: null,
          amount: 0.0,
          client: '',
          remark: '',
          discount: 100,
          goods_set: [],
        };
      },
    },
    watch: {
      selectedItem() {
        this.retrieve();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>