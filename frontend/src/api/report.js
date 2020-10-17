import Cookies from 'js-cookie'
import axios from 'axios'

// PurchaseReport
export function purchaseReportList(params) {
  return axios({
    url: '/api/purchase_reports/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// SalesReport
export function salesReportList(params) {
  return axios({
    url: '/api/sales_reports/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// FinancialStatistics
export function financialStatistics(params) {
  return axios({
    url: '/api/financial_statistics/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// PurchaseStatistics
export function purchaseStatistics(params) {
  return axios({
    url: '/api/purchase_statistics/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// SalesStatistics
export function salesStatistics(params) {
  return axios({
    url: '/api/sales_statistics/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}


// SalesTrend
export function salesTrendList(params) {
  return axios({
    url: '/api/sales_trends/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// ProfitTrend
export function profitTrendList(params) {
  return axios({
    url: '/api/financial_reports/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}
