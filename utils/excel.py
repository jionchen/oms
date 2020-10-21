from rest_framework.exceptions import ValidationError
from django.http.response import HttpResponse
import itertools
import xlwt
import xlrd


def export_excel(data, name, fields):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment;filename={name}.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(name)
    
    # 创建标头
    for col, field in enumerate(fields):
        ws.write(0, col, field[1])

    for row, item in enumerate(data):
        for col, field in enumerate(fields):
            ws.write(row + 1, col, item.get(field[0]))

    wb.save(response)
    return response


def import_excel(self, fields):
    file = self.request.FILES.get('file')

    if not file:
        raise ValidationError({'message': '文件不存在'})

    wb = xlrd.open_workbook(file_contents=file.read())
    ws = wb.sheet_by_index(0)

    row_fields = [item[1][0] for item in itertools.product(ws.row_values(0), fields) if item[0] == item[1][1]]
    for row in range(1, ws.nrows):
        data = {item[0]: item[1] for item in zip(row_fields, ws.row_values(row)) if item[1] != ''}
        self.get_serializer(data=data).is_valid(raise_exception=True)
        yield data
