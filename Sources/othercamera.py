import cv2

class Camera(cv2.VideoCapture):
    def __init__(self, pipeEnd, Alive):
        super().__init__("http://212.60.62.51:8080/mjpg/video.mjpg?timestamp=1604220864235")
        self.pipe = pipeEnd
        self.Alive = Alive
        self.loop()

    def loop(self):
        while self.Alive:
            ret, img = self.read()
            if ret:
                self.pipe.send(img)