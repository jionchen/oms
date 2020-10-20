export default [
  {
    title: '客户编号',
    dataIndex: 'number',
    sorter: true,
  },
  {
    title: '客户名称',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '联系人',
    dataIndex: 'contacts',
  },
  {
    title: '电话',
    dataIndex: 'phone',
  },
  {
    title: '地址',
    dataIndex: 'address',
  },
  {
    title: '邮箱',
    dataIndex: 'email',
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
  },
]