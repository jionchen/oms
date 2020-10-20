export default [
  {
    title: '编号',
    dataIndex: 'number',
    sorter: true,
  },
  {
    title: '名称',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '负责人',
    dataIndex: 'address',
  },
  {
    title: '电话',
    dataIndex: 'address',
  },
  {
    title: '地址',
    dataIndex: 'address',
  },
  {
    title: '邮箱',
    dataIndex: 'address',
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