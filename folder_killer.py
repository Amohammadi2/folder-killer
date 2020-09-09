# Author: Ashkan Mohammadi
# Email: mohammadiashkan1384@gmail.com

import argparse
import os
from os.path import isdir

def delete_empty_folders(folder):
	number_of_deleted_folders = 0
	os.chdir(folder)
	if not (files:=os.listdir()):
		os.chdir("..")
		os.system("rmdir " + folder)
		return number_of_deleted_folders + 1
	for file in files:
		if isdir(file):
			number_of_deleted_folders += delete_empty_folders(file)
			continue
	os.chdir("..") # get back to the parent directory
	return number_of_deleted_folders

def main():
	parser = argparse.ArgumentParser(description="deletes empty folders")
	parser.add_argument("folder")
	args = parser.parse_args()
	try:
		deleted_folders = delete_empty_folders(args.folder)
	except Exception as e:
		print ("an error occured when deleting the folder")
		print (e)
		exit()
	else:
		print (f"{deleted_folders} empty folders deleted")


if __name__ == "__main__":
	main()
