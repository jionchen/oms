import Mock from 'mockjs'


const warehouseList = {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "number": "1001",
            "name": "test",
            "manager": null,
            "address": "",
            "remark": "",
            "is_active": true,
            "id": 1,
            "create_date": "2020-10-20T07:39:07.009663Z",
            "update_date": "2020-10-20T07:39:07.009738Z"
        },
        {
            "number": "1002",
            "name": "uuuu",
            "manager": null,
            "address": "",
            "remark": "",
            "is_active": false,
            "id": 2,
            "create_date": "2020-10-20T07:39:20.065995Z",
            "update_date": "2020-10-20T07:39:20.066118Z"
        }
    ]
};

const inventoryList = {
    "results": [
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec2, spec1, spec6, spec5",
            "spec2": "spec3, spec4",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec2, spec1, spec6, spec5",
            "spec2": "spec3, spec4",
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods2",
            "goods_number": "1002",
            "brand": null,
            "spec1": "spec3",
            "spec2": null,
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods2",
            "goods_number": "1002",
            "brand": null,
            "spec1": "spec3",
            "spec2": null,
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec1",
            "spec2": "spec3",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec1",
            "spec2": "spec3",
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec1",
            "spec2": "spec4",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec1",
            "spec2": "spec4",
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec2",
            "spec2": "spec3",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec2",
            "spec2": "spec3",
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec2",
            "spec2": "spec4",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec2",
            "spec2": "spec4",
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec5",
            "spec2": "spec3",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec5",
            "spec2": "spec3",
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec5",
            "spec2": "spec4",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec5",
            "spec2": "spec4",
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec6",
            "spec2": "spec3",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec6",
            "spec2": "spec3",
            "category": null,
            "warehouse": "warehouse2",
            "quantity": 0.0,
            "purchase_price": 0.0
        },
        {
            "goods_name": "goods1",
            "goods_number": "1001",
            "brand": "brand1",
            "spec1": "spec6",
            "spec2": "spec4",
            "category": null,
            "warehouse": "warehouse1",
            "quantity": 0.0,
            "purchase_price": 0.0
        }
    ],
    "total_value": 0.0,
    "total_quantity": 0.0
};

const flowList = {
    "count": 0,
    "results": [],
}

const countingListList =
{
    "count": 11,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 13,
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "total_counting": 4.0,
            "total_profit": -9.0,
            "profit_amount": -90.0,
            "remark": "212",
            "is_draft": false,
            "products": [
                {
                    "product_id": "e9f1996e-c105-11ea-b73e-87e5a1fdee64",
                    "name": "goods3",
                    "number": "1003",
                    "spec1": "spec4",
                    "spec2": "spec1",
                    "counting": 2.0,
                    "before_counting": 11.0,
                    "total_profit": -9.0,
                    "profit_amount": -90.0
                },
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "number": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "counting": 2.0,
                    "before_counting": 2.0,
                    "total_profit": 0.0,
                    "profit_amount": 0.0
                }
            ],
            "date": "2020-07-10"
        },
        {
            "id": 10,
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "total_counting": 11.0,
            "total_profit": -1.0,
            "profit_amount": -10.0,
            "remark": "213",
            "is_draft": false,
            "products": [
                {
                    "product_id": "e9f1996e-c105-11ea-b73e-87e5a1fdee64",
                    "name": "goods3",
                    "number": "1003",
                    "spec1": "spec4",
                    "spec2": "spec1",
                    "counting": 11.0,
                    "before_counting": 12.0,
                    "total_profit": -1.0,
                    "profit_amount": -10.0
                }
            ],
            "date": "2020-07-10"
        },
        {
            "id": 9,
            "warehouse": 2,
            "warehouse_name": "warehouse2",
            "total_counting": 3.0,
            "total_profit": -3.0,
            "profit_amount": 0.0,
            "remark": "",
            "is_draft": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "number": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "counting": 3.0,
                    "before_counting": 6.0,
                    "total_profit": -3.0,
                    "profit_amount": -0.0
                }
            ],
            "date": "2020-07-10"
        },
        {
            "id": 8,
            "warehouse": 2,
            "warehouse_name": "warehouse2",
            "total_counting": 6.0,
            "total_profit": 4.0,
            "profit_amount": 0.0,
            "remark": "",
            "is_draft": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "number": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "counting": 6.0,
                    "before_counting": 2.0,
                    "total_profit": 4.0,
                    "profit_amount": 0.0
                }
            ],
            "date": "2020-07-10"
        },
        {
            "id": 7,
            "warehouse": 2,
            "warehouse_name": "warehouse2",
            "total_counting": 2.0,
            "total_profit": 2.0,
            "profit_amount": 0.0,
            "remark": "1212",
            "is_draft": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "number": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "counting": 2.0,
                    "before_counting": 0.0,
                    "total_profit": 2.0,
                    "profit_amount": 0.0
                }
            ],
            "date": "2020-07-10"
        },
        {
            "id": 6,
            "warehouse": 2,
            "warehouse_name": "warehouse2",
            "total_counting": 0.0,
            "total_profit": -10.0,
            "profit_amount": 0.0,
            "remark": "55555",
            "is_draft": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "number": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "counting": 0.0,
                    "before_counting": 10.0,
                    "total_profit": -10.0,
                    "profit_amount": -0.0
                }
            ],
            "date": "2020-07-10"
        },
        {
            "id": 5,
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "total_counting": 14.0,
            "total_profit": 0.0,
            "profit_amount": 0.0,
            "remark": "111",
            "is_draft": false,
            "products": [
                {
                    "product_id": "e9f1996e-c105-11ea-b73e-87e5a1fdee64",
                    "name": "goods3",
                    "number": "1003",
                    "spec1": "spec4",
                    "spec2": "spec1",
                    "counting": 12.0,
                    "before_counting": 12.0,
                    "total_profit": 0.0,
                    "profit_amount": 0.0
                },
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "number": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "counting": 2.0,
                    "before_counting": 2.0,
                    "total_profit": 0.0,
                    "profit_amount": 0.0
                }
            ],
            "date": "2020-07-10"
        },
        {
            "id": 4,
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "total_counting": 14.0,
            "total_profit": 28.0,
            "profit_amount": 210.0,
            "remark": "111",
            "is_draft": false,
            "products": [],
            "date": "2020-07-10"
        },
        {
            "id": 3,
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "total_counting": 0.0,
            "total_profit": 0.0,
            "profit_amount": 0.0,
            "remark": "111",
            "is_draft": false,
            "products": [],
            "date": "2020-07-10"
        },
        {
            "id": 2,
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "total_counting": 0.0,
            "total_profit": 0.0,
            "profit_amount": 0.0,
            "remark": "111",
            "is_draft": false,
            "products": [],
            "date": "2020-07-10"
        },
        {
            "id": 1,
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "total_counting": 0.0,
            "total_profit": 0.0,
            "profit_amount": 0.0,
            "remark": "111",
            "is_draft": false,
            "products": [],
            "date": "2020-07-10"
        }
    ]
};

const requisitionList = {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 7,
            "out_warehouse": 1,
            "out_warehouse_name": "warehouse1",
            "into_warehouse": 2,
            "into_warehouse_name": "warehouse2",
            "date": "2020-07-10",
            "remark": "121",
            "is_draft": false,
            "is_undo": false,
            "products": [
                {
                    "product_id": "e9f1996e-c105-11ea-b73e-87e5a1fdee64",
                    "name": "goods3",
                    "number": "1003",
                    "spec1": "spec4",
                    "spec2": "spec1",
                    "quantity": 12.0
                }
            ]
        }
    ]
}

const countingListRetrieve = {
    "id": "9",
    "warehouse": 2,
    "warehouse_name": "warehouse2",
    "total_counting": 3.0,
    "total_profit": -3.0,
    "profit_amount": 0.0,
    "remark": "",
    "is_draft": false,
    "products": [
        {
            "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
            "name": "goods1",
            "number": "1001",
            "spec1": "spec1",
            "spec2": "spec3",
            "counting": 3.0,
            "before_counting": 6.0,
            "total_profit": -3.0,
            "profit_amount": -0.0
        }
    ],
    "date": "2020-07-10T00:00:00Z"
};

const requisitionRetrievev = {
    "id": "8",
    "out_warehouse": 1,
    "out_warehouse_name": "warehouse1",
    "into_warehouse": 2,
    "into_warehouse_name": "warehouse2",
    "date": "2020-07-11T00:00:00Z",
    "remark": "",
    "is_draft": false,
    "is_undo": false,
    "products": [
        {
            "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
            "name": "goods1",
            "number": "1001",
            "spec1": "spec1",
            "spec2": "spec3",
            "quantity": 1.0
        }
    ]
};

Mock.mock(/\/api\/warehouses\//, 'get', warehouseList);
Mock.mock(/\/api\/inventory\//, 'get', inventoryList);
Mock.mock(/\/api\/flows\//, 'get', flowList);
Mock.mock(/^\/api\/counting_list\/$/, 'get', countingListList);
Mock.mock(/\/api\/counting_list\//, 'get', countingListRetrieve);
Mock.mock(/^\/api\/requisition\/$/, 'get', requisitionList);
Mock.mock(/\/api\/requisition\//, 'get', requisitionRetrievev);
