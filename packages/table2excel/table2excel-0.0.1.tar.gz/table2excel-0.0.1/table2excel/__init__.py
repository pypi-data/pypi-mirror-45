# coding=utf8

import xlwt
import StringIO


def _utf8(s):
    if isinstance(s, unicode):
        return s.encode('utf8')
    return s

CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
CONTENT_DISPOSITION = "attachment; filename=sheet.xlsx"

def dumpExcel(name, table):
    book = xlwt.Workbook()
    sheet = book.add_sheet(_utf8(name))
    row_count = len(table)
    col_count = max([len(row) for row in table])

    f = StringIO.StringIO()

    for _r_idx in range(row_count):
        for _c_idx in range(col_count):
            row = table[_r_idx]
            col = "" if len(row) < (_c_idx+1) else row[_c_idx]
            sheet.write(_r_idx, _c_idx, col)
    book.save(f)
    f.seek(0)
    return f.read()
