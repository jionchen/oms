export default [
  {
    title: '商品编号',
    dataIndex: 'number',
    sorter: true,
  },
  {
    title: '商品名称',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '商品单位',
    dataIndex: 'unit',
  },
  {
    title: '商品分类',
    dataIndex: 'category_name',
  },
  {
    title: '采购价',
    dataIndex: 'purchase_price',
    sorter: true,
  },
  {
    title: '零售价',
    dataIndex: 'retail_price',
    sorter: true,
  },
  {
    title: '状态',
    dataIndex: 'is_active',
    scopedSlots: { customRender: 'is_active' },
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
  },
]