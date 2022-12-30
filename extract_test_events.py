# python3 extract_test_events.py
#
# 

from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag
from bs4 import Comment
from dateutil.parser import parse
import datetime
import re
import os

import location_processing as lp #EJ file

# The goal of this script is to extract events from a page of html 
# where each event has exactly one date and the page contains a 
# minimum of 2 events.  We expect a node to have no more than one event
# date.  We identify the nodes with dates, then we find the highest 
# ancestor for each node that only covers a single date, then we 
# extract all the contents beneath that ancestor node as a single event.

def get_date(a_text):
	#print("ln12 Testing text for date: " + str(a_text))
	newdate = None
	if a_text:
		a_text = a_text.replace('\n', ' ').strip()
		a_text = a_text.replace('&nbsp;', ' ').strip()
		a_text = lp.strip_out_street_address(a_text) # removes components like "123 Main St."
		a_text = a_text.replace('18+', '') # Adult Pickleball (18+)-Recreational Pick-Up Play
		a_text = a_text.replace('2D ', '') # 2D Video Game Design (gr3-5) Wed 1/12
		a_text = a_text.replace('3D ', '') 
		a_text = a_text.replace('Yang 24', 'Yang')
		a_text = a_text.replace('Sun-Style', '') 
		a_text = a_text.replace('501(c)(3)', '') # The YMCA is a 501(c)(3) not-for-profit
		a_text = a_text.replace('5K run', '') 
		#a_text = a_text.replace('a.m.', 'a.m. ') 
		#a_text = a_text.replace('p.m.', 'p.m. ') 
		a_text = re.sub('[0-9]+.{1,15} ([Tt]hings [Tt]o [Dd]o)', r'\1', a_text) # 50 Awesome Things To Do
		a_text = re.sub('[Tt]op [0-9]{1,3} ', ' top ', a_text) # list of the top 10 Chicago area
		a_text = re.sub(' S[0-9] ', ' ', a_text)
		a_text = re.sub('[Aa]ges *[0-9]+-[0-9]+', '', a_text)
		a_text = re.sub('[Aa]ges : *[0-9]+\\.?[0-9]? *- *[0-9]+\\.?[0-9]?', '', a_text) # Ages :  3.5 - 5
		a_text = re.sub('[0-9]+ spaces', '', a_text) # 10 spaces
		a_text = re.sub('Class Size: [0-9]+', '', a_text) # 10 years 
		a_text = re.sub('[Gg]r *[Kk0-9]+-[0-9]+', '', a_text) # Gr k-2
		a_text = re.sub('Internet Explorer [0-9]+', '', a_text)
		a_text = re.sub('\$[0-9]+\.[0-9]+', '', a_text) # $253.00 (price)
		a_text = re.sub('\$[0-9]+', '', a_text) # $253 (price)
		a_text = re.sub(' [0-9]{1,2} hour', ' hour', a_text) #  In this 2 hour workshop
		a_text = re.sub('[0-9]+ day', '', a_text) # 1 day
		a_text = re.sub('[0-9]+ week', '', a_text) # 8 weeks
		a_text = re.sub('[0-9]+ months', '', a_text) # 24 months
		a_text = re.sub('[0-9]+ years', '', a_text) # 10 years
		a_text = re.sub('[0-9]+-[0-9]+ yrs.', '', a_text) # 10 years
		a_text = re.sub('12 noon', '', a_text) 
		a_text = re.sub('COVID-19', '', a_text) 
		a_text = re.sub('within [0-9]+ business days', '', a_text) 
		a_text = re.sub('^ *(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) *$', '', a_text) 
		a_text = re.sub('1st (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)', r'First \1', a_text) 
		a_text = re.sub('^ *Mondays', 'next Monday', a_text) 
		a_text = re.sub('^ *Tuesdays', 'next Tuesday', a_text) 
		a_text = re.sub('^ *Wednesdays', 'next Wednesday', a_text)
		a_text = re.sub('^ *Thursdays', 'next Thursday', a_text) 
		a_text = re.sub('^ *Fridays', 'next Friday', a_text) 
		a_text = re.sub('^ *Saturdays', 'next Saturday', a_text) 
		a_text = re.sub('^ *Sundays', 'next Sunday', a_text)  
		a_text = re.sub('[Aa]ll (January|February|March|April|May|June|July|August|September|October|November|December) [Cc]lasses', 'all classes', a_text)
		
		a_text = re.sub('^ *Mon( [01]{1,2}:[0-9]{2})', r'next Monday\1', a_text) 
		a_text = re.sub('^ *Tues( [01]{1,2}:[0-9]{2})', r'next Tuesday\1', a_text) 
		a_text = re.sub('^ *Wed( [01]{1,2}:[0-9]{2})', r'next Wednesday\1', a_text) 
		a_text = re.sub('^ *Thurs( [01]{1,2}:[0-9]{2})', r'next Thursday\1', a_text) 
		a_text = re.sub('^ *Thur( [01]{1,2}:[0-9]{2})', r'next Thursday\1', a_text) 
		a_text = re.sub('^ *Fri( [01]{1,2}:[0-9]{2})', r'next Friday\1', a_text) 
		a_text = re.sub('^ *Sat( [01]{1,2}:[0-9]{2})', r'next Saturday\1', a_text)
		a_text = re.sub('^ *Sun( [01]{1,2}:[0-9]{2})', r'next Sunday\1', a_text) 
		a_text = re.sub('[0-9]+ Mondays', '', a_text) 
		a_text = re.sub('[0-9]+ Tuesdays', '', a_text) 
		a_text = re.sub('[0-9]+ Wednesdays', '', a_text)
		a_text = re.sub('[0-9]+ Thursdays', '', a_text) 
		a_text = re.sub('[0-9]+ Fridays', '', a_text) 
		a_text = re.sub('[0-9]+ Saturdays', '', a_text) 
		a_text = re.sub('[0-9]+ Sundays', '', a_text) 
		a_text = re.sub('^ *of [0-9]+ *$', '', a_text) # because "page 1" is separate html node from "of 24"
		a_text = re.sub('[Pp]age [0-9]+ of [0-9]+', '', a_text) 
		a_text = re.sub('[0-9]+-[0-9]+ of [0-9]+', '', a_text) # 1-20 of 467
		a_text = re.sub('[Pp]rev +[0-9]+ [0-9]+ [0-9]+ . [Nn]ext', '', a_text)  
		a_text = re.sub('^[0-9]+$', '', a_text) # '100' (page numbers)
		a_text = re.sub('([A-Za-z]+)[0-9]+([A-Za-z])', r'\1\2', a_text)
		a_text = re.sub('[0-9](st|nd|rd|th) [Aa]nnual', 'annual', a_text)
		
	if a_text and "square" in a_text and "row" in a_text and "of grid" in a_text:
		return None
	if a_text and "![CDATA" in a_text:
		return None
	if a_text and "@import " in a_text:
		return None
	if a_text and "google-analytics" in a_text:
		return None
	if a_text and "window.dataLayer" in a_text:
		return None
	if a_text and "jQuery" in a_text:
		return None
	if a_text and "xml version" in a_text:
		return None
	if a_text and ".cls" in a_text:
		return None
	if a_text and "Adobe Illustrator" in a_text:
		return None
	if a_text and "scriptPath" in a_text:
		return None
	if a_text and "schema.org" in a_text:
		return None
	if a_text and " cursor:" in a_text:
		return None
	if a_text and "font-size:" in a_text:
		return None
	if a_text and "(function *" in a_text:
		return None
	if a_text and "function(" in a_text:
		return None
	if a_text and " var " in a_text:
		return None
	if a_text and "border-width:" in a_text:
		return None
	if a_text and "{display:" in a_text:
		return None
	if a_text and "</div>" in a_text:
		return None
	if a_text and "<link " in a_text:
		return None
	if a_text and "@media" in a_text:
		return None
	if a_text and "plugin" in a_text:
		return None
	if a_text and "raindate" in a_text.lower():
		return None
	if a_text and "register" in a_text.lower(): # register 6/18/22
		return None
	if a_text and a_text.isdigit(): # '10'
		return None
	if a_text and a_text.replace(' ', '') and a_text.replace(' ', '').isdigit(): # ' 10 '
		return None
	if a_text and a_text.replace(' ', '').replace('y', '').replace('m', '') and a_text.replace(' ', '').replace('y', '').replace('m', '').isdigit(): # '11y 10m'
		return None
	if a_text and a_text.lower().replace('level', '').replace(' ', '').isdigit(): # 'Level 3'
		return None
	if a_text and a_text.lower().replace('-', '').replace('–', '').replace('.', '').replace(':', '').replace(' ', '').replace('a', '').replace('p', '').replace('m', '').replace('noon', '').replace('or', '').isdigit(): # 8 – 9:30 a.m.
		return None
	if a_text and re.sub('(jan|feb|mar|apr|may|jun|july|aug|sep|oct|nov|dec)', '', a_text.lower()).strip() == "":
		return None
#	if a_text:
#		print("103 a_text: " + a_text)
	
	try:
		newdate = parse(a_text, fuzzy=True)
	except:
		newdate = None
	if not newdate:
		try:
			splittext = a_text.split(" ")
			for token in splittext:
				if "/" in token and token.replace('/', '').replace(' ', '').replace(',', '').isdigit():
					newdate = parse(token, fuzzy=True)
					if newdate:
						break
		except:
			newdate = None
	if not newdate:
		try:
			newdate = parse(a_text.split("-")[0], fuzzy=True)
		except:
			newdate = None
	if not newdate:
		try:
			newdate = parse(a_text.split("–")[0], fuzzy=True)
		except:
			newdate = None
	if not newdate:
		try:
			newdate = parse(a_text.split(",")[0], fuzzy=True) # Do commas after dashes (above) "November 10, 2021 - September 28, 2022"
		except:
			newdate = None
	if newdate: #i.e., not None
		today = newdate.today()
		#print(today)
		# Parse defaults to today's date and time.  It means we're missing too much critical information to determine that there's an extractable event.
		if newdate.month == today.month and newdate.day == today.day:
			#print("WARNING: 'Date' is today! Might not be a real date. Year only?? " + a_text)
			#newdate = None
			newdate = special_screen_for_todays_date(a_text)
	if newdate:
		print("ln96 Date Found: " + str(newdate) + " String: " + a_text)
	return newdate
	
	
def special_screen_for_todays_date(a_text):
	a_text = a_text.replace('2023', '').replace('2022', '').replace('2021', '').replace('2020', '').replace('2019', '')
	
	if a_text and (" ave" in a_text.lower() or " rd" in a_text.lower() or " st" in a_text.lower() or " way" in a_text.lower()):
		return None
	if a_text and (" avenue" in a_text.lower() or " road" in a_text.lower() or " street" in a_text.lower() or " lane" in a_text.lower()):
		return None
	if a_text and ("location" in a_text.lower() or "call " in a_text.lower().replace(":", "") ):
		return None
	
	a_text = re.sub('[0-9]{3,}', '', a_text) #'1414 N Ashland'
	
	try:
		newdate = parse(a_text, fuzzy=True)
	except:
		newdate = None
	return newdate
	
def clean_spacing(text):
	while "  " in text:
		text = text.replace('  ', ' ').replace('\n', ' ')
	return text
	
# from: https://stackoverflow.com/questions/54265391/find-all-end-nodes-that-contain-text-using-beautifulsoup4
def is_end_node_with_only_text(tag):
	# Good but misses the text + tag nodes
	if len(tag.find_all(text=False)) == 0:
		return True
	return False
	
def is_middle_node_with_direct_text(tag):
	# Good, prints the remaining text (but misses the tags of that text)
	if len(tag.find_all(text=False)) > 0:
		for child in tag.contents: #some contents is text, some content is child nodes
			if not isinstance(child, Tag) and len(child.strip()) > 0: # if it's not a child node (must be text). Also, get rid of lots of /n
				return True
	return False



# The goal is to find the title of the event, which is usually the node with the 
# shortest text that includes one of these keywords.  Otherwise, we'll just use
# the first node.
def get_improved_title(top_event_node):
	keywords = ['basketball', 'soccer', 'swim', 'swimming', 'dance', 'hip-hop', 'yoga', 'walk', 'fun', 'gala', 'healthy', 'concerts', 'market', 'movie', 'play', 'volleyball', 'tennis', 'archery', 'cardio', 'adventures', 'chess', 'robotics', 'science', 'adventures', 'inventors', 'vacation', 'ceramics', 'clay', 'wheel', 'drawing', 'painting', 'glass', ' art ', ' arts ', 'mixed media', 'cartoons', 'animation', 'animations', 'woodworking', 'tool safety', 'jewelry', 'mosaic', 'sew', 'sewing', 'cooking', 'walk', 'scark', 'bonsai', 'meditation', 'tai chi', 'homeowners', 'music', 'rock', 'classical', 'jazz', 'theater', 'musical', 'party', 'easter', 'independence day', 'fireworks', 'egg', 'apple', 'pumpkin', 'maze', 'haunted', 'holi', 'halloween', 'thanksgiving', 'christmas', 'sledding', 'winnie', 'bunny', 'rabbit', 'mickey', 'peppa', 'robots']
	previous_shortest = None
	previous_shortest_length = 1000
	for subevent_node in top_event_node.find_all():
		for keyword in keywords:
			if keyword in subevent_node.get_text().lower() and len(subevent_node.get_text()) < previous_shortest_length:
				previous_shortest = subevent_node
				previous_shortest_length = len(subevent_node.get_text())
	title = None
	if previous_shortest:
		title = previous_shortest.get_text()[0:90] #trucated for readability
	else:
		for subevent_node in top_event_node.find_all():
			if subevent_node.get_text() and len(subevent_node.get_text()) > 0:
				title = subevent_node.get_text()[0:90]
				break
	#print("237 Title: " + clean_spacing(title.replace('\n', ' ')))
	return title
	
def get_cost(a_text):
	cost_list = re.findall('\$[0-9]+\.?[0-9]{0,2}', a_text)
	return cost_list
	
def get_grades(a_text):
	# Note: findall has a special property where it returns groups () if there are any.
	# So, you need to use non-returning groups like (?: ...) instead of just ().
	grade_list = re.findall('[Gg]r(?:ade|ades)? ?[0-9Kk]{1,2} ?(?:\-|to)? ?[0-9Kk]{0,2}', a_text)
	grade_list_more = re.findall('(?:1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th) ?(?:\-|to)? ?(?:1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th)? ?[Gg]rade', a_text)
	if grade_list_more and grade_list: #if not None
		grade_list.extend(grade_list_more)
	# need 1st-2nd Grade too
	return grade_list
	
def get_ages(a_text):
	# Trying to find: Ages : 0 - 1, Ages : 3 - 4.5, Ages : 0.5 - 4, (Ages 8-12), (ages5-7), Age At least 8 but less than 12y 10m, At least 4 but less than 7y 11m, 
	ages = re.findall('[Aa]ges?\:? ?[0-9\.]{1,2} ?(?:\-|to)? ?[0-9\.]{0,2}', a_text)
	if '18+' in a_text:
		ages.append('18+')
	return ages
	
def get_kid_references(a_text):
	#trying to catch: Kids, age group, outrageous family fun party, family music, their children, parents, families, family friendly, your little ones, children's curiosity, children, the whole family, your toddler, toddler, 
	a_text = a_text.lower().replace('-', ' ')
	kid_keywords = ['kids', 'kid', 'kid friendly', 'age groups', 'age group', 'family fun party', 'family fun', 'family music', 'children', 'parents', 'families', 'family friendly', 'your little one', 'little ones', 'the whole family', 'your toddler', 'toddler', 'fun for all ages', 'mixed ages', 'preschool', 'preschooler', 'preschoolers', 'homeschool', ]
	found_keywords = []
	for keyword in kid_keywords:
		if keyword in a_text:
			found_keywords.append(keyword)
	ages_phrase = re.findall('ages [0-9]{1,2}\+? (?:and up)?', a_text)
	if ages_phrase and found_keywords:
		found_keywords.extend(ages_phrase)
	return found_keywords

def are_sibling_nodes(common_node_list):
	if len(common_node_list) < 2:
		return True
	are_siblings = True
	i = 0
	while i < len(common_node_list):
		j = i + 1
		while j < len(common_node_list):
			node_i = common_node_list[i]
			node_j = common_node_list[j]
			if node_i.parent != node_j.parent:
				are_siblings = False
			j +=1
		i +=1
	return are_siblings
			


def get_events_in_a_file(filename, a_event_location, tsv_file):

	with open(filename) as fp:
	    soup = BeautifulSoup(fp, 'html.parser')

	end_node_with_only_text = soup.find_all(is_end_node_with_only_text)
	middle_node_with_direct_text = soup.find_all(is_middle_node_with_direct_text)
	# I can't figure out how to detect and remove comments without other consequences.
	#comments = soup.find_all(string=lambda text: isinstance(text, Comment))


	date_nodes = [] # list of tuple (node, datetime)
	
	print('\n\n\n' + filename + ' events:')

	# Get nodes that only have child text
	for node in end_node_with_only_text:
		#print("l72 " + node.string)
		maybe_date = get_date(node.string)
		if maybe_date: #i.e., if the date isn't None
			#if node.parent.parent:
			#	print("199 Date Found: " + str(maybe_date) + " String: " + node.string + "  " + node.parent.parent.get_text())
			date_nodes.append((node, maybe_date))

	# Get nodes that have both child nodes and child text
	for node in middle_node_with_direct_text:
		for child in node.contents:
			if not isinstance(child, Tag):
				#print("l77  " + child.string.strip())
				maybe_date = get_date(child.string.strip())
				if maybe_date: #i.e., if the date isn't None
					#if node.parent:
					#	print("209 Date Found: " + str(maybe_date) + " String: " + child.string.strip() + "  " + node.parent.get_text())
					date_nodes.append((node, maybe_date))

	event_counter = 1
	for d in range(len(date_nodes)):
		date_node = date_nodes[d][0]
		ancestor = date_node.parent
		old_ancestor = date_node
		date_nodes_only = []
		for n in date_nodes:
			date_nodes_only.append(n[0])
		
		common_node_list = list(set(list(ancestor.descendants)).intersection(set(date_nodes_only)))
		while ancestor and (len(common_node_list) <= 1 or are_sibling_nodes(common_node_list)):
		
			old_ancestor = ancestor
			ancestor = ancestor.parent
			common_node_list = list(set(list(ancestor.descendants)).intersection(set(date_nodes_only)))
		# This *should* be the highest node that covers only one event.
		top_event_node = old_ancestor 
		
		
		if len(top_event_node.get_text().strip()) > len(date_node.get_text().strip()) and len(list(top_event_node.descendants)) < 200:
			print("\n\n-------------EVENT #" + str(event_counter) + " ------------------")
			event_counter +=1
			title = get_improved_title(top_event_node)
			print("TITLE: " + clean_spacing(title))
			tsv_line = ""
			event_contents = []
			for subevent_node in top_event_node.find_all():
				an_event_info = subevent_node.get_text().replace('\n', ' ').strip()
				if len(an_event_info) > 0 and an_event_info not in event_contents:
					event_contents.append(an_event_info)
					#print("INFO: " + clean_spacing(an_event_info.replace('\n', ' ')))
					
			
			tsv_line = title # truncated for readability
			tsv_line = tsv_line + "\t" + date_nodes[d][1].strftime('%m-%d-%Y')
			tsv_line = tsv_line + "\t" + date_node.get_text().strip()[:100] #truncated
			tsv_line = tsv_line + "\t" + a_event_location.strip()
		
			print("DATE: " + date_nodes[d][1].strftime('%m-%d-%Y'))
			
			costs = get_cost(top_event_node.get_text().replace('\n', ' '))
			if len(costs) > 0:
				print('COST(S): ' + ','.join(costs))
				
			grades = get_grades(top_event_node.get_text().replace('\n', ' '))
			if len(grades) > 0:
				print('GRADE(S): ' + ','.join(grades))
				
			ages = get_ages(top_event_node.get_text().replace('\n', ' '))
			if len(ages) > 0:
				print('AGES: ' + ','.join(ages))
				
			kid_keywords = get_kid_references(top_event_node.get_text().replace('\n', ' '))
			if len(kid_keywords) > 0:
				print('KID WORDS: ' + ', '.join(kid_keywords))
				
			
			links = []
			for link in top_event_node.find_all('a'):
				if not 'javascript:void(0);' in link.get('href'):
					links.append(link.get('href'))
					print("LINK: " + link.get('href')[:50] + ' [...]')
			if len(links) > 0:
				tsv_line = tsv_line + "\t" + links[0]
			else:
				tsv_line = tsv_line + "\t"
			imgs = []
			for img in top_event_node.find_all('img'):
				if 'src' in img.attrs.keys():
					imgs.append(img['src'])
					print("IMG: " + img['src'])
				else:
					imgs.append('IMG: Unknown Source')
					print('IMG: Unknown Source')
			if len(imgs) > 0:
				tsv_line = tsv_line + "\t" + imgs[0]
			else:
				tsv_line = tsv_line + "\t"
			
			tsv_file.write(clean_spacing(tsv_line.replace('\n', '')) + "\n")
			print('ALLTEXT: ' + clean_spacing(top_event_node.get_text().replace('\n', ' ')))


# Get proper directories:
path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))


datalist_file = open(parent_path + "/Data/SampleURLLocations/" + 'datalist.tsv', 'r')

# Create a new tsv file of events for Ross
tsv_file = open(parent_path + "/Data/ExtractedEvents/" + "all_events.tsv", 'w')
tsv_file.write("TITLE (first text node)\tDATE\tDATETEXT\tLOCATION\tFIRST_LINK\tFIRST_IMG\n")
	
line = datalist_file.readline()
while line != "":
	if line[0] != '#' and len(line.split('\t')) == 3: # for comments
		a_data_file, a_event_location = line.split('\t')[0:2] #data file is the filename, event location is like 'Boston MA'
		a_data_file = parent_path + "/Data/SampleHTML/" + a_data_file
		get_events_in_a_file(a_data_file, a_event_location, tsv_file)
	line = datalist_file.readline()
datalist_file.close()
tsv_file.close()

	



# Test code: this shows our date function is working.
#my_date = parse("Central design committee session Tuesday 10/22 6:30 pm", fuzzy=True)
#my_date = parse("next Monday 10am", fuzzy=True)

#my_date = get_date("next Monday 10am")
#print(my_date)

#print(lp.strip_out_street_address("John lives at 123 Elm St. in Poughkeepsie NY"))













