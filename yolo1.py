import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

#yolo = cv2.dnn.readNet("./yolov3-tiny.weights", "./darknet-master/darknet-master/cfg/yolov3-tiny.cfg")
yolo = cv2.dnn.readNet("./yolov3.weights", "./darknet-master/cfg/yolov3.cfg")

classes = []

with open("./coco.names", 'r') as f:
	classes = f.read().splitlines()

img = cv2.imread("./image/maxresultdefault.jpg")

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
	print(label+" "+confi)
	
	cv2.rectangle(img, (x,y),(x+w, y+h), color, 2)
	cv2.putText(img, label+" "+confi, (x, y+20), font, 1, (57, 255, 20), 2)
    
#"C:\Users\Deep\Desktop\object_detectionn\output image"	
#path = 'C:/Users/Deep/Desktop/object_detectionn/output_image'
#cv2.imwrite(os.path.join(path , 'waka.jpg'),img)

cv2.imwrite('C:/Users/Deep/Desktop/object_detectionn/output_image/Image.jpg', img)
cv2.waitKey(0)

plt.imshow(img)
plt.show()