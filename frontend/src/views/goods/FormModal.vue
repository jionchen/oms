<template>
  <div>
    <a-modal v-model="visible" width="756px" :confirmLoading="loading" :maskClosable="false" @cancel="cancel"
      @ok="confirm">
      <div slot="title">{{form.id ? '编辑商品' : '新增商品' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
          <a-row>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="number" label="商品编号">
                <a-input v-model="form.number" :disabled="form.id" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="name" label="商品名称">
                <a-input v-model="form.name" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="unit" label="单位">
                <a-input v-model="form.unit" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="category" label="分类">
                <category-select v-model="form.category" :defaultItem="form" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="purchase_price" label="采购价">
                <a-input-number v-model="form.purchase_price" :precision="2" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="retail_price" label="零售价">
                <a-input-number v-model="form.retail_price" :precision="2" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="shelf_life" label="保质期">
                <a-input-number v-model="form.shelf_life" :precision="0" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="shelf_life_warnning_days" label="预警天数">
                <a-input-number v-model="form.shelf_life_warnning_days" placeholder="保质期到期前天数" :precision="0"
                  style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="inventory_warning" label="库存预警">
                <a-select v-model="form.inventory_warning">
                  <a-select-option :value="true">开启</a-select-option>
                  <a-select-option :value="false">关闭</a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="is_active" label="状态">
                <a-select v-model="form.is_active">
                  <a-select-option :value="true">激活</a-select-option>
                  <a-select-option :value="false">冻结</a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="inventory_upper" label="库存上限">
                <a-input-number v-model="form.inventory_upper" :precision="2" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="inventory_lower" label="库存下限">
                <a-input-number v-model="form.inventory_lower" :precision="2" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { goodsCreate, goodsUpdate } from '@/api/goods'
  import rules from './rules.js'

  export default {
    name: 'FormModal',
    components: {
      CategorySelect: () => import('@/components/CategorySelect/CategorySelect'),
    },
    props: ['visible', 'form'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules,
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? goodsUpdate : goodsCreate;
            func(this.form)
              .then(resp => {
                this.$message.success(this.form.id ? '修改成功' : '新增成功');
                this.$emit(this.form.id ? 'update' : 'create', resp.data);
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
        this.$refs.form.resetFields();
      },
    },
  }
</script>

<style scoped>
</style>