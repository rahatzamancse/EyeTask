import cv2
import numpy as np


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haar_cascades/face.xml')
        self.init = [0, 0]
        self.coordinate = [0, 0]
        self.dir_c = 0
        self.dir_l = 0
        self.dir_r = 0
        self.dir_u = 0
        self.dir_d = 0
        self.conf = 5
        self.rad = 20

    def get_processed_image(self, img):
        ret = {"direction": "NaN", "face": None}
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)
        cv2.circle(img, (self.init[0], self.init[1]), 3, (0, 255, 0), -1)
        cv2.line(img, (self.init[0], self.init[1]), (self.coordinate[0], self.coordinate[1]), (0, 255, 0), 2)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            self.coordinate = [int(x + w / 2), int(y + h / 2)]
            ret["face"] = self.coordinate
            # print("-----")
            # print("initial = " + str(self.init))
            # print("current = " + str(coordinate))
            dir = self.direction(self.init, self.coordinate)
            # print("direction = " + dir)
            # angle = self.getangle(self.init, coordinate)
            # print("angle = " + angle)

            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfTextr = (200, 250)
            bottomLeftCornerOfTextc = (80, 250)
            bottomLeftCornerOfTextl = (20, 250)
            fontScale = 1
            fontColor = (255, 255, 255)
            lineType = 2

            if dir == "center":
                self.dir_c += 1
                if self.dir_c >= self.conf:
                    self.dir_l = 0
                    self.dir_r = 0
                    self.dir_u = 0
                    self.dir_d = 0
                    if self.dir_c%self.conf == 0:
                        ret["direction"] = dir
                    img = cv2.putText(img, '< Center >',
                                      bottomLeftCornerOfTextc,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)
            elif dir == "right":
                self.dir_r += 1
                if self.dir_r > self.conf:
                    self.dir_l = 0
                    self.dir_c = 0
                    self.dir_u = 0
                    self.dir_d = 0
                    if self.dir_r%self.conf == 0:
                        ret["direction"] = dir
                    img = cv2.putText(img, 'Right >',
                                      bottomLeftCornerOfTextr,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)

            elif dir == "left":
                self.dir_l += 1
                if self.dir_l > self.conf:
                    self.dir_c = 0
                    self.dir_r = 0
                    self.dir_u = 0
                    self.dir_d = 0
                    if self.dir_l%self.conf == 0:
                        ret["direction"] = dir
                    img = cv2.putText(img, '< left',
                                      bottomLeftCornerOfTextl,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)

            elif dir == "up":
                self.dir_u += 1
                if self.dir_u > self.conf:
                    self.dir_l = 0
                    self.dir_r = 0
                    self.dir_c = 0
                    self.dir_d = 0
                    if self.dir_u%self.conf == 0:
                        ret["direction"] = dir
                    img = cv2.putText(img, '< Up >',
                                      bottomLeftCornerOfTextc,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)

            elif dir == "down":
                self.dir_d += 1
                if self.dir_d > self.conf:
                    self.dir_l = 0
                    self.dir_r = 0
                    self.dir_c = 0
                    self.dir_d = 0
                    if self.dir_d%self.conf == 0:
                        ret["direction"] = dir
                    img = cv2.putText(img, '< Down >',
                                      bottomLeftCornerOfTextc,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)

        cv2.imshow('img', img)
        return ret

    def direction(self, ini, cur, flag=1):
        ix = ini[0]
        iy = ini[1]
        cx = cur[0]
        cy = cur[1]
        if self.init == [0, 0]:
            return "not initialized"
        elif ix + self.rad >= cx >= ix - self.rad:
            if flag == 0:
                return "center"
            elif flag == 1 and cy >= iy + self.rad:
                return "down"
            elif flag == 1 and cy <= iy - self.rad:
                return "up"
            else:
                return "center"

        elif cx >= ix + self.rad:
            return "right"
        elif cx <= ix - self.rad:
            return "left"

    def getangle(self, ini, cur):
        ix = ini[0]
        iy = ini[1]
        cx = cur[0]
        cy = cur[1]
        a = np.array([cx, cy])
        b = np.array([ix, iy])
        c = np.array([1000, iy])
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return str(np.degrees(angle))

    def initPos(self, face):
        self.init = face
