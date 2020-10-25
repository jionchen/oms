<template>
  <div>
    <a-card title="销售单">
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
        <a-row>
          <a-col :span="9">
            <a-form-model-item prop="sales_order" label="关联销售单" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
              <a-button style="width: 100%;" @click="relationModalVisible = true">
                {{form.sales_order ? form.sales_order : '设置'}}</a-button>
            </a-form-model-item>
          </a-col>
          <a-col :span="5">
            <a-form-model-item v-if="form.sales_order" label="日期">
              <div>{{moment(returnForm.date).format('YYYY-MM-DD')}}</div>
            </a-form-model-item>
          </a-col>
          <a-col :span="5">
            <a-form-model-item v-if="form.sales_order" label="整单折扣">
              <div>{{returnForm.discount}} %</div>
            </a-form-model-item>
          </a-col>
          <a-col :span="5">
            <a-form-model-item v-if="form.sales_order" label="实收金额">
              <div>{{returnForm.amount}}</div>
            </a-form-model-item>
          </a-col>
        </a-row>

        <div v-if="form.sales_order">
          <a-table :columns="returnGoodsColumns" :data-source="returnForm.goods_set ? returnForm.goods_set : []"
            :pagination="false" size="small">
            <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
            <div slot="amount" slot-scope="value">{{NP.round(value, 2)}}</div>
          </a-table>
        </div>
        <a-divider />

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
              <user-select v-model="form.seller" :user="form.seller" :userName="form.seller_name" />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="warehouse" label="仓库">
              <warehouse-select v-model="form.warehouse" :defaultItem="form" disabled />
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
              <client-select v-model="form.client" :defaultItem="form" disabled />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item prop="remark" label="备注">
              <a-input v-model="form.remark" allowClear />
            </a-form-model-item>
          </a-col>
          <a-col :span="8">
            <a-form-model-item style="float: right;">
              <a-button type="primary" icon="plus" @click="addGoodsModalVisible = true">添加条目</a-button>
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
          <a-button type="primary" :loading="buttonLoading">退货</a-button>
        </a-popconfirm>
        <a-button v-else @click="printInvoice">生成打印单据</a-button>
        <a-button style="float: right;" @click="resetForm">空白退货单</a-button>
      </div>
    </a-card>

    <relation-modal v-model="relationModalVisible" @select="selectSales" />
    <add-goods-modal v-model="addGoodsModalVisible" @confirm="addGoods" />
  </div>
</template>

<script>
  import { salesOrderCreate, salesOrderDestroy } from '@/api/sales'
  import { goodsColumns, returnGoodsColumns } from './columns.js'
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

      AddGoodsModal: () => import('@/components/AddGoodsModal/AddGoodsModal.vue'),
      RelationModal: () => import('./RelationModal.vue'),
    },
    props: ['selectedItem'],
    data() {
      return {
        NP,
        rules,
        moment,
        goodsColumns,
        returnGoodsColumns,
        loading: false,
        form: {},
        returnForm: {},
        addGoodsModalVisible: false,
        relationModalVisible: false,
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
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            if (this.form.goods_set.length == 0) {
              this.$message.error('请选择条目');
              return
            }
            this.loading = true;
            salesOrderCreate(this.form)
              .then((resp) => {
                this.$emit('createItem', resp.data);
                this.$message.success('退货成功');
                this.resetForm();
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              })
              .finally(() => {
                this.loading = false;
              });
          }
        });
      },
      destroy() {
        let form = { ...this.form };
        salesOrderDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.$emit('destroyItem', form.id);
            this.resetForm();
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      printInvoice() {
        window.open(`/invoice/sales?id=${this.form.id}`);
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
      selectSales(item) {
        this.form.sales_order = item.id;
        this.returnForm = item;
        this.form.client = item.client;
        this.form.client_name = item.client_name;
        this.form.warehouse = item.warehouse;
      },
      addGoods(goodsItem) {
        goodsItem.remark = '';
        this.form.goods_set.push(goodsItem);
      },
    },
    watch: {
      selectedItem() {
        this.form = this.selectedItem;
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>