#!/usr/bin/env python
# coding=utf-8

import sys
import traceback
from openpyxl import load_workbook
import xlrd

class SimpleExcel:
		def __init__(self):
				self.first_row = []
				self.datas = []

		def open(self, filename, sheet):
				if filename.find('.xls') != -1:
						self.__open_xls(filename, sheet)
				else:
						self.__open_xlsx(filename, sheet)

		def __open_xlsx(self, filename, sheet):
				wb = load_workbook(filename=filename, read_only=True)
				ws = wb[sheet]

				for row in ws.rows:
						row_data = {}
						for cell in row:
								print (cell.value)
								if cell.row == 1:
										self.first_row.append(cell.value)
								else:
										col_name = self.first_row[cell.column - 1]
										row_data[col_name] = cell.value

						if len(row_data) != 0:
								self.datas.append(row_data)

				wb.close()

		def __open_xls(self, filename, sheet):
				bk = xlrd.open_workbook(filename)
				sh = bk.sheet_by_name(sheet)

				for rx in range(sh.nrows):
						row = sh.row(rx)
						row_data = {}
						for cx in range(len(row)):
								val = row[cx].value
								if rx == 0:
										self.first_row.append(val)
								else:
										col_name = self.first_row[cx]
										row_data[col_name] = val

						if len(row_data) != 0:
								self.datas.append(row_data)

				del bk

		def find(self, key, value):
				try:
						self.first_row.index(key)
				except Exception as e:
						print('cant find key ' + key)
						return None

				for dat in self.datas:
						if dat[key] == value:
								return dat

		def rows(self):
				return self.datas


# -------------- main --------------
if __name__ == '__main__':
		try:
				# test
				sx = SimpleExcel()
				sx.open('your.xlsx', 'Sheet1')
				dat = sx.find('KEY', 'IDKEY')

		except Exception as e:
				traceback.print_exc()
				sys.exit(1)
