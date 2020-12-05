# face detection with mtcnn on a photograph. this code is to identify lips portion in face and fetch color of it. Then verify the selected lipstick color is matched with lips color after the lipstick has been applied.
import re
import time

import cv2
import pyautogui
from PIL import Image
from matplotlib import pyplot
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from mtcnn.mtcnn import MTCNN


# draw an image with detected objects
def draw_image_with_boxes(filename, result_list, inputColor):
    # load the image
    data = pyplot.imread(filename)
    # plot the image
    pyplot.imshow(data)
    # get the context for drawing boxes
    ax = pyplot.gca()
    count = 0
    pyplot.show(block=False)
    # plot each box
    for result in result_list:
        # get coordinates
        x, y, width, height = result['box']
        # create the shape
        rect = Rectangle((x, y), width, height, fill=False, color='red')
        # draw the box
        ax.add_patch(rect)
        lip_point_x = []
        lip_point_y = []
        # draw the dots
        for key, value in result['keypoints'].items():
            # create and draw dot
            print(key)
            if (key == "mouth_left" or key == "mouth_right"):
                count = count + 1
                lip_point_x.append(value[0])
                lip_point_y.append(value[1])
                # print("lip,start point",lip_start_point_x)
                if (count == 2):
                    print("wow!!!")
                dot = Circle(value, radius=5, color='red')
                ax.add_patch(dot)
            # print(value)
            print(count)

        print(lip_point_x)
        print(lip_point_y)
        i = lip_point_x[0]
        print("starting X co-ordinate", i)
        j = lip_point_y[0]
        print("starting Y co-ordinate", j)
        red_image = Image.open(filename)
        red_image_rgb = red_image.convert("RGB")
        temp = re.findall(r'\d+', inputColor)
        rgb_pixel_value_chosen_color = list(map(int, temp))
        print("input color array is ", rgb_pixel_value_chosen_color)

        # rgb_pixel_value_chosen_color = red_image_rgb.getpixel((1210, 476))
        print("Chosen color RGB", rgb_pixel_value_chosen_color)
        r_value = 0
        g_value = 0
        b_value = 0
        if (j <= lip_point_y[1]):
            while (j <= lip_point_y[1]):
                while (i <= lip_point_x[1]):
                    rgb_pixel_value_on_face = red_image_rgb.getpixel((i, j))
                    print(i, j)
                    print("RGB color", rgb_pixel_value_on_face)
                    if (rgb_pixel_value_on_face[0] <= rgb_pixel_value_chosen_color[0] + 20 and rgb_pixel_value_on_face[
                        0] >= rgb_pixel_value_chosen_color[0] - 20):
                        r_value = 1
                        if (rgb_pixel_value_on_face[1] <= rgb_pixel_value_chosen_color[1] + 22 and
                                rgb_pixel_value_on_face[1] >= rgb_pixel_value_chosen_color[1] - 22):
                            g_value = 1
                            if (rgb_pixel_value_on_face[2] <= rgb_pixel_value_chosen_color[2] + 30 and
                                    rgb_pixel_value_on_face[2] >= rgb_pixel_value_chosen_color[2] - 30):
                                b_value = 1

                    i = i + 1
                j = j + 1
        else:
            while (j >= lip_point_y[1]):
                while (i <= lip_point_x[1]):
                    rgb_pixel_value_on_face = red_image_rgb.getpixel((i, j))
                    print(i, j)
                    print("RGB color", rgb_pixel_value_on_face)
                    if (rgb_pixel_value_on_face[0] <= rgb_pixel_value_chosen_color[0] + 20 and
                            rgb_pixel_value_on_face[0] >= rgb_pixel_value_chosen_color[0] - 20):
                        r_value = 1
                        if (rgb_pixel_value_on_face[1] <= rgb_pixel_value_chosen_color[1] + 22 and
                                rgb_pixel_value_on_face[1] >= rgb_pixel_value_chosen_color[1] - 22):
                            g_value = 1
                            if (rgb_pixel_value_on_face[2] <= rgb_pixel_value_chosen_color[2] + 30 and
                                    rgb_pixel_value_on_face[2] >= rgb_pixel_value_chosen_color[2] - 30):
                                b_value = 1

                    i = i + 1
                j = j - 1

        if (r_value == 1 and g_value == 1 and b_value == 1):
            print("Selected color has been applied to lips successfully")
        else:
            print("Selected color has not been applied to lips")

    # show the plot
    pyplot.show()
    # pyplot.show(block=False)
    time.sleep(10)
    pyplot.close('all')
    driver.quit()


# _________________________________________________________________________________________________________________________
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("prefs", { \
    # "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    # "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options=options,
                          executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.maccosmetics.com/product/13854/60284/products/makeup/lips/lipstick/powder-kiss-lipstick#/')

driver.implicitly_wait(20)
inputElement = driver.find_element_by_xpath("(//div[@class='product-full__shade-swatch'])[6]")
inputElement.click()
time.sleep(10)
selected_color = inputElement.value_of_css_property('background-color')
print("Selected color RGB", selected_color)
driver.implicitly_wait(10)
inputElement = driver.find_element_by_xpath("//div[@class='product-smart-gift__content']")
a = ActionChains(driver)
a.move_to_element(inputElement).perform()
driver.implicitly_wait(2)

inputElement = driver.find_element_by_xpath(
    "//a[@class='js-youcambtn product-vto__btn button cta-vto jquery-once-1-processed']")
driver.implicitly_wait(10)
inputElement.click()

iframe = driver.find_element_by_id("YMK-module-iframe")
driver.switch_to_frame(iframe)

inputElement = driver.find_element_by_xpath("//div[@class='frame-content']")
if (inputElement.is_displayed()):
    inputElement = driver.find_element_by_xpath("//div[contains(text(),'LIVE CAMERA')]")
    inputElement.click()
    # Verify Camera is enabled
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    else:
        print("Webcam is opened")
        time.sleep(30)
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('TryitOn.jpg')

# _____________________________________________________________________________________________________________________________

filename = 'TryitOn.jpg'
# load image from file
pixels = pyplot.imread(filename)
# create the detector, using default weights
detector = MTCNN()
# detect faces in the image
faces = detector.detect_faces(pixels)
# display faces on the original image
draw_image_with_boxes(filename, faces, selected_color)
