import Cookies from 'js-cookie'
import axios from 'axios'

// SalesOrder
export function salesOrderList(params) {
  return axios({
    url: '/api/sales_orders/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function salesOrderCreate(form) {
  return axios({
    url: '/api/sales_orders/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function salesOrderRetrieve(params) {
  return axios({
    url: `/api/sales_orders/${params.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function salesOrderDestroy(form) {
  return axios({
    url: `/api/sales_orders/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

export function salesOrderCommit(form) {
  return axios({
    url: `/api/sales_orders/${form.id}/commit/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

// SalesTask
export function salesTaskList(params) {
  return axios({
    url: '/api/sales_tasks/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function salesTaskCreate(form) {
  return axios({
    url: '/api/sales_tasks/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

// salesOrderProfit
export function salesOrderProfitList(params) {
  return axios({
    url: '/api/sales_order_profit/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function salesOrderProfitUpdate(form) {
  return axios({
    url: `/api/sales_order_profit/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function salesOrderTotalProfit(params) {
  return axios({
    url: '/api/sales_order_profit/total_profit/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// Client
export function clientList(params) {
  return axios({
    url: '/api/clients/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function clientCreate(form) {
  return axios({
    url: '/api/clients/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function clientUpdate(form) {
  return axios({
    url: `/api/clients/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function clientDestroy(id) {
  return axios({
    url: `/api/clients/${id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

export let clientExportExcel = '/api/export/clients/'

export function clientImportExcel(data) {
  return axios({
    url: '/api/import/clients/',
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
      'Content-Type': 'multipart/form-data',
    },
    method: 'post',
    data,
  })
}

// SalesPaymentRecord
export function salesPaymentRecord(params) {
  return axios({
    url: '/api/sales_payment_records/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// PaymentRecord
export function paymentRecordCreate(form) {
  return axios({
    url: `/api/sales_order/payment/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}