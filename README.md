# folder-killer

simple python script to delete empty folders from your computer

## installation

```bash
$ python setup.py install
```

## usage

```bash
$ python -m folder_killer <folder_name>
```

## plugins

this python project also supports plugins. to see an example of a plugin file,
please refer to plugins/deleteImages.py
"delteImages.py" extends the behaviour of the program by allowing it to scan for
jpg files inside the folders and delete them. this plugin will delete jpg images
if you use the command line flag `--delete-jpg-images`.

### how to create a plugin

all plugins should be placed in plugins folder to be loaded. there is
a `system` package inside plugins folder. All the plugins should be 
a python module and all of them should have a top level class called
Plugin. the class `Plugin` should extend `BasePlugin` from `plugins.system.pluginSystem`
and also it should implement `loadPlugin` and `unloadPlugin` methods. the `loadPlugin`
method is used to initialize the plugin and you can perform clean up tasks
(such as unsubscribing the events) in `unloadPlugin`
method

## create your first plugin

create a new file inside plugins folder called `samplePlugin.py`. the name should not
start with an underscore otherwise it won't qualify as a plugin.  

now insert this import statement:

```python
from plugins.system.pluginSystem import BasePlugin
```

then create a top level class called Plugin which extends BasePlugin. the `BasePlugin` class
provieds some useful functions for subclasses.

```python
from plugins.system.pluginSystem import BasePlugin

class Plugin(BasePlugin):
    pass
```