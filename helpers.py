import shutil, os, sys, re, json

# Create a list of regex for classification
REGEX_TELLRAW = [
	re.compile(r'tell\((.*)\)=" (.*) "'), 
	re.compile(r'tellraw\((.*)\)=" (.*) "')
]

REGEX_TIME = [
	re.compile(r't=(.*)'), 
	re.compile(r'time=(.*)'), 
	re.compile(r'end')
]

REGEX_TITLE = [
	re.compile(r'title\((.*)\)=" (.*) "'), 
]

REGEX_SUBTITLE = [
	re.compile(r'sub\((.*)\)=" (.*) "'),
	re.compile(r'subtitle\((.*)\)=" (.*) "')
]

REGEX_COMMAND = [
	re.compile(r'run=(.*)'), 
]

REGEX_CREATE = [
	re.compile(r'create=(.*)')
]

REGEX_COMMENT = [
	re.compile(r'\s*--(.*)--\s*')
]

REGEX_COLOR = [
	re.compile(r'c=(.*)'),
	re.compile(r'color=(.*)')
]

STR_FONT_BOLD = [
	"b",
	"bold"
]

STR_FONT_ITALIC = [
	"i",
	"italic"
]

STR_FONT_UNDERLINED = [
	"u",
	"underlined"
]

STR_FONT_STRIKETHROUGH = [
	"s",
	"strikethrough"
]

STR_FONT_OBFUSCATED = [
	"o",
	"obfuscated"
]

REGEX_TITLE_IN = [
	re.compile(r'in=(.*)')
]

REGEX_TITLE_OUT = [
	re.compile(r'out=(.*)')
]

REGEX_TITLE_DUR = [
	re.compile(r'dur=(.*)')
]

REGEX_CLICK = [
	re.compile(r'click\((.*)=(.*)\)')
]

REGEX_HOVER = [
	re.compile(r'" (.*) ", \((.*)\)')
]


# Create folder, exits if REPLACE = "no" and folder exists
def create_folder(namespace, REPLACE):
	path = namespace + "/functions"
	if os.path.exists(path):
		if REPLACE == "yes":
			shutil.rmtree(path)
		else:
			sys.exit(f"Error: \"{namespace}\" folder exists")
						
	# Create dir
	os.makedirs(path)



# Separate tag, exits when unknown tag appear and some tags are duplicate
def make_command_dict(functions, line_number):
	dict = {}

	for function in functions:
		# Check time and whether duplicate or not
		if any(regex.match(function) for regex in REGEX_TIME):
			if "time" not in dict:
				# Directly import schedule command
				if function == "end":
					dict["time"] = ""
				else:
					for regex in REGEX_TIME:
						match_object = regex.match(function)
						if match_object:
							dict["time"] = match_object.group(1)

			else:
				sys.exit(f"Error: There are multiple \"time\" / \"end\" tag in line {line_number}")

		# Check title tag and whether duplicate or not
		elif any(regex.match(function) for regex in REGEX_TITLE):
			# Directly import title command
			if "title" not in dict:
				for regex in REGEX_TITLE:
					match_object = regex.match(function)
					if match_object:
						# Get tag_dict
						tag_dict = {}

						tag_dict["text"] = match_object.group(2)
						optional_arg = match_object.group(1)

						tag_dict = add_attribute(tag_dict, optional_arg, line_number)

						# Make title timing command
						try:
							time_in = int(tag_dict["in"])
						except:
							sys.exit(f"Error: Fade in time is not integer / does not exist in line {line_number}")
						
						try:
							time_out = int(tag_dict["out"])
						except:
							sys.exit(f"Error: Fade out time is not integer / does not exist in line {line_number}")
						
						try:
							time_dur = int(tag_dict["dur"])
						except:
							sys.exit(f"Error: Duration time is not integer / does not exist in line {line_number}")
						
						command = f"title @a times {time_in} {time_dur} {time_out}"
						dict["title"] = [command]

						# Make title command
						del tag_dict["in"]
						del tag_dict["out"]
						del tag_dict["dur"]

						Json = json.dumps(tag_dict)

						command = f"title @a title {Json}"
						dict["title"].append(command)

			else:
				sys.exit(f"Error: There are multiple \"title\" tag in line {line_number}")
				
		# Check subtitle tag and whether duplicate or not
		elif any(regex.match(function) for regex in REGEX_SUBTITLE):
			# Directly import subtitle command			
			if "subtitle" not in dict:
				for regex in REGEX_SUBTITLE:
					match_object = regex.match(function)
					if match_object:
						tag_dict = {}

						tag_dict["text"] = match_object.group(2)
						optional_arg = match_object.group(1)

						tag_dict = add_attribute(tag_dict, optional_arg, line_number)
						Json = json.dumps(tag_dict)
						command = f"title @a subtitle {Json}"

						dict["subtitle"] = [command]

			else:
				sys.exit(f"Error: There are multiple \"subtitle\" tag in line {line_number}")
				
		# Check command tag
		elif any(regex.match(function) for regex in REGEX_COMMAND):
			# Directly import command
			for regex in REGEX_COMMAND:
				match_object = regex.match(function)
				if match_object:
					if "command" not in dict:
						dict["command"] = [match_object.group(1)]
					else:
						dict["command"].append(match_object.group(1))
				
		# Check create tag and whether duplicate or not
		elif any(regex.match(function) for regex in REGEX_CREATE):
			# Directly import new file name
			if "create" not in dict:
				for regex in REGEX_CREATE:
					match_object = regex.match(function)
					if match_object:
						dict["create"] = match_object.group(1).lower()

			else:
				sys.exit(f"Error: There are multiple \"create\" tag in line {line_number}")

		# Ignore comment, remaining is tellraw
		elif not any(regex.match(function) for regex in REGEX_COMMENT):
			if "tellraw" not in dict:
				dict["tellraw"] = [function]
			else:
				dict["tellraw"].append(function)
	
	# Adding time key if time key not exists
	if "time" not in dict:
		dict["time"] = "4s"

	return dict


# Function that add all attributed to tag
def add_attribute(unfinished_tag, optional_arg, line_number):
	args = re.split(r'\s*,\s*', optional_arg)
	for arg in args:
		# Add color
		if any(regex.match(arg) for regex in REGEX_COLOR):
			for regex in REGEX_COLOR:
				match_object = regex.match(arg)
				if match_object:
					unfinished_tag["color"] = match_object.group(1)
		
		# Add bold
		elif any(arg == str for str in STR_FONT_BOLD):
			unfinished_tag["bold"] = "true"
		
		# Add italic
		elif any(arg == str for str in STR_FONT_ITALIC):
			unfinished_tag["italic"] = "true"
		
		# Add underlined
		elif any(arg == str for str in STR_FONT_UNDERLINED):
			unfinished_tag["underlined"] = "true"
		
		# Add strikethrough
		elif any(arg == str for str in STR_FONT_STRIKETHROUGH):
			unfinished_tag["strikethrough"] = "true"
		
		# Add obfuscated
		elif any(arg == str for str in STR_FONT_OBFUSCATED):
			unfinished_tag["obfuscated"] = "true"
		
		# Add fade in time
		elif any(regex.match(arg) for regex in REGEX_TITLE_IN):
			for regex in REGEX_TITLE_IN:
				match_object = regex.match(arg)
				if match_object:
					unfinished_tag["in"] = match_object.group(1)
		
		# Add fade out time
		elif any(regex.match(arg) for regex in REGEX_TITLE_OUT):
			for regex in REGEX_TITLE_OUT:
				match_object = regex.match(arg)
				if match_object:
					unfinished_tag["out"] = match_object.group(1)

		# Add duration time
		elif any(regex.match(arg) for regex in REGEX_TITLE_DUR):
			for regex in REGEX_TITLE_DUR:
				match_object = regex.match(arg)
				if match_object:
					unfinished_tag["dur"] = match_object.group(1)

		# Add Clickevent
		elif any(regex.match(arg) for regex in REGEX_CLICK):
			for regex in REGEX_CLICK:
				match_object = regex.match(arg)
				if match_object:
					event_dict = {}
					# Find what action
					if match_object.group(1).strip() == "open":
						event_dict["action"] = "open_url"
					
					elif match_object.group(1).strip() == "run":
						event_dict["action"] = "run_command"
					
					elif match_object.group(1).strip() == "suggest":
						event_dict["action"] = "suggest_command"
					
					elif match_object.group(1).strip() == "copy":
						event_dict["action"] = "copy_to_clipboard"

					# Reject unknown text
					else:
						sys.exit(f"Unknown tag in click event in line {line_number}")

					event_dict["value"] = match_object.group(2).strip()
					unfinished_tag["clickEvent"] = event_dict

	return unfinished_tag


# Function that make schedule command
def makeschedule(dict, namespace, next_file_count):
	# Remove empty string
	if dict["time"] == "":
		del dict["time"]
	else:
		command = f"schedule function {namespace}:{next_file_count} {dict['time']} "
		dict["time"] = [command]
	
	return dict

def maketellrawtag(un_process_list, line_number, STYLE):
	# Create a list with a empty string element
	tag = [""]

	for element in un_process_list:
		if any(regex.match(element) for regex in REGEX_TELLRAW):
			for regex in REGEX_TELLRAW:
				match_object = regex.match(element)
				# Check tag exists or not
				if match_object:
					tag_dict = {}
					
					tag_dict["text"] = match_object.group(2)
					optional_arg = match_object.group(1)

					tag_dict = add_attribute(tag_dict, optional_arg, line_number)

					tag.append(tag_dict)
			
		else:
			str_to_separated = "("
			if STYLE:
				for dict in STYLE:
					str_to_separated += f"{dict['text']}|"
				
				str_to_separated = str_to_separated.rstrip("|")
				str_to_separated += ")"

				splitted = re.split(str_to_separated, element)
				for dict in STYLE:
					splitted = [dict if element == dict["text"] else element for element in splitted]
				
				try:
					splitted.remove("")
				except:
					pass

				tag.extend(splitted)
			else:
				tag.append(element)

	return tag


def maketellraw(dict, line_number, list):
	try:
		un_process_list = dict["tellraw"]
	except:
		return dict 
	
	tag = json.dumps(maketellrawtag(un_process_list, line_number, list))
	
	command = f"tellraw @a {tag}"
	dict["tellraw"] = [command]
	return dict
	