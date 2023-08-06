# Description

Intuitive PNG library. 

# Usage


## All-in-1
```python
from ipng import PNG

png = PNG(file='path/to/input.png')
print(png.metadata)
print(f'this is a {png.width}x{png.height} picture =)')
png.render(output='path/to/output.png')
```
