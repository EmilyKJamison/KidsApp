# python3 location_processing.py
#
# This is a set of methods to process text to find and parse location information.

import usaddress

def pre_clean(a_text):
	a_text.replace('2022 ', ' ')
	a_text.replace('2023 ', ' ')
	a_text.replace(' 2022', ' ')
	a_text.replace(' 2023', ' ')
	return a_text

def get_street_number(a_text):
	parsed_address = usaddress.parse(a_text)
	for component in parsed_address:
		if component[1] == 'AddressNumber':
			return component[0]
	return None
	
def post_clean(address_string):
	address_string = address_string.replace('10m Quick View', '')
	address_string = address_string.replace('100 Quick View', '')
	return address_string
	
def get_entire_detected_address(a_text):
	a_text = pre_clean(a_text)
	parsed_address = usaddress.parse(a_text)
	print(parsed_address)
	address_string = ''
	for component in parsed_address:
		if component[1] == 'AddressNumber':
			address_string = component[0]
		if component[1] == 'StreetName':
			address_string = address_string + ' ' + component[0]
		if component[1] == 'StreetNamePostType':
			address_string = address_string + ' ' + component[0]
		if component[1] == 'OccupancyType':
			address_string = address_string + ' ' + component[0]
		if component[1] == 'OccupancyIdentifier':
			address_string = address_string + ' ' + component[0]
		if component[1] == 'PlaceName':
			address_string = address_string + ' ' + component[0]
		if component[1] == 'StateName':
			address_string = address_string + ' ' + component[0]
		if component[1] == 'ZipCode':
			address_string = address_string + ' ' + component[0]
	address_string = post_clean(address_string)
	return address_string
	
def strip_out_street_address(a_text):
	parsed_address = usaddress.parse(a_text)
	stripped_text = a_text
	for component in parsed_address:
		if component[1] == 'AddressNumber':
			stripped_text = ''.join(stripped_text.split(component[0], 1))
		if component[1] == 'StreetName':
			stripped_text = ''.join(stripped_text.split(component[0], 1))
		if component[1] == 'StreetNamePostType':
			stripped_text = ''.join(stripped_text.split(component[0], 1))
		if component[1] == 'ZipCode':
			stripped_text = ''.join(stripped_text.rsplit(component[0], 1)) #rsplit from right (backwards)
	return stripped_text
	
	
#print(get_entire_detected_address("Fun4All Programming"))
print(strip_out_street_address("John lives at 123 Elm St. in Poughkeepsie NY"))



















