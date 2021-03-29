import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA


#Load digits
digits = load_digits()
dataset = digits.data
print(digits.data.shape)

pca = PCA(n_components=2)

# Fit and transform the data to the model
reduced_data_pca = pca.fit_transform(digits.data)

# Inspect the shape
reduced_data_pca.shape
#find the maximum and minimum XY values
x_min = reduced_data_pca[:, 0].min() - 10
x_max = reduced_data_pca[:, 0].max() + 10
y_min = reduced_data_pca[:, 1].min() - 10
y_max = reduced_data_pca[:, 1].max() + 10
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)


kmeans = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
 n_clusters=10, n_init=10, n_jobs=1, precompute_distances='auto',
 random_state=None, tol=0.0001, verbose=0)

kmeans.fit(reduced_data_pca)

h = .02     # point in the mesh
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap='viridis',
           aspect='auto',
           origin='lower')

##########################################

Kmean = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
 n_clusters=10, n_init=10, n_jobs=1, precompute_distances='auto',
 random_state=None, tol=0.0001, verbose=0)
Kmean.fit(reduced_data_pca)

# Plot the centroids
centroids = Kmean.cluster_centers_
centroid01= []
for i in range(len(centroids)):
    list = []
    coord = centroids[i]
    list.append(coord[0])
    list.append(coord[1])
    centroid01.append(list)

centroid01.sort(key=lambda x:x[1])
#sort centroids
ax = plt.subplot(111)
t = 0
for i in centroid01:

    plt.scatter(i[0], i[1],
        marker='x', s=169, linewidths=3,
        color='black', zorder=10, label="Centroid")
    #Annotate the centroids with the number it represents
    imagebox = offsetbox.AnnotationBbox(
            offsetbox.OffsetImage(digits.images[t], cmap=plt.cm.gray_r, zoom=2), xy=(i[0]+2, i[1]))
    ax.add_artist(imagebox)
    t+=1

colors = ['black', 'blue', 'purple', 'yellow', 'violet', 'red', 'lime', 'cyan', 'orange', 'gray']

for i in range(10):
    x = reduced_data_pca[:, 0][digits.target == i]
    y = reduced_data_pca[:, 1][digits.target == i]
    plt.scatter(x, y, c=colors[i], s=5, label=i)


plt.xlabel('')
plt.ylabel('')
plt.title("Kmeans Scatter Plot")



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
