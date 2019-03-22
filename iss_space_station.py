# Created by: Pycharm
# Auther: Mohamed Ismail
# Date: 3/9/2019
# Time: 9:11 PM

import sys
import json
import datetime
from urllib2 import urlopen


class iss_space_station:
	iss_location_url = 'http://api.open-notify.org/iss-now.json'
	iss_astors_url = 'http://api.open-notify.org/astros.json'
	iss_passing_url = "http://api.open-notify.org/iss-pass.json?lat={0}&lon={1}"

	def __init__(self):
		print("ISS Coding Chanllenge")

	# read command line arguments --loc, --people, --pass
	def read_cmd_args(self):
		cmd_args = sys.argv[1:]
		for currentArgument in cmd_args:

			if currentArgument in ("-l", "--loc"):

				if len(cmd_args) == 1:
					self.iss_current_location()

				else:
					print("Found more than 1 argument. Please try again.")
					break

			elif currentArgument in ("-pp", "--people"):

				if len(cmd_args) == 1:
					self.iss_people_details()

				else:
					print("Found more than 1 argument. Please try again.")
					break

			elif currentArgument in ("-p", "--pass"):

				if len(cmd_args) == 3:
					self.iss_passing_details(lat_cord=cmd_args[1], long_cord=cmd_args[2])
					break #necessary to stop parsing the lat and long as additional arguments.

				elif len(cmd_args) > 3:
					print("Found more than 3 argument. Please try again.")
					break

				else:
					print("Enter LAT and LONG information.")
					break

			elif currentArgument in ("-h", "--help"):

				if len(cmd_args) == 1:
					self.iss_help()

				else:
					print("Found more than 1 argument. Please try again.")
					break

			else:
				print ("Argument not recognized!")
				self.iss_help()
				break

	def iss_help(self):
		print("Please use the following switches for desired output.")
		print("1. Use -p or --pass switch to print the passing details of the ISS for a given location")
		print("2. Use -l or --loc switch to print the current location of the ISS space station")
		print("3. Use -pp or --people switch to print the details of those people that are currently for each craft in space.")

	# print the current location of the ISS
	def iss_current_location(self):
		load_locations = urlopen(self.iss_location_url)
		query_location = json.loads(load_locations.read()) #Decoding Python file object
		timestamp = datetime.datetime.fromtimestamp(query_location['timestamp'])
		# date = timestamp.strftime('%Y-%m-%d')
		time = timestamp.strftime('%H:%M:%S')
		latitude = query_location['iss_position']['latitude']
		longitude = query_location['iss_position']['longitude']
		print("The ISS current location at {time} is {LAT}, {LONG}.".format(time=time, LAT=latitude, LONG=longitude))

	# print the passing details of the ISS for a given location
	def iss_passing_details(self, lat_cord, long_cord):
		# latitude = -50.7487
		# longitude = 149.5982

		pass_url = self.iss_passing_url.format(lat_cord, long_cord)
		request_pass_info = urlopen(pass_url)
		response_pass = json.loads(request_pass_info.read())

		pass_lat = response_pass['request']['latitude']
		pass_long = response_pass['request']['longitude']
		pass_date = datetime.datetime.fromtimestamp(response_pass['response'][0]['risetime'])
		pass_time = pass_date.strftime('%H:%M:%S') #returns a string representing date and time using date, time or datetime object.
		pass_duration = response_pass['response'][0]['duration']

		print("The ISS will be overhead {0} at {1}, {2} for {3} seconds."
			  .format(pass_lat, pass_long, pass_time, pass_duration))

	# print the details of those people that are currently in space
	def iss_people_details(self):
		query_location = urlopen(self.iss_astors_url)
		location_list = json.loads(query_location.read())

		print ("There are {0} people aboard the {1}. They are:") \
			.format(location_list['number'], location_list['people'][0]['craft'])

		for i in range(location_list['number']):
			print(location_list['people'][i]['name'])


# Main method
if __name__ == '__main__':
	iss_space_station().read_cmd_args()
