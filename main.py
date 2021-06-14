import numpy as np
import PIL
from PIL import Image

# print('Pillow Version:', PIL.__version__)

# load and show an image with Pillow
# Open the image form working directory
image = Image.open('images/Koala_climbing_tree.jpg')
# summarize some details about the image
print(image.format)
print(image.size)
print(image.mode)

# show the image
image.show()

# Two matrices are
#  initialized by value
x = np.array([[1, 2], [4, 5]])
y = np.array([[7, 8], [9, 10]])


#  add()is used to add matrices
print("Addition of two matrices: ")
print(np.add(x, y))
