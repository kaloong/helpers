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
import datetime, sys
import click
from pathlib import Path

def create_testdir():
	Path("testdir").mkdir(parents=True, exist_ok=True)

def create_testfile():
	for f in range(10):
		Path("testdir/testfile-3-2-2020-{}.time".format(f)).touch()
	for f in range(10):
		Path("testdir/testfile-2-2-2020-{}.log".format(f)).touch()
	"""
	for f in range(10):
		Path("testdir/testfile2-2020-01-30-{}.log".format(f)).touch()
	"""

def extract_date( target ):
	"""
	Extract date from filename
	"""
	regex_list=['\d{1,2}-\d{1,2}-\d{4}', '\d{4}-\d{1,2}-\d{1,2}' ]
	fmt_list=['%d-%m-%Y','%Y-%m-%d']	
	date_regex=re.compile('|'.join(regex_list))

	result_date=None
	target_date = date_regex.search(target)
	for fmt in fmt_list:
		
		if target_date is not None:
			try: 
				result_date=datetime.datetime.strptime(target_date.group(),"{}".format(fmt))
			except:
				pass
	try:
		'''
		If search is ok, return new datetime object and current date string(to be used for regex substitution)
		'''
		return result_date, target_date.group()
	except AttributeError as e:
		print(">>> Error: {}\n>>> Target file does not match in regex_list. Script terminated.".format(e))
		sys.exit()


def create_new_filename( target ):

	result_date, cur_date_fmt =extract_date( target )
	if result_date:
		new_date_fmt=result_date.strftime('%Y-%m-%d')
		'''
		New name will have its date substituted 
		from: testfile-4-12-2020-1.log 
		to:   testfile-2020-12-04-1.log
		'''
		new_name = re.sub( cur_date_fmt, new_date_fmt, target )
		return new_name
	'''
	This is not needed I think.
	'''
	return "{}".format(target)
	

def create_new_dirname(target):
	new_dirname, _ = extract_date(target)
	return new_dirname.strftime('%Y%m%d')


def main():

	parser = argparse.ArgumentParser()
	group1 = parser.add_mutually_exclusive_group(required=True)
	group2 = parser.add_argument_group()

	group1.add_argument("-g","--generate",help="Generate test directory and files", action='store_true')
	group1.add_argument("-t","--target", help="Specify target folder -t testdir")
	group2.add_argument("-d","--directory", help="Move files to new directory based on date", action='store_true', default=False)
	args = parser.parse_args()
	if args.generate:
		"""
		Generate test data if option is specified.
		"""
		create_testdir()
		create_testfile()
	if args.target:
		try:
			p=Path(args.target)
			"""
			What does 'f' stand for? Give meaningful name.
			"""
			for f in p.iterdir(): 
				if not f.is_dir():
					new_filename = create_new_filename( f.name )
					'''print("New name: {}".format(new_filename))'''
					new_dirname=None
					if args.directory :
						new_dirname = create_new_dirname( f.name )
						"""
						What does 'a' stand for? Give meaningful name.
						"""
						a = Path(args.target+"/"+ new_dirname).mkdir(parents=True,exist_ok=True)

					if new_dirname is not None:
						a = Path(args.target+"/"+new_dirname+"/"+new_filename)
					else:
						a = Path(args.target+"/"+new_filename)

					if not a.exists():
						f.rename(a)
						print(f)
					else:
						if click.confirm("Looks like file {} already exists: {},\nwould you like to overwrite?".format(a, a.exists()), default=True):
							'''check if we should replace it'''
							f.replace(a)
		except FileNotFoundError as e:
			print("{}".format(e))


if __name__ == '__main__':
	main()

