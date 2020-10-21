from plugins.system.pluginSystem import BasePlugin, event_emitter
import os

class Plugin(BasePlugin):
    
    def loadPlugin(self):
        self.listeners_to_unsubscribe: list = [
            self.subscribeEvent("argument-parser-ready", self.addCommandLineArgument),
            self.subscribeEvent("arguments-parsed", self.checkDeleteImageFlagActive)
        ]

    def addCommandLineArgument(self, parser):
        parser.add_argument("--delete-jpg-images", action="store_true", dest="delete_images")

    def deleteImages(self, files, current_dir):
        print ("the event is emitted")
        for file in files:
            if file.endswith(".jpg"):
                os.remove(os.path.join(current_dir, file))

    def checkDeleteImageFlagActive(self, commandline_arguments):
        if commandline_arguments.delete_images:
            self.listeners_to_unsubscribe += [
                self.subscribeEvent("files-listed", self.deleteImages)
            ]

    def unloadPlugin(self):
        for unsubscribeCallbackFN in self.listeners_to_unsubscribe:
            unsubscribeCallbackFN()
