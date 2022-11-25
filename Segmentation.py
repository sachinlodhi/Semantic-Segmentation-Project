
from PIL import Image, ImageOps
import numpy as np
import random
import cv2
import matplotlib.pyplot as plt
from keras.models import load_model
# Loading the model
model = load_model("model/HME_SEm_Seg_704_704.hdf5",  compile=False)
def draw_bbox(seg_path):
    # img = Image.open(seg_path)
    img = cv2.imread(seg_path,0)
    print(img.shape)

    result = img.copy()
    contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for cntr in contours:
        print(cntr)
        x, y, w, h = cv2.boundingRect(cntr)
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print("x,y,w,h:", x, y, w, h)
    cv2.imwrite("/home/sachin/PycharmProjects/flaskProject/static/segmented/bounding_box/bbox.jpeg", result)


def segment(image_path):
    image = Image.open(image_path)
    image = ImageOps.grayscale(image)
    resized = image.resize((704,704))
    resized.save("static/resized/resized_img.jpg")
    test_img = cv2.imread("static/resized/resized_img.jpg")
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)/255 # need to divide input image by 255 as the model is trained on the pixels between(0 and 1)
    test_img = np.expand_dims(test_img, axis=[0,3]) #Adding dimension
    prediction = (model.predict(test_img)[0,:,:,0]> 0.5).astype(np.uint8)
    # print(prediction.shape)
    img = Image.fromarray((prediction*255).astype(np.uint8)) # multiplying by 2 otherwise they would look black
    # img.show()
    segmented_img_path = r"static/segmented/pred.jpg"
    img.save(segmented_img_path)
    # draw_bbox(segmented_img_path)
    return segmented_img_path


# if __name__ == '__main__':
#     draw_bbox("/home/sachin/PycharmProjects/flaskProject/static/segmented/pred.jpg")