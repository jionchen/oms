<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑分类' : '新增分类' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 16 }">
          <a-row>
            <a-col :span="24">
              <a-form-model-item prop="number" label="分类编号">
                <a-input v-model="form.number" :disabled="form.id" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item prop="name" label="分类名称">
                <a-input v-model="form.name" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item prop="remark" label="备注">
                <a-input v-model="form.remark" />
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { categoryCreate, categoryUpdate } from '@/api/goods'
  import rules from './rules.js'

  export default {
    name: 'FormModal',
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
            let func = this.form.id ? categoryUpdate : categoryCreate;
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