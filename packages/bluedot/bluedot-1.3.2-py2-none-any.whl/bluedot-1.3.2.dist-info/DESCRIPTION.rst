# Blue Dot

[Blue Dot](http://bluedot.readthedocs.io/en/latest/) allows you to control your Raspberry Pi projects wirelessly - it's a Bluetooth remote and zero boiler plate (super simple to use :) Python library.

## Getting started

1. Install

```
sudo pip3 install bluedot
```

2. Get the [Android Blue Dot app](http://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot) or use the [Python Blue Dot app](http://bluedot.readthedocs.io/en/latest/bluedotpythonapp.html)

3. Pair your Raspberry Pi

4. Write some code

```python
from bluedot import BlueDot
bd = BlueDot()
bd.wait_for_press()
print("You pressed the blue dot!")
```

5. Press the Blue Dot

See the [getting started guide](http://bluedot.readthedocs.io/en/latest/gettingstarted.html) to 'get statred'!

## More

The Blue Dot is a joystick as well as button. You can tell if the dot was pressed in the middle, on the top, bottom, left or right. You can easily create a BlueDot controlled Robot.

Why be restricted by such vague positions like top and bottom though: you can get the exact (x, y) position or even the angle and distance from centre where the dot was pressed.

Its not all about when the button was pressed either - pressed, released or moved they all work.

You can press it, slide it, swipe it, rotate it - one blue circle can do a lot!

## Even more

The [online documentation](http://bluedot.readthedocs.io/en/latest/) describes how to use Blue Dot and the Python library including recipes and ideas.



