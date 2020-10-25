export default {
  discount: [{ required: true, message: '请输入整单折扣', trigger: 'change' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  seller: [{ required: true, message: '请选择供应商', trigger: 'change' }],
  warehouse: [{ required: true, message: '请选择仓库', trigger: 'change' }],
  account: [{ required: true, message: '请选择账户', trigger: 'change' }],
  amount: [{ required: true, message: '请输入实收金额', trigger: 'change' }],
  remark: [{ max: 256, message: '超出最大范围 (256)', trigger: 'change' }],
  sales_order: [{ required: true, message: '请选择关联单', trigger: 'change' }],
}