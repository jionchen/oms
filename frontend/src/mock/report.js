import Mock from 'mockjs'


const purchaseReportList = {
  "total": {
      "times": 22,
      "quantity": 202.0,
      "amount": 328.0
  },
  "results": [
      {
          "goods_number": "1001",
          "goods_name": "goods1",
          "brand_name": "brand1",
          "category_name": "category1",
          "quantity": 36.0,
          "min_purchase_price": 0.0,
          "max_purchase_price": 10.0,
          "avg_purchase_price": 7.777777777777778
      },
      {
          "goods_number": "1002",
          "goods_name": "goods2",
          "brand_name": null,
          "category_name": null,
          "quantity": 4.0,
          "min_purchase_price": 0.0,
          "max_purchase_price": 112.0,
          "avg_purchase_price": 44.5
      },
      {
          "goods_number": "1002",
          "goods_name": "goods2",
          "brand_name": null,
          "category_name": "category1",
          "quantity": 161.0,
          "min_purchase_price": 0.0,
          "max_purchase_price": 0.0,
          "avg_purchase_price": 0.0
      },
      {
          "goods_number": "1003",
          "goods_name": "goods3",
          "brand_name": "brand2",
          "category_name": "category1",
          "quantity": 1.0,
          "min_purchase_price": 10.0,
          "max_purchase_price": 10.0,
          "avg_purchase_price": 10.0
      },
      {
        "goods_number": "1001",
        "goods_name": "goods1",
        "brand_name": "brand1",
        "category_name": "category1",
        "quantity": 36.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 7.777777777777778
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": null,
        "quantity": 4.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 112.0,
        "avg_purchase_price": 44.5
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": "category1",
        "quantity": 161.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 0.0,
        "avg_purchase_price": 0.0
    },
    {
        "goods_number": "1003",
        "goods_name": "goods3",
        "brand_name": "brand2",
        "category_name": "category1",
        "quantity": 1.0,
        "min_purchase_price": 10.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 10.0
    },
    {
        "goods_number": "1001",
        "goods_name": "goods1",
        "brand_name": "brand1",
        "category_name": "category1",
        "quantity": 36.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 7.777777777777778
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": null,
        "quantity": 4.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 112.0,
        "avg_purchase_price": 44.5
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": "category1",
        "quantity": 161.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 0.0,
        "avg_purchase_price": 0.0
    },
    {
        "goods_number": "1003",
        "goods_name": "goods3",
        "brand_name": "brand2",
        "category_name": "category1",
        "quantity": 1.0,
        "min_purchase_price": 10.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 10.0
    },
    {
        "goods_number": "1001",
        "goods_name": "goods1",
        "brand_name": "brand1",
        "category_name": "category1",
        "quantity": 36.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 7.777777777777778
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": null,
        "quantity": 4.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 112.0,
        "avg_purchase_price": 44.5
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": "category1",
        "quantity": 161.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 0.0,
        "avg_purchase_price": 0.0
    },
    {
        "goods_number": "1003",
        "goods_name": "goods3",
        "brand_name": "brand2",
        "category_name": "category1",
        "quantity": 1.0,
        "min_purchase_price": 10.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 10.0
    },
    {
        "goods_number": "1001",
        "goods_name": "goods1",
        "brand_name": "brand1",
        "category_name": "category1",
        "quantity": 36.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 7.777777777777778
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": null,
        "quantity": 4.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 112.0,
        "avg_purchase_price": 44.5
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": "category1",
        "quantity": 161.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 0.0,
        "avg_purchase_price": 0.0
    },
    {
        "goods_number": "1003",
        "goods_name": "goods3",
        "brand_name": "brand2",
        "category_name": "category1",
        "quantity": 1.0,
        "min_purchase_price": 10.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 10.0
    },
    {
        "goods_number": "1001",
        "goods_name": "goods1",
        "brand_name": "brand1",
        "category_name": "category1",
        "quantity": 36.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 7.777777777777778
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": null,
        "quantity": 4.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 112.0,
        "avg_purchase_price": 44.5
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": "category1",
        "quantity": 161.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 0.0,
        "avg_purchase_price": 0.0
    },
    {
        "goods_number": "1003",
        "goods_name": "goods3",
        "brand_name": "brand2",
        "category_name": "category1",
        "quantity": 1.0,
        "min_purchase_price": 10.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 10.0
    },
    {
        "goods_number": "1001",
        "goods_name": "goods1",
        "brand_name": "brand1",
        "category_name": "category1",
        "quantity": 36.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 7.777777777777778
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": null,
        "quantity": 4.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 112.0,
        "avg_purchase_price": 44.5
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": "category1",
        "quantity": 161.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 0.0,
        "avg_purchase_price": 0.0
    },
    {
        "goods_number": "1003",
        "goods_name": "goods3",
        "brand_name": "brand2",
        "category_name": "category1",
        "quantity": 1.0,
        "min_purchase_price": 10.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 10.0
    },
    {
        "goods_number": "1001",
        "goods_name": "goods1",
        "brand_name": "brand1",
        "category_name": "category1",
        "quantity": 36.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 7.777777777777778
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": null,
        "quantity": 4.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 112.0,
        "avg_purchase_price": 44.5
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": "category1",
        "quantity": 161.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 0.0,
        "avg_purchase_price": 0.0
    },
    {
        "goods_number": "1003",
        "goods_name": "goods3",
        "brand_name": "brand2",
        "category_name": "category1",
        "quantity": 1.0,
        "min_purchase_price": 10.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 10.0
    },
    {
        "goods_number": "1001",
        "goods_name": "goods1",
        "brand_name": "brand1",
        "category_name": "category1",
        "quantity": 36.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 7.777777777777778
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": null,
        "quantity": 4.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 112.0,
        "avg_purchase_price": 44.5
    },
    {
        "goods_number": "1002",
        "goods_name": "goods2",
        "brand_name": null,
        "category_name": "category1",
        "quantity": 161.0,
        "min_purchase_price": 0.0,
        "max_purchase_price": 0.0,
        "avg_purchase_price": 0.0
    },
    {
        "goods_number": "1003",
        "goods_name": "goods3",
        "brand_name": "brand2",
        "category_name": "category1",
        "quantity": 1.0,
        "min_purchase_price": 10.0,
        "max_purchase_price": 10.0,
        "avg_purchase_price": 10.0
    },
    
  ]
};


const salesReportList = {
    "total": {
        "cost": 16.0,
        "quantity": 28.0,
        "amount": 164.0
    },
    "results": [
        {
            "spec1": "spec1",
            "spec2": "spec3",
            "quantity": 1.0,
            "goods_number": "1001",
            "goods_name": "goods1",
            "brand_name": "brand1",
            "category_name": "category1",
            "seller_name": "11",
            "warehouse_name": "warehouse1",
            "date": "2020-07-11T00:00:00Z",
            "relation_order": 9
        },
        {
            "spec1": "spec1",
            "spec2": "spec3",
            "quantity": 1.0,
            "goods_number": "1001",
            "goods_name": "goods1",
            "brand_name": "brand1",
            "category_name": "category1",
            "seller_name": "11",
            "warehouse_name": "warehouse2",
            "date": "2020-06-30T16:00:00Z",
            "relation_order": 11
        },
        {
            "spec1": "spec1",
            "spec2": "spec3",
            "quantity": 12.0,
            "goods_number": "1001",
            "goods_name": "goods1",
            "brand_name": "brand1",
            "category_name": "category1",
            "seller_name": "11",
            "warehouse_name": "warehouse1",
            "date": "2020-07-08T00:00:00Z",
            "relation_order": 7
        },
        {
            "spec1": "spec1",
            "spec2": "spec3",
            "quantity": 2.0,
            "goods_number": "1001",
            "goods_name": "goods1",
            "brand_name": "brand1",
            "category_name": "category1",
            "seller_name": "11",
            "warehouse_name": "warehouse1",
            "date": "2020-07-12T00:00:00Z",
            "relation_order": 10
        },
        {
            "spec1": "spec1",
            "spec2": "spec3",
            "quantity": 2.0,
            "goods_number": "1001",
            "goods_name": "goods1",
            "brand_name": "brand1",
            "category_name": "category1",
            "seller_name": "11",
            "warehouse_name": "warehouse2",
            "date": "2020-07-08T00:00:00Z",
            "relation_order": 6
        },
        {
            "spec1": "spec4",
            "spec2": "spec1",
            "quantity": 10.0,
            "goods_number": "1003",
            "goods_name": "goods3",
            "brand_name": "brand2",
            "category_name": "category1",
            "seller_name": "11",
            "warehouse_name": "warehouse1",
            "date": "2020-07-08T00:00:00Z",
            "relation_order": 8
        }
    ]
}


const salesTrendList = {
    "results": [
        {
            "date": "2020-07-08",
            "warehouse_name": "warehouse1",
            "amount": 274.0
        },
        {
            "date": "2020-07-11",
            "warehouse_name": "warehouse1",
            "amount": 14.0
        },
        {
            "date": "2020-07-12",
            "warehouse_name": "warehouse1",
            "amount": 28.0
        },
        {
            "date": "2020-07-15",
            "warehouse_name": "warehouse1",
            "amount": 98.0
        },
        {
            "date": "2020-07-08",
            "warehouse_name": "warehouse2",
            "amount": 27.5
        },
        {
            "date": "2020-06-30",
            "warehouse_name": "warehouse2",
            "amount": 14.0
        }
    ],
    "warehouse_list": [
        "warehouse1",
        "warehouse2",
        "333"
    ]
};

const profitTrendList = {
    "results": [],
    "warehouse_list": []
}

Mock.mock(/\/api\/purchase_reports\//, 'get', purchaseReportList);
Mock.mock(/\/api\/sales_reports\//, 'get', salesReportList);
Mock.mock(/\/api\/sales_trends\//, 'get', salesTrendList);
Mock.mock(/\/api\/profit_trends\//, 'get', profitTrendList);
