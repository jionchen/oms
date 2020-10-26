import Mock from 'mockjs'


const supplierList = {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "number": "1001",
            "name": "supplier1",
            "contacts": "test",
            "phone": "111",
            "email": "111",
            "address": "test",
            "remark": "test",
            "id": 1
        }
    ]
};

const purchaseOrderList = {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "supplier": 1,
            "warehouse": 1,
            "account": 1,
            "contacts": "test",
            "amount": 0.0,
            "date": "2020-10-25T16:00:00Z",
            "remark": "",
            "id": 4,
            "number": "P2020102617092607961",
            "supplier_name": "supplier1",
            "warehouse_name": "warehouse1",
            "warehouse_address": "test",
            "account_name": "account1",
            "contacts_name": "test",
            "contacts_phone": "18571589816",
            "is_commit": true,
            "goods_set": [
                {
                    "id": 3,
                    "number": "1001",
                    "name": "goods1",
                    "unit": null,
                    "purchase_price": 10.0,
                    "quantity": 5.0,
                    "discount": 100.0,
                    "discount_price": 1000.0,
                    "amount": 50.0,
                    "discount_amount": 5000.0
                }
            ],
            "total_amount": 5000.0
        },
        {
            "supplier": 1,
            "warehouse": 1,
            "account": 1,
            "contacts": "test",
            "amount": 0.0,
            "date": "2020-10-25T16:00:00Z",
            "remark": "",
            "id": 3,
            "number": "P2020102617070685852",
            "supplier_name": "supplier1",
            "warehouse_name": "warehouse1",
            "warehouse_address": "test",
            "account_name": "account1",
            "contacts_name": "test",
            "contacts_phone": "18571589816",
            "is_commit": true,
            "goods_set": [
                {
                    "id": 2,
                    "number": "1002",
                    "name": "goods2",
                    "unit": null,
                    "purchase_price": 5.0,
                    "quantity": 5.0,
                    "discount": 100.0,
                    "discount_price": 500.0,
                    "amount": 25.0,
                    "discount_amount": 2500.0
                }
            ],
            "total_amount": 2500.0
        },
        {
            "supplier": 1,
            "warehouse": 1,
            "account": 1,
            "contacts": "test",
            "amount": 0.0,
            "date": "2020-10-25T16:00:00Z",
            "remark": "",
            "id": 2,
            "number": "P202010260033316732",
            "supplier_name": "supplier1",
            "warehouse_name": "warehouse1",
            "warehouse_address": "test",
            "account_name": "account1",
            "contacts_name": "test",
            "contacts_phone": "18571589816",
            "is_commit": true,
            "goods_set": [
                {
                    "id": 1,
                    "number": "1001",
                    "name": "goods1",
                    "unit": null,
                    "purchase_price": 10.0,
                    "quantity": 10.0,
                    "discount": 100.0,
                    "discount_price": 1000.0,
                    "amount": 100.0,
                    "discount_amount": 10000.0
                }
            ],
            "total_amount": 10000.0
        }
    ]
};

const purchasePriceRecordList = {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "goods_name": "goods2",
            "spec1": "spec5",
            "spec2": "spec4",
            "change_method": "手动修改",
            "before_change": 0.0,
            "after_change": 33.0,
            "operator": "test",
            "relation_order": null
        },
        {
            "id": 2,
            "goods_name": "goods2",
            "spec1": "spec5",
            "spec2": "spec3",
            "change_method": "手动修改",
            "before_change": 12.0,
            "after_change": 33.0,
            "operator": "test",
            "relation_order": null
        },
        {
            "id": 1,
            "goods_name": "goods1",
            "spec1": "spec1",
            "spec2": "spec3",
            "change_method": "手动修改",
            "before_change": 0.0,
            "after_change": 1.0,
            "operator": "test",
            "relation_order": null
        }
    ]
};

const purchaseOrderRetrieve = {
    "id": "PC200720104306239619",
    "supplier": 1,
    "supplier_name": "23212312",
    "warehouse": 2,
    "warehouse_name": "warehouse2",
    "account": 3,
    "account_name": "21312",
    "amount": 0.0,
    "date": "2020-07-19T16:00:00Z",
    "remark": "",
    "products": [
        {
            "product_id": "e9f1996e-c105-11ea-b73e-87e5a1fdee64",
            "name": "goods3",
            "number": "1003",
            "spec1": "spec4",
            "spec2": "spec1",
            "quantity": 1.0,
            "purchase_price": 11.0,
            "discount": 100.0,
            "discount_price": 11.0,
            "amount": 11.0,
            "discount_amount": 11.0
        }
    ],
    "is_draft": false
};

Mock.mock(/\/api\/suppliers\//, 'get', supplierList);
Mock.mock(/\/api\/purchase_orders\/.+\//, 'get', purchaseOrderRetrieve);
Mock.mock(/\/api\/purchase_orders\//, 'get', purchaseOrderList);
Mock.mock(/\/api\/change_records\//, 'get', purchasePriceRecordList);
