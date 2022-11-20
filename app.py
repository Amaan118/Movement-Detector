# To detect the motion
import cv2

# To make app resizing and stuff
import imutils

# To make app fast using multiple threads
import threading

# To make noise when motion is detected
import winsound

# To send mails
from sendMail import sendMail


# Number of cameras we want to capture (Put 0 for 1 camera)
capture_count = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Define window size
capture_count.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture_count.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Start the capturing
_, start_frame = capture_count.read()

start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)


# Initially set the alarm to false
alarm = False
alarm_mode = False
alarm_counter = 0


# This function will trigger the alarm
def trigger_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("Alarm Triggered !!!")
        winsound.Beep(4000, 1000)

    alarm = False
    sendMail(['2019bcs118@sggs.ac.in'])


while True:
    _, frame = capture_count.read()

    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        # Color the background
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        start_frame = frame_bw

        # Set a threshold if crossed will raise an alarm
        if threshold.sum() > 100:
            alarm_counter += 1
        else:
            if alarm_counter:
                alarm_counter -= 1

        # Display the image
        cv2.imshow("Cam", threshold)

    else:
        cv2.imshow("Cam", frame)

    # If the alarm_counter reaches a certain limit then fire the Trigger
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=trigger_alarm).start()

    # Start the alarm is user presses s and stop it after he presses q
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("s") or key_pressed == ord("S"):
        alarm_mode = not alarm_mode
        alarm_counter = 0

    if key_pressed == ord("q") or key_pressed == ord("Q"):
        alarm_mode = False
        break

# Release all the resources and delete the windows
capture_count.release()
cv2.destroyAllWindows()
