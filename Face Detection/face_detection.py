#Description: This program detects faces, and eyes.

#import Open CV library
import cv2

#The Haar Classifiers stored as .xml files (Open CV's pretrained classifiers)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#Read in the img
img = cv2.imread('dwayne_and_james.jpg') # The image is transformed into a numpy array
faces = face_cascade.detectMultiScale(img, 1.3, 5) #returns the position of the detected faces as Rect(x,y,w,h), #face_cascade.detectMultiScale(img, scalefactor, minNeighbors)

# detectMultiScale(image, scalefactor, minNeighbors)
# scalefactor: In a group photo, there may be some faces which are near the camera than others. Naturally, such faces would appear more
#             prominent than the ones behind. This factor compensates for that.
# minNeighbors: This parameter specifies the number of neighbors a rectangle should have to be called a face.

# Print the number of faces found
print('Faces found: ', len(faces))

#Images which recorded in visible wavelengths contain 3 bands or  3 channels called RGB. NOTE: Open CV uses BGR
# R = red , G = green and B = blue. When overlapping these three bands,
# you can see an image in true color similar what people see.
print('The image height, width, and channel: ',img.shape) #Get the number of rows & cols AKA the height & width of the image 
print('The coordinates of each face detected: ', faces) #Print the coordinates of each face found

#loop over all the coordinates faces returned and draw rectangles around them using Open CV.
#We will be drawing a green rectangle with a thickness of 2
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2) # Draw rectangle around detected face(s) , #cv2.rectangle(img, pt1, pt2, color, thickness), NOTE: pt1 os upper left and pt2 is bottom right
    roi_face = img[y:y + h, x:x + w] #Get the pixel coordinates within the detected face border the region of interest (ROI), because eyes are located on the face
    eyes = eye_cascade.detectMultiScale(roi_face) #returns the position of the detected eyes
    for (ex, ey, ew, eh) in eyes: #loop over all the coordinates eyes returned and draw rectangles around them using Open CV.
        cv2.rectangle(roi_face, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2) #Draw reactangle around the eyes


#Add Text To The image
font = cv2.FONT_HERSHEY_SIMPLEX# Create the font to write on the image #normal size sans-serif font
text = cv2.putText(img, 'Face Detected', (0, img.shape[0]), font, 2, (255, 255, 255), 2)#Write text on the image #cv.PutText(img, text, org (bottom left corner of text), font, text size, color, thickness)

cv2.imshow('imgage',img) #Show the image
cv2.waitKey(0)# 0==wait forever, Its argument is the time in milliseconds
cv2.destroyAllWindows() # simply destroys all the windows we created.

#The images can be saved in the working directory as follows:
#cv2.imwrite('final_image.png',img)
