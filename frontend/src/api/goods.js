import Cookies from 'js-cookie'
import axios from 'axios'


// Category
export function categoryList(params) {
  return axios({
    url: '/api/categories/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function categoryCreate(form) {
  return axios({
    url: '/api/categories/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function categoryUpdate(form) {
  return axios({
    url: `/api/categories/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function categoryDestroy(id) {
  return axios({
    url: `/api/categories/${id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

export let categoryExportExcel = '/api/export/categories/'

export function categoryImportExcel(data) {
  return axios({
    url: '/api/import/categories/',
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
      'Content-Type': 'multipart/form-data',
    },
    method: 'post',
    data,
  })
}

// Goods
export function goodsList(params) {
  return axios({
    url: '/api/goods/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function goodsCreate(form) {
  return axios({
    url: '/api/goods/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function goodsUpdate(form) {
  return axios({
    url: `/api/goods/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function goodsDestroy(id) {
  return axios({
    url: `/api/goods/${id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

export let goodsExportExcel = '/api/export/goods/'

export function goodsImportExcel(data) {
  return axios({
    url: '/api/import/goods/',
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
      'Content-Type': 'multipart/form-data',
    },
    method: 'post',
    data,
  })
}
