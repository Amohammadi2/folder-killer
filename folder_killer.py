# Author: Ashkan Mohammadi
# Email: mohammadiashkan1384@gmail.com
# usage: python folder_killer.py <folder_name>
#                                -------------
#                                ^ replace it
#
# example: python folder_killer.py testing_folder

import argparse
import os
from os.path import isdir
from logger import Logger

def delete_empty_folders(folder):
	number_of_deleted_folders = 0
	os.chdir(folder)
	path = os.getcwd()
	deleted_folders = []
	if not (files:=os.listdir()):
		os.chdir("..")
		os.system("rmdir " + folder)
		return [number_of_deleted_folders + 1, [path]]
	for file in files:
		if isdir(file):
			results = delete_empty_folders(file)
			number_of_deleted_folders += results[0]
			deleted_folders += results[1]
			continue
	os.chdir("..") # get back to the parent directory
	return [number_of_deleted_folders, deleted_folders]

def main():
	parser = argparse.ArgumentParser(description="deletes empty folders")
	parser.add_argument("folder")
	args = parser.parse_args()
	try:
		number_of_deleted_folders, deleted_folders = delete_empty_folders(args.folder)
	except Exception as e:
		Logger().error(e) # log the error
		print ("there was an error while deleting empty folders")
	else:
		outputs = [
			"{} empty folder deleted",
			"{} empty folders deleted",
		]
		for folder in deleted_folders:
			print (folder)
		print ("\n" + outputs[min(1, number_of_deleted_folders-1)].format(number_of_deleted_folders))


if __name__ == "__main__":
	main()
