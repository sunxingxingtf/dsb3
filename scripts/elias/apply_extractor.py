import pickle as pkl
import numpy as np
from skimage.measure import label, regionprops
from extract_nodules import extract_nodules_best_kmeans, extract_nodules_best_gmix, extract_nodules_conv_filter

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


folder = 'storage/metadata/dsb3/model-predictions/ikorshun/luna_scan_v3_dice-20170202-154805/'

patient_id = '1.3.6.1.4.1.14519.5.2.1.6279.6001.121391737347333465796214915391' 
# there is only one cancerous nodule in this patient
# original coos
# [(49.31293635, -63.21521025, -118.7995619, 22.13322034)]
# vox coos
# [array([ 312.98274683,  169.22729589,  154.76035048])]
# diameter
# [22.13322034]

# load in predicted segmentation
pred = pkl.load(open(folder+'pred_'+patient_id+'.pkl', 'rb' ))
print pred.shape

target = pkl.load(open(folder+'tgt_'+patient_id+'.pkl', 'rb' ))
print target.shape

#only one nodule
listofcoos = np.where(target[0,0]==1)
center = [np.round(np.average(listofcoos[0])).astype(int), np.round(np.average(listofcoos[1])).astype(int), np.round(np.average(listofcoos[2])).astype(int)]

	
fig = plt.figure()

ax1 = fig.add_subplot(3,1,1)
ax1.imshow(target[0,0,center[0],:,:].transpose())
circ1 = plt.Circle((center[1],center[2]), 24, color='y', fill=False)
ax1.add_patch(circ1)

ax2 = fig.add_subplot(3,1,2)
ax2.imshow(target[0,0,:,center[1],:])
circ2 = plt.Circle((center[0],center[2]), 24, color='y', fill=False)
ax2.add_patch(circ2)

ax3 = fig.add_subplot(3,1,3)
ax3.imshow(target[0,0,:,:,center[2]].transpose())
circ3 = plt.Circle((center[0],center[1]), 24, color='y', fill=False)
ax3.add_patch(circ3)
fig.savefig('original_mask.jpg')


labeled_target = label(target[0,0])
regions = regionprops(labeled_target)
for region in regions:
	print region.area


print np.histogram(target)

#extract_nodules_best_kmeans(pred[0,0], 10, True)
#extract_nodules_best_gmix(pred[0,0], 20, True)
extract_nodules_conv_filter(pred[0,0], pred[0,0], no_rois=5, dim=16, plot=False, dbg_target=target[0,0])



print np.histogram(pred)

