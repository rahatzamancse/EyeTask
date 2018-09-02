import numpy as np

import cv2

import dlib
from imutils import face_utils
from scipy.spatial import distance as dist


class BlinkDetector:
    def __init__(self):

        # define two constants, one for the eye aspect ratio to indicate
        # blink and then a second constant for the number of consecutive
        # frames the eye must be below the threshold
        self.EYE_AR_THRESH = 0.25
        self.EYE_AR_CONSEC_FRAMES = 6

        # initialize the frame counters and the total number of blinks
        self.BOTH_COUNTER = 0
        self.COUNTER_L = 0
        self.COUNTER_R = 0
        self.TOTAL = 0
        self.TOTAL_L = 0
        self.TOTAL_R = 0

        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print("BlinkDetector :[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("haar_cascades/shape_predictor_68_face_landmarks.dat")

        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def run_blink_detector(self, frame, eyeThresh):
        self.EYE_AR_THRESH = eyeThresh
        #print(eyeThresh)
        retDict = {"eyegaze": None,
                   "both": False,
                   "left": False,
                   "right": False,
				   "rightEAR": -1,
				   "leftEAR": -1}

        frame = cv2.resize(frame, (640, 450))
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = self.detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[self.rStart:self.rEnd]
            rightEye = shape[self.lStart:self.lEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # get the eye frame for the window

            eyegaze = frame[max(leftEye[1][1], 0):leftEye[5][1], max(leftEye[0][0], 0):leftEye[3][0]]
            eyegaze = cv2.resize(eyegaze, (0, 0), fx=8, fy=8)
            retDict["eyegaze"] = np.copy(eyegaze)

            # TODO: same for both

            retDict["leftEAR"] = round(leftEAR, 2)
            retDict["rightEAR"] = round(rightEAR, 2)
            # both
            if leftEAR < self.EYE_AR_THRESH - 0.02 and rightEAR < self.EYE_AR_THRESH - 0.02:
                self.BOTH_COUNTER += 1
            else:
                self.BOTH_COUNTER = 0
            # left
            if leftEAR < self.EYE_AR_THRESH:
                self.COUNTER_L += 1
            else:
                self.COUNTER_L = 0
            # right
            if rightEAR < self.EYE_AR_THRESH:
                self.COUNTER_R += 1
            else:
                self.COUNTER_R = 0

            # if the eyes were closed for a sufficient number of
            # then increment the total number of blinks
            if self.BOTH_COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                self.TOTAL += 1
                retDict["both"] = True
                self.COUNTER_R = 0
                self.COUNTER_L = 0
                self.BOTH_COUNTER = 0

            if self.COUNTER_L >= self.EYE_AR_CONSEC_FRAMES:
                self.TOTAL_L += 1
                retDict["left"] = True
                self.COUNTER_L = 0
                self.COUNTER_R = 0
                self.BOTH_COUNTER = 0

            if self.COUNTER_R >= self.EYE_AR_CONSEC_FRAMES:
                self.TOTAL_R += 1
                retDict["right"] = True
                self.COUNTER_L = 0
                self.COUNTER_R = 0
                self.BOTH_COUNTER = 0

            retDict["EAR_left"] = leftEAR
            retDict["EAR_right"] = rightEAR
            self.draw_in_frame(frame, leftEye, rightEye)

        cv2.flip(frame, 0)
        retDict["bothTotal"] = self.TOTAL
        retDict["leftTotal"] = self.TOTAL_L
        retDict["rightTotal"] = self.TOTAL_R
        retDict["image"] = frame
        return retDict

    def draw_in_frame(self, frame, leftEye, rightEye):
        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)

        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

    def reset(self):
        self.BOTH_COUNTER = 0
        self.COUNTER_L = 0
        self.COUNTER_R = 0
        self.TOTAL = 0
        self.TOTAL_L = 0
        self.TOTAL_R = 0


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
