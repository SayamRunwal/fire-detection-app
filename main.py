from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class FireApp(App):
    def build(self):
        self.img = Image()
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS
        return self.img

    def detect_fire(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_fire = np.array([0, 100, 100])
        upper_fire = np.array([10, 255, 255])
        fire_mask = cv2.inRange(hsv_frame, lower_fire, upper_fire)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_DILATE, kernel)
        return fire_mask

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        fire_mask = self.detect_fire(frame)
        contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

        # Convert frame to texture
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    FireApp().run()
