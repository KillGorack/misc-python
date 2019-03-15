import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

im = Image.open('E:/Users/David/Documents/python/Mario.png')
height = im.size[1]

# We need a float array between 0-1, rather than
# a uint8 array between 0-255
im = np.array(im).astype(np.float) / 255

fig = plt.figure()

plt.plot(np.arange(10), 4 * np.arange(10))

# With newer (1.0) versions of matplotlib, you can 
# use the "zorder" kwarg to make the image overlay
# the plot, rather than hide behind it... (e.g. zorder=10)
fig.figimage(im, 0, fig.bbox.ymax - height)

# (Saving with the same dpi as the screen default to
#  avoid displacing the logo image)
fig.savefig('E:/Users/David/Documents/python/Mario.png', dpi=80)

plt.show()
