from plugins.system.pluginSystem import BasePlugin, event_emitter
import os

class Plugin(BasePlugin):
    
    def loadPlugin(self):
        print (id(self._emitter))
        self.listeners_to_unsubscribe: list = [
            self.subscribeEvent("files-listed", self.delete_images)
        ]
        self._emitter.on("files-listed", self.delete_images)

    def delete_images(self, files, current_dir):
        print ("the event is emitted")
        for file in files:
            if file.endswith(".jpg"):
                os.remove(os.path.join(current_dir, file))

    def unloadPlugin(self):
        for unsubscribeCallbackFN in self.listeners_to_unsubscribe:
            unsubscribeCallbackFN()
