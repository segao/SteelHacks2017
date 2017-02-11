import cv2
import sys
import numpy as np
import math
import requests
import MySQLdb
from twilio.rest import TwilioRestClient


cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

template_rgb = cv2.imread('BotLeft.png')
template_tr_rgb = cv2.imread('TopRight.png')

template = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
template2 = cv2.cvtColor(template_tr_rgb, cv2.COLOR_BGR2GRAY)

# TWILIO
account_sid = "AC1c007bdeea710ba5b96c8bd84333346c"
auth_token = "093ef53346af1ea86165ab21fd07d997"
client = TwilioRestClient(account_sid, auth_token)


db = MySQLdb.connect("35.165.180.48","david","david123","babydata")
cursor = db.cursor()

w, h = template.shape[::-1]
w2, h2 = template2.shape[::-1]

isBabySafe = True


# hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

video_capture = cv2.VideoCapture(0)


def isInBounds(blb, trb, bls, trs, extendby):

    new_blbx = blb[0] - extendby
    new_blby = blb[1] - extendby

    new_trbx = trb[0] + extendby
    new_trby = trb[1] + extendby

    new_blb = (new_blbx, new_blby)
    new_trb = (new_trbx, new_trby)

    #far off left, far off bottom, far off top, far off right
    if(bls[0] < new_blb[0] or bls[1] > new_blb[1] or trs[0] > new_trb[0] or trs[1] < new_trb[1]):
        return False
    return True


def detect_isSafe(botLeft, topRight, faces, isBabySafe):
    count_faces = len(faces)
    count_NotInBounds = 0

    safe_color = (0, 255, 255)
    danger_color = (0, 0, 255)

    for x, y, w, h in faces:
        pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        facePt1 = (x + pad_w, y + pad_h)
        facePt2 = (x + w - pad_w, y + h - pad_h)
        # print botLeft, topRight, facePt1, facePt2
        if not isInBounds(botLeft, topRight, facePt1, facePt2, 10):
            count_NotInBounds += 1

    if count_NotInBounds == count_faces:
        # message = client.messages.create(to="+16105055536", from_="+14848044280", body="BABY IS IN DANGER!")
        # Post that baby is in danger
        if isBabySafe is True:
            # client.messages.create(to="+16105055536", from_="+14848044280", body="BABY IS IN DANGER!")
            isBabySafe = False
            # Has not been updated
            executeSQL(1)
        return (danger_color, isBabySafe)

    if isBabySafe is False:
        # client.messages.create(to="+16105055536", from_="+14848044280", body="nvm you good")
        isBabySafe = True
        executeSQL(2)

    return (safe_color, isBabySafe)


def executeSQL(value):
    sql = "UPDATE `babycheck` SET `babyCheck` = '1' WHERE `babycheck`.`babyID` = " + str(value)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()


def draw_detections(img, rects, thickness=1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)

def average(tuple_array):
    sum_x = 0
    sum_y = 0
    n = len(tuple_array)
    if n == 0:
        return (float('nan'),float('nan'))
    for pt in tuple_array:
        sum_x += pt[0]
        sum_y += pt[1]

    return (sum_y/n, sum_x/n)



iteration = 0
prev_pt1 = (0, 0)
prev_pt2 = (0, 0)

while True:
    iteration = iteration + 1

    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(gray, template2, cv2.TM_CCOEFF_NORMED)

    threshold = 0.9
    threshold2 = 0.6

    loc = np.where(res >= threshold)
    loc2 = np.where(res2 >= threshold2)

    avg_point1 = np.mean(loc, axis=1)

    loc2_points = zip(*loc2[::-1])
    loc2_valid_points = []
    for pt in loc2_points:
        if pt[0] > avg_point1[0]:
            loc2_valid_points.append(pt)


    # for pt2 in loc2_valid_points:
    #     cv2.rectangle(frame, pt2, (pt2[0] + w, pt2[1] + h), (255,0,255), 2)

    avg_point2 = average(loc2_valid_points)

    # for pt in zip(*loc[::-1]):
    #      cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

    # for pt2 in zip(*loc2[::-1]):
    #      if pt2[0] > avg_point1[0] and pt2[1] < avg_point1[1]
    #      cv2.rectangle(frame, pt2, (pt2[0] + w, pt2[1] + h), (255,0,255), 2)
    # print loc2[:,0] > avg_point1[0]
    # loc2 = loc2[(loc2[:,0] > avg_point1[0])[0]]

    if math.isnan(avg_point1[1]) or math.isnan(avg_point1[0]):
        avg_point1 = prev_pt1
    else:
        prev_pt1 = avg_point1

    if math.isnan(avg_point2[1]) or math.isnan(avg_point2[0]):
        avg_point2 = prev_pt2
    else:
        prev_pt2 = avg_point2

    point1 = (int(avg_point1[1]) + h/2, int(avg_point1[0]) + w/2)
    point2 = (int(avg_point2[1]) + h2/2, int(avg_point2[0]) + w2/2)

    cv2.circle(frame, point2, 10, (0, 255, 255))
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    # found,w=hog.detectMultiScale(gray, winStride=(8,8), padding=(32,32), scale=1.05)

    draw_detections(frame, faces)

    [color, isBabySafe] = detect_isSafe(point1, point2, faces, isBabySafe)
    cv2.rectangle(frame, point2, point1, color, 2)

    cv2.imshow('Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

