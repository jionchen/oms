import Cookies from 'js-cookie'
import axios from 'axios'

// Supplier
export function supplierList(params) {
  return axios({
    url: '/api/suppliers/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function supplierCreate(form) {
  return axios({
    url: '/api/suppliers/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function supplierUpdate(form) {
  return axios({
    url: `/api/suppliers/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function supplierDestroy(id) {
  return axios({
    url: `/api/suppliers/${id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

export let supplierExportExcel = '/api/export/suppliers/'

export function supplierImportExcel(data) {
  return axios({
    url: '/api/import/suppliers/',
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
      'Content-Type': 'multipart/form-data',
    },
    method: 'post',
    data,
  })
}

// PurchaseOrder
export function purchaseOrderList(params) {
  return axios({
    url: '/api/purchase_orders/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function purchaseOrderCreate(form) {
  return axios({
    url: '/api/purchase_orders/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function purchaseOrderRetrieve(params) {
  return axios({
    url: `/api/purchase_orders/${params.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function purchaseOrderCommit(id) {
  return axios({
    url: `/api/purchase_orders/${id}/commit/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
  })
}

export function purchaseOrderDestroy(form) {
  return axios({
    url: `/api/purchase_orders/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// PurchasePriceRecord
export function purchasePriceRecordList() {
  return axios({
    url: '/api/purchase_price_records/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

// PurchasePaymentRecord
export function purchasePaymentRecord(params) {
  return axios({
    url: '/api/purchase_payment_records/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// PaymentRecord
export function paymentRecordCreate(form) {
  return axios({
    url: `/api/purchase_order/payment/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}