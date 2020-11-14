import csv
import subprocess
import os
import time
import sys

# for debugging, if you want to print to stdout in terminal
VERBOSE = False

PRIORITY_BY_WORDS = {
	"blacklist": 1,
	"black_list": 1,
	"black list": 1,
	"white_list": 2,
	"whitelist": 2,
	"white list": 2,
	"slave": 3,
	"dummy": 5,
	"grandfathered": 6
}

COLUMNS_LIST = [
	"Root_Directory",
	"File_Path",
	"Line_Number",
	"Snippet",
	"Priority",
	"Searched_Word",
	"File_Extension"
]

# -i ignores cAsEs
# -g exclude this file itself
# -n force line numbers to be shown, even with piping
CMD = "rg -i -n -g !wordfinder.py"

def main():
	with open("outfile.csv", "w") as f:
		writer = csv.DictWriter(f, COLUMNS_LIST)
		writer.writeheader()
		process_grep_cmd(writer=writer)

def get_arg_directory():
	if len(sys.argv) == 2:
		passed_dir = sys.argv[1]
		if os.path.isdir(passed_dir):
			return sys.argv[1]
		else:
			raise ValueError('%s  is not a valid directory.', passed_dir)
			exit()
	else:
		return "."

def process_grep_cmd(writer):
	cmd_sequence = CMD.split()
	cmd_sequence.append("placeholder") # not the cleanest solution, but we need arg_dir to be last.
	arg_dir = get_arg_directory()
	cmd_sequence.append(arg_dir)
	for word in PRIORITY_BY_WORDS.keys():
		cmd_sequence[-2] = word # replace the old word, this is O(1), I think
		process = subprocess.Popen(cmd_sequence, stdout=subprocess.PIPE, universal_newlines=True)

		#  wait for the output until the process has actually completed.
		stdout, stderr = process.communicate()

		# this is a bytestring
		write_rg_output(output_bytestring=stdout, searched_word=word, csv_writer=writer, search_path=arg_dir)

def write_rg_output(output_bytestring, searched_word, csv_writer, search_path):
	occurrences = output_bytestring.split("\n")[:-1]
	for occurrence in occurrences:
		if VERBOSE:
			print(occurrence)
		row = parse_occurrence_into_csv_row(occurrence=occurrence, searched_word=searched_word, search_path=search_path)
		csv_writer.writerow(row)

def parse_occurrence_into_csv_row(occurrence, searched_word, search_path):
	occurence_split_by_colons = occurrence.split(":")
	file_path = get_file_path(occurence_split_by_colons=occurence_split_by_colons)
	line_number = get_line_number(occurence_split_by_colons=occurence_split_by_colons)
	code_snippet = get_code_snippet(occurence_split_by_colons=occurence_split_by_colons)
	file_ext = get_file_extension(file_path=file_path)
	priority = get_priority(searched_word=searched_word)
	root_dir = get_root_directory(file_path=file_path, search_path=search_path)
	return {
		"Root_Directory": root_dir,
		"File_Path": file_path,
		"Line_Number": line_number,
		"Snippet": code_snippet,
		"Searched_Word": searched_word,
		"Priority": priority,
		"File_Extension": file_ext
	}

def get_priority(searched_word):
	return PRIORITY_BY_WORDS[searched_word]

def get_file_path(occurence_split_by_colons):
	return occurence_split_by_colons[0]

def get_line_number(occurence_split_by_colons):
	return occurence_split_by_colons[1]

def get_code_snippet(occurence_split_by_colons):
	return " ".join(occurence_split_by_colons[2:]).strip()

def get_file_extension(file_path):
	file, ext = os.path.splitext(str(file_path))
	if ext:
		return ext
	else:
		return file.split("/")[-1]

def get_root_directory(file_path, search_path):
	return os.path.relpath(str(file_path), search_path).split("/")[0]

if __name__ == "__main__":
	start = time.time()
	main()
	print("Finished in %s seconds" % str(round(time.time() - start, 2)))
