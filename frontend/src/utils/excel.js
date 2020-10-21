export function exportExcel(url, filename) {
  let link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `${filename}.xls`);
  document.body.appendChild(link);
  link.click();
}