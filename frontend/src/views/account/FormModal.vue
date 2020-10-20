<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑账户' : '新增账户' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 16 }">
          <a-row>
            <a-col :span="24">
              <a-form-model-item prop="number" label="账户编号">
                <a-input v-model="form.number" :disabled="form.id" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item prop="name" label="账户名称">
                <a-input v-model="form.name" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item prop="account" label="账号">
                <a-input v-model="form.account" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item prop="holder" label="开户人">
                <a-input v-model="form.holder" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item prop="type" label="类型">
                <a-select>
                  <a-select-option value="cash">现金</a-select-option>
                  <a-select-option value="bank_accounts">银行账户</a-select-option>
                  <a-select-option value="alipay">支付宝</a-select-option>
                  <a-select-option value="wechat_pay">微信支付</a-select-option>
                  <a-select-option value="other">其他</a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item prop="remark" label="备注">
                <a-input v-model="form.remark" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item prop="is_active" label="状态">
                <a-select v-model="form.is_active">
                  <a-select-option :value="true">激活</a-select-option>
                  <a-select-option :value="false">冻结</a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { accountCreate, accountUpdate } from '@/api/account'
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
            let func = this.form.id ? accountUpdate : accountCreate;
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