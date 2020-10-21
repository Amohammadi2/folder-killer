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
from pathlib import Path

command_line_current_dir = os.getcwd()
os.chdir(Path(__file__).resolve().parent)

class Program:

	def main(self):
		self.initPlugins()
		args = self.getArguments()
		try:
			number_of_deleted_folders, deleted_folders= self.delete_empty_folders_exp(
				args.folder, command_line_current_dir
			)
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

	def delete_empty_folders_exp(self, folder, current_dir):
		number_of_deleted_folders = 0
		deleted_folders:list = []
		current_dir = os.path.join(current_dir, folder)
		print (current_dir)
		if not (files:=os.listdir(current_dir)):
			os.rmdir(current_dir)
			results =  [number_of_deleted_folders + 1, [current_dir]]
			current_dir, _ = os.path.split(current_dir)
			return results
		event_emitter.emit("files-listed", files, current_dir)
		for file in files:
			if isdir(os.path.join(current_dir, file)):
				subprocess_result = self.delete_empty_folders_exp(file, current_dir)
		if not os.listdir(current_dir):
			deleted_folders += [current_dir]
			number_of_deleted_folders += 1
			current_dir, _ = os.path.split(current_dir)
			os.rmdir(current_dir)
		return [number_of_deleted_folders, deleted_folders]


	def getArguments(self):
		parser = argparse.ArgumentParser(description="deletes empty folders")
		parser.add_argument("folder")
		event_emitter.emit("argument-parser-ready", parser)
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