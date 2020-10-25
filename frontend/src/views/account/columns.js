export default [
  {
    title: '账户编号',
    dataIndex: 'number',
    sorter: true,
  },
  {
    title: '账户名称',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '类型',
    dataIndex: 'type',
    scopedSlots: { customRender: 'type' },
  },
  {
    title: '备注',
    dataIndex: 'remark',
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