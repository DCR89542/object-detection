import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

yolo = cv2.dnn.readNet("./yolov3-tiny.weights", "./yolov3-tiny.cfg")

classes = []
with open("./coco.names", 'r') as f:
	classes = f.read().splitlines()

img_path = "../uploads/" + sys.argv[1];
img = cv2.imread(img_path)

blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), (0,0,0), swapRB = True, crop = False)

#i = blob[0].reshape((320, 320, 3))
#plt.imshow(i)
#plt.show()

yolo.setInput(blob)
output_layer_name = yolo.getUnconnectedOutLayersNames()
layeroutput = yolo.forward(output_layer_name)

boxes = []
confidences = []
class_ids = []

#print(img.shape)
width = img.shape[1]
height = img.shape[0]

for output in layeroutput:
	for detection in output:
		score = detection[5:]
		class_id = np.argmax(score)
		confidence = score[class_id]
		if confidence > 0.7:
			#print(detection[0:5])
			center_x = int(detection[0]*width)
			center_y = int(detection[1]*height)
			w = int(detection[2]*width)
			h = int(detection[3]*height)
			
			#print(center_x, center_y, w, h)
			
			x = int(center_x - w/2)
			y = int(center_y - h/2)
			
			boxes.append([x,y,w,h])
			confidences.append(float(confidence))
			class_ids.append(class_id)

#print(len(boxes))
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

#print(indices)

font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size = (len(boxes), 3))

for i in indices.flatten():
	x,y,w,h = boxes[i]
	
	label = str(classes[class_ids[i]])
	
	confi = str(round(confidences[i], 2))
	color = colors[i]
	
	cv2.rectangle(img, (x,y),(x+w, y+h), color, 2)
	cv2.putText(img, label+" "+confi, (x, y+20), font, 2, (0, 0, 0), 1)
	
cv2.imwrite("../outputs/out.jpg", img)
#plt.imshow(img)
#plt.show()