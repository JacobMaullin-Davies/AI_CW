from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale




digits = load_digits()
dataset = digits.data
print(digits.data.shape)

# Create a Randomized PCA model that takes two components
# randomized_pca = RandomizedPCA(n_components=2)
#
# # Fit and transform the data to the model
# reduced_data_rpca = randomized_pca.fit_transform(digits.data)

# Create a regular PCA model
pca = PCA(n_components=2)
# Fit and transform the data to the model
reduced_data_pca = pca.fit_transform(digits.data)
# Inspect the shape
reduced_data_pca.shape

x_min = reduced_data_pca[:, 0].min() - 10
x_max = reduced_data_pca[:, 0].max() + 10
y_min = reduced_data_pca[:, 1].min() - 10
y_max = reduced_data_pca[:, 1].max() + 10
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)


kmeans = KMeans(init='k-means++', n_clusters=10, n_init=10)
kmeans.fit(reduced_data_pca)

h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap='viridis',
           aspect='auto',
           origin='lower')


##########################################



#plt.plot(reduced_data_pca[:, 0], reduced_data_pca[:, 1], 'k.', markersize=1)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10, label=0)



colors = ['black', 'blue', 'purple', 'yellow', 'pink', 'red', 'lime', 'cyan', 'orange', 'gray']
for i in range(0,10):
    x = reduced_data_pca[:, 0][digits.target == i]
    y = reduced_data_pca[:, 1][digits.target == i]
    plt.scatter(x, y, c=colors[i],s=5, label=colors[i])
    plt.legend(digits.target_names, bbox_to_anchor=(1,1), loc=2, borderaxespad=0.)



plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title("PCA Scatter Plot")



plt.show()

# plt.imshow(digits.images[10], cmap='gray')
# model.predict(dataset[0].reshape(1,-1))
#
# for idx, image in enumerate(digits.images[:10]):
#     plt.subplot(2, 5, idx+1)
#     plt.axis('off')
#     plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')

# data, labels = load_digits(return_X_y=True)
# (n_samples, n_features), n_digits = data.shape, np.unique(labels).size
#
# print(
#     f"# digits: {n_digits}; # samples: {n_samples}; # features {n_features}"
# )
#
# X, y = make_blobs(n_samples=1797, centers=10, cluster_std=0.7, random_state=0)
# plt.scatter(X[:,0], X[:,1])
#
# plt.gray()
# plt.matshow(digits.images[333])
plt.show()
