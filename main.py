import cv2
import time
import glob
from emailing import send_email

"""
    VideoCapture(0)
    0 is used for the main camera of the laptop/PC.
    1 is used for the second integrated/USB attached camera 
"""
video = cv2.VideoCapture(0)

# Give time for the camera to load, to prevent the black frames
time.sleep(1)

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    # Compare first frame with the current frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # To classify the delta_frame pixels
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # Dilate the frame
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Show the frame
    # cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            # if < 6000 pixels, there is no object in front of the camera
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        # Extract image from webcam video
        all_images = sorted(glob.glob("images/*.png"))
        index = int(len(all_images) / 2)
        image_with_object = all_images[index]
        print(f"image with object: {index}.png")

        send_email()

    cv2.imshow("Video - bounded frame", frame)

    # User pressed the "q" key on keyboard to stop the video from camera
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
