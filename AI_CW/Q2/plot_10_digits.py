from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler


digits = load_digits()
dataset = digits.data

for idx, image in enumerate(digits.images[:20]):
    plt.subplot(2, 10, idx+1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')

plt.show()
