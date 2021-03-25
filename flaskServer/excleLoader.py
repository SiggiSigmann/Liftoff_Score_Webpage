import dbconnector.dbconnector as dbcon
from openpyxl import load_workbook
import sys


class ExcelLoader():
	user_list = []
	drone_list = []

	excluded_headder=["Map","Track","Race","Level",None]

	user_id = {}
	drone_id = {}

	

	def __init__(self, db):
		self.db = db
		for user in db.get_users():
			self.user_list.append(user[1])
		
		for drone in db.get_drones():
			self.drone_list.append(drone[1])


	def loadFile(self, filename):
		workbook = load_workbook(filename=filename)

		for dronename in workbook.sheetnames:
			self._make_shure_drone_exists(dronename)
			sheet = workbook[dronename]
			firstrow = sheet[1]

			username_idx = {}
			index = 0
			user_count = 0
			
			for cell in firstrow:
				if not cell.value in self.excluded_headder:
					user = cell.value.rstrip()
					color = "#"+cell.fill.start_color.index[2:].rstrip()
					self._make_shure_user_exists(user, color)
					username_idx[index] = user
					user_count += 1
				index += 1

			max_idx = user_count+4
			
			self._load_user_id()
			self._load_drone_id()
				
			
			skip_first = 0
			
			for row in sheet:
				if skip_first == 0:
					skip_first = 1
					continue


				if row[0].value != None:
					map_name = row[0].value.rstrip()
					track_name = row[1].value.rstrip()
					#dronename

					index = 4
					for user in row[4:]:
						if index < max_idx:
							if user.value != None:
								time = user.value.rstrip()
								username = username_idx[index]

								ids = self.db.get_map_track_id(map_name, track_name)
								if len(ids) < 1:
									continue
								print(ids, file=sys.stderr)

								print(str(self.drone_id[dronename]) + " " + str(ids[0]) +" "+ str(ids[1])+" "+str(self.user_id[username])+ " "+time, file=sys.stderr)
								self.db.add_new_result(ids[0], ids[1], str(self.user_id[username]), self.drone_id[dronename], time)
						index += 1

		#self.db.add_new_result(mapid, trackid, userid, droneid, resulttimestamp):
		#return


	def _make_shure_user_exists(self, username, color):
		if not username in self.user_list:
			print("user not exis: " + username + " ("+color+")", file=sys.stderr)
			self.db.add_new_user(username,color)
			self.user_list.append(username)

	def _make_shure_drone_exists(self, dronename):
		if not dronename in self.drone_list:
			print("drone not exis: " + dronename, file=sys.stderr)
			self.db.add_new_drone(dronename)
			self.drone_list.append(dronename)

	def _load_user_id(self):
		users =  self.db.get_users()
		for user in users:
			self.user_id[user[1]] = user[0]

	def _load_drone_id(self):
		drones = self.db.get_drones()
		for drone in drones:
			self.drone_id[drone[1]] = drone[0]
		
			


			

		