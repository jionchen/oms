export default [
  {
    title: '分类编号',
    dataIndex: 'number',
    sorter: true,
  },
  {
    title: '分类名称',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '备注',
    dataIndex: 'remark',
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
  },
]