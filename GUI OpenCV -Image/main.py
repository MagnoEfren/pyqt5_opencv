# Magno Efren - 2022
# https://www.youtube.com/c/MagnoEfren/videos

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi 
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPixmap
import imutils
import cv2
import sys

class MyApp(QMainWindow):
	def __init__(self):
		super(MyApp, self).__init__()
		loadUi('design.ui', self)

		self.open_image.clicked.connect(self.load_image)
		self.save_image.clicked.connect(self.save_image_final)
		self.reset_edit.clicked.connect(self.reset_image)

		self.slider_one.valueChanged['int'].connect(self.tonality)
		self.slider_two.valueChanged['int'].connect(self.saturation)
		self.slider_three.valueChanged['int'].connect(self.brightness)
		self.slider_four.valueChanged['int'].connect(self.gray_scale)
		self.filename = str()

	def load_image(self):
		self.filename = QFileDialog.getOpenFileName(
			filter="Image JPG(*.jpg);;Image PNG(*.png)")[0]
		if len(self.filename)!=0:
			self.image = cv2.imread(self.filename)
			self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)	
			image = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2RGB)	
			self.set_image(image)
	def set_image(self,image):
		if len(self.filename)!=0:
			self.image_final = image
			frame = imutils.resize(image, width=500, height=500)
			image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
			self.label_image.setPixmap(QPixmap.fromImage(image))	
	def tonality(self,value):
		if len(self.filename)!=0:
			h,s,v = cv2.split(self.hsv)
			r = 180 - value
			h[h>r] = 180
			h[h<=r] += value		
			hsv_final = cv2.merge((h,s,v))
			img = cv2.cvtColor(hsv_final,cv2.COLOR_HSV2RGB)
			self.set_image(img)		
	def saturation(self,value):
		if len(self.filename)!=0:	
			h,s,v = cv2.split(self.hsv)
			r = 255 - value
			s[s>r] = 255
			s[s<=r] += value
			hsv_final = cv2.merge((h,s,v))
			img = cv2.cvtColor(hsv_final,cv2.COLOR_HSV2RGB)
			self.set_image(img)
	def brightness(self, value):
		if len(self.filename)!=0:
			h,s,v = cv2.split(self.hsv)
			r = 255 - value
			v[v>r] = 255
			v[v<=r] += value		
			hsv_final = cv2.merge((h,s,v))
			img = cv2.cvtColor(hsv_final,cv2.COLOR_HSV2RGB)
			self.set_image(img)
	def gray_scale(self, value):
		if len(self.filename)!=0:
			gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
			r = 255 - value
			gray[gray>r] = 255
			gray[gray<=r] += value
			img = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
			self.set_image(img)
	def save_image_final(self):
		if len(self.filename)!=0:		
			filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")[0]
			cv2.imwrite(filename, self.image_final)
	def reset_image(self):
		if len(self.filename)!=0:		
			self.slider_one.setValue(0)
			self.slider_two.setValue(0)
			self.slider_three.setValue(0)
			self.slider_four.setValue(0)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	my_app = MyApp()
	my_app.show()
	sys.exit(app.exec_())
