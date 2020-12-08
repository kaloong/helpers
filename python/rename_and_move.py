#!/usr/bin/python


"""
Test data filename:
===================
timefile="ssh-18-06-2020-14h-23m-40s-svc_user-21239.time"
logfile="ssh-18-06-2020-14h-23m-40s-svc_user-21239.log"

Specify target dummy folder
Generate dummy data file

Psuedocode:
loop
get filename
extract info(such as date) from filename
check if date folder exists in target logfolder, if not exists create folder.
check if filename is in use under process, if not move file to folder. 
go loop, for next file


old patterns and options:
	file_pattern="\d\d-\d\d-\d\d\d\d-\d\dh-\d\dm-\d\ds"
	old_pattern="%d-%m-%Y-%Hh-%Mm-%Ss"
	new_pattern="%Y-%m-%d-%Hh-%Mm-%Ss"

	parser.add_argument("-p","--pattern",help="Filename date regex. E.g. DD-MM-YYYY shouldbe \d\d-\d\d-\d\d\d\d",default="\d\d-\d\d-\d\d\d\d")
	required_parser = parser.add_argument_group("Required options for -p.")
	required_parser.add_argument("-b","--before",help="Date format before \%d-\%m-\%Y. E.g. 31-12-2020",default="%d-%m-%Y")
	required_parser.add_argument("-a","--after", help="Date format after  \%Y-\%m-\%d. E.g. 2020-12-31", default="%Y-%m-%d")
	args = parser.parse_args()
	print("---{}".format( args.before ) )

"""
import re, argparse
import datetime
from pathlib import Path

def create_testdir():
	Path("testdir").mkdir(parents=True, exist_ok=True)

def create_testfile():
	for f in range(10):
		Path("testdir/testfile-08-12-2020-{}.py".format(f)).touch()

def rename( target, file_pattern, old_pattern, new_pattern):

	'''date_regex=re.compile(r'\d\d-\d\d-\d\d\d\d-\d\dh-\d\dm-\d\ds')'''
	date_regex=re.compile(file_pattern)
	target_date=date_regex.search( target )
	if target_date:
		file_date=datetime.datetime.strptime(target_date.group(), old_pattern)
		old_fmt=file_date.strftime(old_pattern)
		new_fmt=file_date.strftime(new_pattern)
		new_name = re.sub( old_fmt, new_fmt, target )
		return new_name
	return "{}".format(target)

def main():

	file_pattern="\d\d-\d\d-\d\d\d\d"
	old_pattern="%d-%m-%Y"
	new_pattern="%Y-%m-%d"


	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group(required=True)
	"""

	"""

	group.add_argument("-g","--generate",help="Generate test dir files", action='store_true')
	group.add_argument("-t","--target", help="Specify target folder -t testdir")
	args = parser.parse_args()
	if args.generate:
		create_testdir()
		create_testfile()
	if args.target:
		try:
			p=Path(args.target)
			for f in p.iterdir(): 
				new_name = rename( f.name, file_pattern, old_pattern, new_pattern )
				a = Path(args.target+"/"+new_name)
				if not a.exists():
					f.rename(a)
					print(f)
				else:
					print("File {} already exists. Skip".format(a))
		except FileNotFoundError as e:
			print("{}".format(e))


if __name__ == '__main__':
	main()

