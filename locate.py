import json
import os
import time
import numpy as np
import matplotlib.pyplot as plt


def horizontalCut(img):
    (x, y) = img.shape
    pointCount = np.zeros(x, dtype=np.uint8)
    for i in range(0, x):
        for j in range(0, y):
            if (img[i, j] == 0):
                pointCount[i] = pointCount[i] + 1

    # plt.plot(range(x),pointCount)
    # plt.show()
    start = 0
    end = x-1
    # 对照片进行分割
    keyvalue = 2
    while pointCount[start] < keyvalue:
        start += 1
        if start >= x:
            break
    while pointCount[end] < keyvalue:
        end -= 1
        if end < 0:
            break

    success = False
    if start < end:
        img = img[start:end, :]
        success = True
    return img, success


def verticalCut(img):
    (x, y) = img.shape
    pointCount = np.zeros(y, dtype=np.uint8)
    for i in range(0, x):
        for j in range(0, y):
            if (img[i, j] == 0):
                pointCount[j] = pointCount[j] + 1

    # plt.plot(range(y),pointCount)
    # plt.show()
    imgArr = []
    pos = []
    # 对照片进行分割
    flag = False
    mark = 0
    keyvalue = 2
    for index in range(0, y):
        if not flag:
            if pointCount[index] > keyvalue:
                flag = True
                mark = index
        else:
            if pointCount[index] <= keyvalue:
                flag = False
                imgArr.append(img[:, mark:index])
                if mark*2 >= y:
                    pos.append('r')
                else:
                    pos.append('l')
    if flag:
        imgArr.append(img[:, mark:index])
        if mark*2 >= y:
            pos.append('r')
        else:
            pos.append('l')

    return imgArr, pos


class locater:
    pos: dict

    def __init__(self):
        file = open('./configue.json')
        pos = json.load(file)
        file.close()

        self.question = (int(pos['width']*pos['question_left']),
                         int(pos['width']*pos['question_right']),
                         int(pos['height']*pos['question_top']),
                         int(pos['height']*pos['question_bottom']))
        input_y = pos['height']*pos['input_top']
        input_x = pos['width']*pos['input_left']
        input_h = pos['height']*(pos['input_bottom']-pos['input_top'])
        input_w = pos['width']*(pos['input_right']-pos['input_left'])

        self.left = (
            (int(input_y+input_h*0.4), int(input_x+input_w*0.4)),
            (int(input_y+input_h*0.5), int(input_x+input_w*0.6)),
            (int(input_y+input_h*0.6), int(input_x+input_w*0.4))
        )

        self.right = (
            (int(input_y+input_h*0.4), int(input_x+input_w*0.6)),
            (int(input_y+input_h*0.5), int(input_x+input_w*0.4)),
            (int(input_y+input_h*0.6), int(input_x+input_w*0.6))
        )

        self.next = (
            (int(pos['height']*pos['next1_top']),
             int(pos['width']*pos['next1_left'])),
            (int(pos['height']*pos['next2_top']),
             int(pos['width']*pos['next2_left'])),
            (int(pos['height']*pos['next3_top']),
             int(pos['width']*pos['next3_left']))
        )

    def sim_left(self):
        time = 10
        cmd = f'adb shell input swipe {self.left[0][1]} {self.left[0][0]} {self.left[1][1]} {self.left[1][0]} {time}'
        print('command:', cmd)
        os.system(cmd)
        cmd = f'adb shell input swipe {self.left[1][1]} {self.left[1][0]} {self.left[2][1]} {self.left[2][0]} {time}'
        print('command:', cmd)
        os.system(cmd)

    def sim_right(self):
        time = 10
        cmd = f'adb shell input swipe {self.right[0][1]} {self.right[0][0]} {self.right[1][1]} {self.right[1][0]} {time}'
        print('command:', cmd)
        os.system(cmd)
        cmd = f'adb shell input swipe {self.right[1][1]} {self.right[1][0]} {self.right[2][1]} {self.right[2][0]} {time}'
        print('command:', cmd)
        os.system(cmd)

    def click_next(self):
        time.sleep(6)
        cmd = f'adb shell input tap {self.next[0][1]} {self.next[0][0]}'
        os.system(cmd)
        print('command:', cmd)
        time.sleep(1)
        cmd = f'adb shell input tap {self.next[1][1]} {self.next[1][0]}'
        os.system(cmd)
        print('command:', cmd)
        time.sleep(1)
        cmd = f'adb shell input tap {self.next[2][1]} {self.next[2][0]}'
        os.system(cmd)
        print('command:', cmd)
        time.sleep(2)
