import Mock from 'mockjs'


const categoryList = {
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "number": "1001",
      "name": "食品",
      "description": "",
      "id": 1
    },
    {
      "number": "1002",
      "name": "日用品",
      "description": "",
      "id": 2
    }
  ]
};


const goodsList = {
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "number": "1001",
      "name": "apple",
      "unit": "个",
      "category": null,
      "purchase_price": 0.0,
      "retail_price": 0.0,
      "shelf_life": null,
      "shelf_life_warnning_days": null,
      "inventory_upper": null,
      "inventory_lower": null,
      "inventory_warning": false,
      "is_active": true,
      "id": 1,
      "category_name": null
    },
    {
      "number": "1002",
      "name": "orange",
      "unit": "个",
      "category": null,
      "purchase_price": 0.0,
      "retail_price": 0.0,
      "shelf_life": null,
      "shelf_life_warnning_days": null,
      "inventory_upper": 5.0,
      "inventory_lower": 1000.0,
      "inventory_warning": true,
      "is_active": true,
      "id": 2,
      "category_name": null
    }
  ]
}

Mock.mock(/\/api\/categories\//, 'get', categoryList);
Mock.mock(/\/api\/goods\//, 'get', goodsList);
