export const recordColumns = [
  {
    title: '状态',
    dataIndex: 'status',
    scopedSlots: { customRender: 'status' },
  },
  {
    title: '日期',
    dataIndex: 'date',
    scopedSlots: { customRender: 'date' },
  },
  {
    title: '销售员',
    dataIndex: 'seller',
  },
]

export const goodsColumns = [
  {
    title: '编号',
    dataIndex: 'number',
  },
  {
    title: '名称',
    dataIndex: 'name',
  },
  {
    title: '单位',
    dataIndex: 'unit',
  },
  {
    title: '数量',
    dataIndex: 'quantity',
  },
  {
    title: '单价',
    dataIndex: 'retail_price',
  },
  {
    title: '金额',
    dataIndex: 'amount',
    key: 'amount',
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
  },
]