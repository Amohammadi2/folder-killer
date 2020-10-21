from functools import partial
from pyee import BaseEventEmitter
event_emitter  = BaseEventEmitter()

class BasePlugin:
    
    def __init__(self, event_e):
        self._emitter = event_e
        self._listeners: list = []
        self.getListenersList()

    def getListenersList(self):
        self._listeners = [
            # means get all the methods that qualify as a listener
            method for item in dir(self) 
            if 
                callable((method:=getattr(self, item))
                and not item == "getMethodsList" 
                and not item.startswith("_")
                and     item.endswith("_listener"))
        ]
            
    def subscribeEvent(self, event_name, listener):
        self._emitter.on(event_name, listener)
        event_emitter.remove_listener
        return partial(self._emitter.remove_listener, event_name, listener)

    def loadPlugin(self):
        raise NotImplementedError(
            "this method should be implemented by a subclass"
        )

    def unloadPlugin(self):
        raise NotImplementedError(
            "this method should be implemented by a subclass"
        )