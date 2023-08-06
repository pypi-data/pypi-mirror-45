# Description

Intuitive PNG library. 

# Usage


## All-in-1
```python
from ipng import PNG
from binascii import hexlify

def func(bitmap):
    # do anything with the bytearray, here we just print out the 
    # first 100 bytes of each row
    print(hexlify(bitmap)[0:100])

png = PNG(file='path/to/input.png', process=func)
print(png.metadata) # get info about the image
png.render(output='path/to/output.png') # only "render" will trigger the process, path can be None
```
