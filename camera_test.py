import cv2
import face_recognition

print("Starting Camera... Look at the lens!")

# open the webcam (0 is usually the default camera)
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not access the camera")
else:
    print("Camera is ON. 'q' to quit")
    
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    # Find all the faces in the current frame
    
    face_locations = face_recognition.face_locations(frame)

    # Draw a box around the face
    for top,right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
    cv2.imshow('Face Scanner', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()


    