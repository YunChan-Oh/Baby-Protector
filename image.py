import cv2
def image1():
    vidcap = cv2.VideoCapture('raw/input3.mp4')
    ret, image = vidcap.read()
    image = cv2.resize(image, (960, 540))
    cv2.imwrite("output/image1.png",image)
print(image1())
