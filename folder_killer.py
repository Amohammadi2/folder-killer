# Author: Ashkan Mohammadi
# Email: mohammadiashkan1384@gmail.com

import argparse
import os
from os.path import isdir

def delete_empty_folders(folder):
	os.chdir(folder)
	if not (files:=os.listdir()):
		os.chdir("..")
		os.system("rmdir " + folder)
		return
	for file in files:
		if isdir(file):
			delete_empty_folders(file); continue
	os.chdir("..") # get back to the parent

def main():
	parser = argparse.ArgumentParser(description="deletes empty folders")
	parser.add_argument("folder")
	args = parser.parse_args()
	try:
		delete_empty_folders(args.folder)
	except Exception as e:
		print ("an error occured when deleting the folder")
		print (e)
		exit()
	else:
		print ("empty folders deleted")


if __name__ == "__main__":
	main()