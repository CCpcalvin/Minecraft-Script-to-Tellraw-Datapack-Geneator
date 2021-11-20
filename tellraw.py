import sys, os, re
from helpers import add_attribute, create_folder, make_command_dict, makeschedule, maketellraw
from helpers import REGEX_COMMENT, REGEX_TELLRAW


# Check usage
if len(sys.argv) != 2 and len(sys.argv) != 1:
	sys.exit("Usage: <program> (optional <input_file_name>)")

# List of global variable
DELIMITER = "\\"
INPUT_FILE = "script.txt"
REPLACE = "no"
DEFAULT_NAMESPACE = "Scene_1"
STYLE = []
CREATED_FOLDERS = []

# Change global variable setting base on command line and config
# Overwrite INPUT_FILE
if len(sys.argv) == 2:
	INPUT_FILE = sys.argv[1]

if os.path.exists("config.txt"):
	with open("config.txt", "r", encoding="utf-8") as config:
		rows = config.readlines()

		for row in rows:
			splitted = re.split(r'(?:,|=)', row)

			# Overwrite DELIMITER
			if splitted[0].strip(" ") == "DELIMITER":
				try:
					DELIMITER = re.search(r'\"(.*?)\"', row).group(1)
				except:
					sys.exit("Usage: DELIMITER = \"<symbol>\"")

			# Overwrite REPLACE
			elif splitted[0].strip(" ") == "REPLACE":
				try:
					string = re.search(r'\"(.*?)\"', row).group(1).lower()
				except:
					sys.exit("Usage: REPLACE = \"<bool>\"")

				if string != "yes" and string != "no":
					sys.exit("Error: REPLACE can only be \"yes\" or \"no\"")
				else:
					REPLACE = string
			
			# Overwrite DEFAULT_NAMESPACE
			elif splitted[0].strip(" ") == "DEFAULT_NAMESPACE":
				try:
					DEFAULT_NAMESPACE = re.search(r'\"(.*?)\"', row).group(1)
				except:
					sys.exit("Usage: DEFAULT_NAMESPACE \"<string>\"")
			
			# Write style
			elif any(regex.match(row) for regex in REGEX_TELLRAW):
				for regex in REGEX_TELLRAW:
					match_object = regex.match(row)
					if match_object:
						tag_dict = {}
						tag_dict["text"] = match_object.group(2)
						optional_arg = match_object.group(1)

						tag_dict = add_attribute(tag_dict, optional_arg, 0)
						STYLE.append(tag_dict)


# Test input_file exists or not
if not os.path.exists(INPUT_FILE):
	sys.exit("Error: Input file does not exist")


def main():
	skip_index = []
	# Read all lines from input file
	with open(INPUT_FILE, "r", encoding="utf-8") as input:
		rows = input.readlines()

		for index in range(len(rows)):
			
			# Skip rows when in Skip_rows
			if index in skip_index:
				continue

			# Skip any line with only whitespace
			if rows[index].isspace():
				continue

			# Skip comment
			if REGEX_COMMENT[0].match(rows[index]):
				continue

			# Split each line to functions
			functions = re.split(f'\s*{DELIMITER}\s*', rows[index])

			# Keep reading next line if cont at the end
			while re.match(r'cont\s*', functions[-1]):
				index += 1

				# Skip any line with only whitespace
				if rows[index].isspace():
					skip_index.append(index)
					continue

				# Skip comment
				if REGEX_COMMENT[0].match(rows[index]):
					skip_index.append(index)
					continue

				# Add functions to list, remove cont
				more_functions = re.split(f'\s*{DELIMITER}\s*', rows[index])
				del functions[-1]
				functions.extend(more_functions)

				# Add current index to skip rows
				skip_index.append(index)
			
			# Cleaning functions list
			# Remove empty string
			if "" in functions:
				functions.remove("")

			# Remove all whitespace from left and right
			for function_index in range(len(functions)):
				functions[function_index] = functions[function_index].strip()

			# Separate tag, exits when unknown tag appear and some tags are duplicate, make command except time
			command_dict = make_command_dict(functions, index + 1)

			# Create new file if "create" tag exists
			if "create" in command_dict:
				namespace = command_dict["create"]
				file_count = 0
				create_folder(namespace, REPLACE)
				del command_dict["create"]
				CREATED_FOLDERS.append(namespace)
			
			# Create default path
			try:
				namespace
			except:
				namespace = DEFAULT_NAMESPACE
				file_count = 0
				create_folder(namespace, REPLACE)
				CREATED_FOLDERS.append(namespace)
			
			# Start writting .mcfunction file
			with open(f"{namespace}/functions/{file_count}.mcfunction", "w") as output:
				# Make schedule command
				command_dict = makeschedule(command_dict, namespace, file_count + 1)

				# Make tellraw command
				command_dict = maketellraw(command_dict, index + 1, STYLE)
				for functions in command_dict.values():
					for function in functions:
						output.write(function + "\n")
			
			file_count += 1
		
		# Create start folder
		create_folder("start", REPLACE)
		for folder in CREATED_FOLDERS:
			with open(f"start/functions/{folder}.mcfunction", "w") as output:
				output.write(f"function {folder}:0")

	# Return success message
	print("Datapack successfully generated!")


# Execute main
main()
