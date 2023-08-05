### Apps / Toolchains

It's easy to get an latest app instance.

```python
from mcutk.apps import appfactory
# get iar APP by factory method
APP = appfactory('iar')
app = APP.get_latest()

print app.version
print app.path
print app.is_ready

```

or create instance by specific path.

```python
from mcutk.apps import appfactory
app = appfactory('iar')('C:/Program Files(x86)/IAR Sytems/IAR Workbench/', version='8.22.1')

print app
```

Use app instance to build project


```python
import os
from mcutk.apps import appfactory

# scan system and get the latest version of instance
iarapp = appfactory("iar").get_latest()

# load project
project = iarapp.Project("hello_world.eww")

# get app name
print project.name

# get app targets
targets = project.targets

# loop build each target
for target in targets:
    # set log path
    logfile = os.path.join(project.prjdir, target+"_log.log")
    # build the project
    result = iarapp.build_project(project, target, logfile)
    print result

```


### Board in mcutk

mcutk Board is a data model and supporting some useful functionality.

- board basic

```python
from mcutk.board import getboard

# render a board object
board = getboard(name="frdmkl43z", devicename="MKL43Z256xxx4", interface="SWD", debugger_type="pyocd")
board.serial = "COM5"
board.baudrate = "115200"
```

- debugger


```python
from mcutk.debugger import getdebugger

# get latest jlink as we did before
jlink = getdebugger('jlink').get_latest()

# check jlink
if jlink.is_ready:
    print 'ready'

# show version and path
print jlink.version, jlink.path

```



- board programming and debugging


```python
import serial
from mcutk.board import getboard
from mcutk.debugger import getdebugger

# get board object
board = getboard(name="frdmkl43z", devicename="MKL43Z256xxx4", interface="SWD", debugger_type="jlink")
board.serial = "COM5"
board.baudrate = "115200"
board.usbid = '2010101010'

# get debugger object
jlink = getdebugger(board.debugger_type).get_latest()
if jlink.is_ready:
    print jlink.version
    print jlink.path

jlink.gdbpath = "C:/MinGW/bin/gdb.exe"

board.debugger = jlink

# support register callback execute before loading image.
@board.debugger.register("before-load")
def callback():
    print "This is callback function"
    print "Do something before load image"
    print "Example open serial port"
    sport = serial.Serial(boards.serial, board.baudrate)
    print sport.read()
    sport.close()
    print "Callback end"

# erase flash
board.debugger.erase()
# unlock kinetis
board.debugger.unlock()
# unified interface for programming
board.programming("hello_world.out")
# reset board
board.debugger.reset()
```


### Serial ports in mcutk

mcutk extend and improve [pyserial](https://pythonhosted.org/pyserial/ "pyserial") and [python-pexpect](https://pexpect.readthedocs.io/en/stable/ "python-pexpect") to support more advanced features.

expect is a very useful tool to interact with other application. `mcutk.pserial.SerialSpawn` can interact with serial port. The usage is very simple.

You can go to [pexpect-doc](https://pexpect.readthedocs.io/en/stable/ "doc") for more.

Here is a short example:

```python
from mcutk.pserial import Serial
from mcutk.pserial import SerialSpawn

# open serial port
ser = Serial('COM3', 9600)

# create spawn object
spawn = SerialSpawn()

# set logfile for serial read, we used the console.
spawn.logfile_read = sys.stdout

# input a value and check the output match the expectation until timeout
# return value is the output
output = spawn.test_input("A", "Waiting for power mode select..", timeout=3)

# interact step by step
spawn.expect("please input your username")
spawn.write("admin\n")
spawn.expect("please input your password\n")
spawn.expect("admin123")

# also support regular expression
spawn.expect("waiting for.*mode \sselection\n")
spawn.expect("2\n")

# close serial port
spawn.close()
```