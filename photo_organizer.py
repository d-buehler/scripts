#!/usr/bin/python3

import os
import time
import shutil
import exifread
from argparse import ArgumentParser


if __name__ == "__main__":

	parser = ArgumentParser()
	parser.add_argument(
		"directory",
		help="the directory containing the files you wish to organize",
	)
	args = parser.parse_args()

	path = args.directory
	if not os.path.exists(path):
		raise Exception(f"{path} does not exist.")

	files = os.listdir(path)

	files_by_date_dict = {}
	for f in files:
		full_path = path + "/" + f
		with open(full_path, "rb") as file:
			tags = exifread.process_file(file)
		
		ctime_fmt_date = time.strftime(
			"%Y-%m-%d",
			time.strptime(
				tags["EXIF DateTimeOriginal"].printable,
				"%Y:%m:%d %H:%M:%S"
			)
		)
		
		if ctime_fmt_date not in files_by_date_dict.keys():
			files_by_date_dict[ctime_fmt_date] = [full_path]
		else:
			files_by_date_dict[ctime_fmt_date].append(full_path)


	years = {
		time.strftime("%Y", time.strptime(date, "%Y-%M-%d"))
		for date in files_by_date_dict
	}
	# print(years)
	# print(files_by_date_dict)

	output_dir = path
	for year in years:
		year_output_dir = output_dir + "/" + year
		if not os.path.exists(year_output_dir):
			os.mkdir(year_output_dir)

	for date, files in files_by_date_dict.items():
		year = time.strftime("%Y", time.strptime(date, "%Y-%M-%d"))
		
		date_output_dir = output_dir + "/" + year + "/" + date
		if not os.path.exists(date_output_dir):
			os.mkdir(date_output_dir)

		for file in files:
			fname = file.split("/")[-1]
			new_full_path = date_output_dir + "/" + fname
			shutil.move(file, new_full_path)