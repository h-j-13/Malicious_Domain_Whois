# -*- coding: UTF-8 -*-
from selenium import webdriver
from pyvirtualdisplay import Display
import Image
from time import sleep


# with Display(backend="xvfb", size=(1440, 900)):		
driver = webdriver.Chrome()
driver.get('http://index.baidu.com/?tpl=trend&word=%B0%C4%C3%C5')
sleep(5)
driver.save_screenshot('screenshot_1.png')
driver.quit()
left = element.location['x']
top = element.location['y']
right = element.location['x'] + element.size['width']
bottom = element.location['y'] + element.size['height']

im = Image.open('screenshot.png')
im = im.crop((left, top, right, bottom))
im.save('screenshot.png')

print left
print top
print right
print bottom