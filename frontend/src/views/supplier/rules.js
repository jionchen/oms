export default {
  number: [
    { required: true, message: '请输入编号', trigger: 'change' },
    { max: 32, message: '超出最大长度 (32)', trigger: 'change' },
  ],
  name: [
    { required: true, message: '请输入名称', trigger: 'change' },
    { max: 64, message: '超出最大长度 (64)', trigger: 'change' },
  ],
  manager: [{ max: 64, message: '超出最大长度 (64)', trigger: 'change' }],
  phone: [{ max: 12, message: '超出最大长度 (12)', trigger: 'change' }],
  address: [{ max: 256, message: '超出最大长度 (256)', trigger: 'change' }],
  email: [{ max: 256, message: '超出最大长度 (256)', trigger: 'change' }],
  bank_account: [{ max: 64, message: '超出最大长度 (64)', trigger: 'change' }],
  bank_name: [{ max: 64, message: '超出最大长度 (64)', trigger: 'change' }],
  url: [{ max: 256, message: '超出最大长度 (256)', trigger: 'change' }],
  remark: [{ max: 256, message: '超出最大长度 (256)', trigger: 'change' }],
}