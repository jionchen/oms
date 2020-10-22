export default [
  {
    key: '1', name: '报表管理', icon: 'line-chart', submenus: [
      { key: '/sales_report', name: '销售报表' },
      { key: '/purchase_report', name: '采购报表' },
      { key: '/inventory', name: '库存报表' },
    ]
  },
  {
    key: '2', name: '基础数据', icon: 'table', submenus: [
      { key: '/warehouse', name: '仓库管理' },
      { key: '/supplier', name: '供应商管理' },
      { key: '/client', name: '客户管理' },
      { key: '/category', name: '商品分类' },
      { key: '/goods', name: '商品管理' },
      { key: '/account', name: '结算账户' },
    ]
  },
  {
    key: '3', name: '采购管理', icon: 'shopping-cart', submenus: [
      { key: '/purchase_order', name: '采购开单' },
      { key: '/purchase_return', name: '采购退货' },
      { key: '/change_record', name: '采购价记录' },
    ]
  },
  {
    key: '4', name: '销售管理', icon: 'shop', submenus: [
      { key: '/sales_order', name: '销售开单' },
      { key: '/sales_return', name: '销售退货' },
      { key: '/sales_task', name: '销售任务' },
    ]
  },
  {
    key: '5', name: '库存管理', icon: 'database', submenus: [
      { key: '/into_warehouse', name: '入库作业' },
      { key: '/out_warehouse', name: '出库作业' },
      { key: '/counting_list', name: '库存盘点' },
      { key: '/requisition', name: '库存调拨' },
      { key: '/flow', name: '库存流水' },
    ]
  },
  {
    key: '6', name: '财务管理', icon: 'dollar', submenus: [
      { key: '/financial_statistics', name: '收支统计' },
      { key: '/sales_statistics', name: '销售收款统计' },
      { key: '/purchase_statistics', name: '采购付款统计' },
    ]
  },

  {
    key: '7', name: '系统管理', icon: 'team', submenus: [
      { key: '/role', name: '角色管理' },
      { key: '/subuser', name: '账号管理' },
    ]
  },
]