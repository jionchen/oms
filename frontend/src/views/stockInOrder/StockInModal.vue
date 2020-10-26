<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{`入库 - ${stockInGoods.goods_number}`}}</div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="quantity" label="入库数量">
          <a-input-number v-model="form.quantity" :min="0" style="width: 100%;" />
        </a-form-model-item>
        <a-form-model-item v-if="stockInGoods.shelf_life_warnning" prop="production_date" label="生产日期">
          <a-date-picker v-model="form.production_date" :showToday="false" :allowClear="false" style="width: 100%;" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { stockInGoodsStockIn } from '@/api/warehouse'
  import rules from './rules.js'

  export default {
    name: 'StockInModal',
    props: ['visible', 'stockInGoods'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules,
        form: { quantity: undefined, production_date: undefined },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            stockInGoodsStockIn({id: this.stockInGoods.id, ...this.form})
              .then(resp => {
                this.$emit('update', resp.data);
                this.$message.success('入库成功');
                this.cancel();
              })
              .catch(err => {
                this.$message.error(this.errorToString(err));
              })
              .finally(() => {
                this.loading = false;
              });
          }
        });
      },
      cancel() {
        this.$emit('cancel', false);
        this.form = { quantity: undefined, production_date: undefined };
        this.$refs.form.resetFields();
      },
    },
  }
</script>

<style scoped>
</style>