from collections import namedtuple
import numpy as np
import cv2

# define the `Detection` object
Detection = namedtuple("Detection", ["image_path", "gt", "pred"])

def get_iou(a, b):

    # a: real image
    # b: predicted image
    # COORDINATES OF THE INTERSECTION BOX / Order: [xmin, ymin, xmax, ymax]
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])

    # AREA OF OVERLAP - Area where the boxes intersect
    width = (x2 - x1)
    height = (y2 - y1)
    # handle case where there is NO overlap
    if (width<0) or (height <0):
        return 0.0
    area_overlap = width * height

    # COMBINED AREA
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    area_combined = area_a + area_b - area_overlap

    # RATIO OF AREA OF OVERLAP OVER COMBINED AREA
    iou = area_overlap / (area_combined)
    return iou

# define the list of example detections. Order: [xmin, ymin, xmax, ymax]
'''
examples = [
	Detection("image_0002.jpg", [39, 63, 203, 112], [54, 66, 198, 114]),
	Detection("image_0016.jpg", [49, 75, 203, 125], [42, 78, 186, 126]),
	Detection("image_0075.jpg", [31, 69, 201, 125], [18, 63, 235, 135]),
	Detection("image_0090.jpg", [50, 72, 197, 121], [54, 72, 198, 120]),
	Detection("image_0120.jpg", [35, 51, 196, 110], [36, 60, 180, 108])]
'''

examples = [
	Detection("/home/igor/Documentos/Developments/Experiment_Plan/Renault_Oficial_Images/ad_blue_all_480p/bresil_ad_blue_0.png", [66, 353, 168, 450], [66, 353, 166, 448])]


# loop over the example detections
for detection in examples:
	# load the image
	image = cv2.imread(detection.image_path)

	# draw the ground-truth bounding box along with the predicted
	# bounding box
	cv2.rectangle(image, tuple(detection.gt[:2]),
		tuple(detection.gt[2:]), (0, 255, 0), 2)
	cv2.rectangle(image, tuple(detection.pred[:2]),
		tuple(detection.pred[2:]), (0, 0, 255), 2)

	# compute the intersection over union and display it
	iou = get_iou(detection.gt, detection.pred)
	cv2.putText(image, "IoU: {:.4f}".format(iou), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
	print("{}: {:.4f}".format(detection.image_path, iou))

	# show the output image
	cv2.imwrite('/home/igor/Documentos/Developments/Experiment_Plan/Renault_Oficial_Images/ad_blue_all_480p/teste.png', image)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
