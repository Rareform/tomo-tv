"""
Total-variation penalization for tomography reconstruction
==========================================================

In this example, we reconstruct an image from its tomography projections
with an uncomplete set of projections (l/3 angles, where l is the linear
size of the image. For a correct reconstruction without a-priori information,
one would usually require l or more angles). In addition, noise is added to
the projections.

In order to reconstruct the original image, we minimize a function that is
the sum of (i) a L2 data fit term, and (ii) the total variation of the image.
Proximal iterations using the FISTA scheme are used.

This example should take around 30 seconds to compute and plot the results.
"""

print (__doc__)


import numpy as np
from reconstruction.forward_backward_tv import fista_tv,watershed_norm,watershedshow,tv
from reconstruction.projections import build_projection_operator
from reconstruction.util import generate_synthetic_data
from time import time
import matplotlib.pyplot as plt
from skimage.io import imread

# Synthetic data
l = 256
x = generate_synthetic_data(l)

x = imread('C:/Users/Roman/Documents/Developer/Images/Lenna.png', as_grey=True)
x = x[100:356,100:356]

# Projection operator and projections data, with noise
H = build_projection_operator(l, l/3)
y = H * x.ravel()[:, np.newaxis]
y += 2*np.random.randn(*y.shape)

# Reconstruction
t1 = time()
#res, energies = fista_tv(y, 50, 100, H) 
t2 = time()
print ("reconstruction done in %f s" %(t2 - t1) )

# Fraction of errors of segmented image wrt ground truth
#err = [np.abs(x - (resi > 0.5)).mean() for resi in res]



#===============================================================================
# # Display results
# plt.figure()
# plt.subplot(221)
# plt.imshow(x, cmap='gray', interpolation='nearest', vmin=0, vmax=1)
# plt.title('original data (256x256)')
# plt.axis('off')
# plt.subplot(222)
# #plt.imshow(res[-1], cmap='gray', interpolation='nearest', vmin=0, vmax=1)
# plt.imshow(energies, cmap='gray')
# plt.title('reconstruction after 100 iterations')
# plt.axis('off')
# plt.subplot(223)
# #plt.loglog(energies, 'o')
# plt.xlabel('iteration number')
# plt.title('energy')
# plt.subplot(224)
# #plt.loglog(err, 'o')
# plt.xlabel('iteration number')
# plt.title('error fraction')
# plt.show()
#===============================================================================

err = np.zeros(100)
energies=watershed_norm(x)
watershed = watershedshow(x)
tv= tv(x)

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 8), sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
ax = axes.ravel()

ax[0].imshow(x, cmap=plt.cm.gray, interpolation='nearest')
ax[0].set_title("Original")

ax[1].imshow(tv, cmap=plt.cm.spectral, interpolation='nearest')
ax[1].set_title("Local Gradient")

ax[2].imshow(x, cmap=plt.cm.spectral, interpolation='nearest')
ax[2].set_title("Markers")

#ax[3].imshow(image, cmap=plt.cm.gray, interpolation='nearest')
ax[3].imshow(watershed, cmap=plt.cm.gray, interpolation='nearest', alpha=.7)
ax[3].set_title("Segmented")

for a in ax:
    a.axis('off')

fig.tight_layout()
plt.show()