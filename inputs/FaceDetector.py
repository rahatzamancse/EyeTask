import cv2
import numpy as np


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('inputs/face.xml')
        self.init = [0, 0]
        self.coordinate = [0, 0]
        self.dir_c = 0
        self.dir_l = 0
        self.dir_r = 0
        self.dir_u = 0
        self.dir_d = 0
        self.conf = 5
        self.rad = 20

        self.face = None

    def processImage(self, img, drawImg):
        ret = {
            "direction": "NaN"
        }
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)

        cv2.circle(drawImg, (self.init[0], self.init[1]), 3, (0, 255, 0), 2)
        cv2.line(drawImg, (self.init[0], self.init[1]), (self.coordinate[0], self.coordinate[1]), (0, 255, 0), 2)

        for (x, y, w, h) in faces:
            self.coordinate = [int(x + w / 2), int(y + h / 2)]
            self.face = self.coordinate
            dir = self.direction(self.init, self.coordinate)

            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfTextr = (200, 250)
            bottomLeftCornerOfTextc = (80, 250)
            bottomLeftCornerOfTextl = (20, 250)
            fontScale = 1
            fontColor = (255, 255, 255)
            lineType = 2

            if dir == "headcenter":
                self.dir_c += 1
                if self.dir_c >= self.conf:
                    self.dir_l = 0
                    self.dir_r = 0
                    self.dir_u = 0
                    self.dir_d = 0
                    if self.dir_c%self.conf == 0:
                        ret["direction"] = dir

                    drawImg = cv2.putText(drawImg, '< Center >',
                                      bottomLeftCornerOfTextc,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)
            elif dir == "headright":
                self.dir_r += 1
                if self.dir_r > self.conf:
                    self.dir_l = 0
                    self.dir_c = 0
                    self.dir_u = 0
                    self.dir_d = 0
                    if self.dir_r%self.conf == 0:
                        ret["direction"] = dir

                    drawImg = cv2.putText(drawImg, 'Right >',
                                      bottomLeftCornerOfTextr,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)

            elif dir == "headleft":
                self.dir_l += 1
                if self.dir_l > self.conf:
                    self.dir_c = 0
                    self.dir_r = 0
                    self.dir_u = 0
                    self.dir_d = 0
                    if self.dir_l%self.conf == 0:
                        ret["direction"] = dir

                    drawImg = cv2.putText(drawImg, '< left',
                                      bottomLeftCornerOfTextl,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)

            elif dir == "headup":
                self.dir_u += 1
                if self.dir_u > self.conf:
                    self.dir_l = 0
                    self.dir_r = 0
                    self.dir_c = 0
                    self.dir_d = 0
                    if self.dir_u%self.conf == 0:
                        ret["direction"] = dir

                    drawImg = cv2.putText(drawImg, '< Up >',
                                      bottomLeftCornerOfTextc,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)

            elif dir == "headdown":
                self.dir_d += 1
                if self.dir_d > self.conf:
                    self.dir_l = 0
                    self.dir_r = 0
                    self.dir_c = 0
                    self.dir_d = 0
                    if self.dir_d%self.conf == 0:
                        ret["direction"] = dir

                    drawImg = cv2.putText(drawImg, '< Down >',
                                      bottomLeftCornerOfTextc,
                                      font,
                                      fontScale,
                                      fontColor,
                                      lineType)
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
                return "headcenter"
            elif flag == 1 and cy >= iy + self.rad:
                return "headdown"
            elif flag == 1 and cy <= iy - self.rad:
                return "headup"
            else:
                return "headcenter"

        elif cx >= ix + self.rad:
            return "headright"
        elif cx <= ix - self.rad:
            return "headleft"

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

    def initPos(self):
        self.init = self.face
