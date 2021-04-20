import dbconnector.dbconnector as dbcon
from openpyxl import Workbook
from openpyxl.styles import PatternFill
import sys
import re
import io


class Creator():
	user_list = []
	drone_list = []

	user_id = {}
	drone_id = {}

	def __init__(self, db):
		self.db = db
		for user in db.get_users():
			self.user_list.append(user)
		
		for drone in db.get_drones():
			self.drone_list.append(drone[1])

	def createFile(self):
		wb = Workbook()

		ws = wb.active
		for drone in self.drone_list:
	
			ws.title = drone


			ws.cell(row=1, column=1, value = "MAPS")
			ws.cell(row=1, column=2, value = "Track")
			ws.cell(row=1, column=3, value = "Race")
			ws.cell(row=1, column=4, value = "Level")

			col = 5
			for user in self.user_list:
				ws.cell(row=1, column=col, value = user[1])
				print(user[2][1:], file=sys.stderr)
				ws.cell(row=1, column=col).fill = PatternFill(start_color=user[2][1:], end_color=user[2][1:], fill_type = "solid")
				
				col += 1

			if self.drone_list[-1] != drone:
				ws = wb.create_sheet()
		return wb