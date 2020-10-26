export const recordColumns = [
  {
    title: '状态',
    dataIndex: 'status',
    scopedSlots: { customRender: 'status' },
  },
  {
    title: '仓库',
    dataIndex: 'warehouse_name',
  },
  {
    title: '日期',
    dataIndex: 'date',
    scopedSlots: { customRender: 'date' },
  },
]

export const goodsColumns = [
  {
    title: '编号',
    dataIndex: 'goods_number',
  },
  {
    title: '名称',
    dataIndex: 'goods_name',
  },
  {
    title: '单位',
    dataIndex: 'goods_unit',
  },
  {
    title: '数量',
    dataIndex: 'quantity',
  },
  {
    title: '已入库数量',
    dataIndex: 'quantity_completed',
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
  },
]