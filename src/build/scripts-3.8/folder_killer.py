# Author: Ashkan Mohammadi
# Email: mohammadiashkan1384@gmail.com
# usage: python folder_killer.py <folder_name>
#                                -------------
#                                ^ replace it
#
# example: python folder_killer.py testing_folder

import argparse
import os
from os.path import isdir, isfile
import importlib
from logger import Logger
from plugins.system.pluginSystem import event_emitter
import plugins.system.signals

class Program:

	def main(self):
		self.initPlugins()
		args = self.getArguments()
		try:
			number_of_deleted_folders, deleted_folders = self.delete_empty_folders(args.folder)
			event_emitter.emit("post-delete", number_of_deleted_folders, deleted_folders)
		except Exception as e:
			self.handleException(e)
		else:
			self.prepareOutput(number_of_deleted_folders, deleted_folders)
		self.unloadPlugins()

	def initPlugins(self):
		os.chdir("plugins")
		plugins_list: list = [
			plugin for plugin in os.listdir()
			if 
				plugin.endswith(".py") 
				and not plugin.startswith("_")
			]
		self.plugins_to_unload: list = []
		for plugin in plugins_list:
			plugin_handle = importlib.import_module(f"plugins.{plugin[:-3]}")
			plugin_instance = plugin_handle.Plugin(event_emitter)
			plugin_instance.loadPlugin()
			self.plugins_to_unload.append(plugin_instance)

	def delete_empty_folders(self, folder):
		number_of_deleted_folders = 0
		os.chdir(folder)
		path = os.getcwd()
		deleted_folders = []
		if not (files:=os.listdir()):
			os.chdir("..")
			os.system("rmdir " + folder)
			return [number_of_deleted_folders + 1, [path]]
		event_emitter.emit("files-listed", files)
		for file in files:
			if isdir(file):
				results = delete_empty_folders(file)
				number_of_deleted_folders += results[0]
				deleted_folders += results[1]
				continue
		os.chdir("..") # get back to the parent directory
		return [number_of_deleted_folders, deleted_folders]


	def getArguments(self):
		parser = argparse.ArgumentParser(description="deletes empty folders")
		parser.add_argument("folder")
		args = parser.parse_args()
		event_emitter.emit("arguments-parsed", args)
		return args


	def handleException(self, e):
		event_emitter.emit("error", e)
		Logger().error(e) # log the error
		print ("there was an error while deleting empty folders")
		self.askOpenLogFile()
		event_emitter.emit("error-handled")


	def askOpenLogFile(self):
		if {"y": True, "n": False}[input ("want to check the log: " + os.getcwd() + "\\log.txt? (y,n): ")[0].lower()]:
			os.system("notepad log.txt" if os.name == "nt" else "nano log.txt")


	def prepareOutput(self, number_of_deleted_folders, deleted_folders):
		outputs = [
			"{} empty folder deleted",
			"{} empty folders deleted",
		]
		event_emitter.emit("pre-output")
		for folder in deleted_folders:
			print (folder)
			event_emitter.emit("folder-prited", folder)
		print ("\n" + outputs[min(1, number_of_deleted_folders-1)].format(number_of_deleted_folders))
		event_emitter.emit("post-output")


	def unloadPlugins(self):
		for plugin in self.plugins_to_unload:
			plugin.unloadPlugin()
			
			


if __name__ == "__main__":
	event_emitter.emit("start")
	Program().main()
	event_emitter.emit("exit")