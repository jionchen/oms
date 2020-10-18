export default {
  number: [
    { required: true, message: '请输入商品编号', trigger: 'change' },
    { max: 32, message: '超出最大长度 (32)', trigger: 'change' },
  ],
  name: [
    { required: true, message: '请输入商品名称', trigger: 'change' },
    { max: 256, message: '超出最大长度 (64)', trigger: 'change' },
  ],
  unit: [{ max: 32, message: '超出最大长度 (32)', trigger: 'change' }],
  description: [{ max: 256, message: '超出最大长度 (256)', trigger: 'change' }],
}