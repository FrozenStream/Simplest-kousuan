import subprocess
import numpy as np
import cv2
import time
import os
from locate import *
from cal import *


os.system('adb kill-server')
os.system('adb connect 127.0.0.1:16384')
locate = locater()
cal = caler()
rect = locate.question


for epoch in range(100):
    old_l, old_r = 0, 0
    question_num = 0
    wrong = 0
    st = time.time()
    while question_num < 10:
        print('detecting image...')
        process = subprocess.Popen(
            ['adb', 'shell', 'screencap', '-p'],
            stdout=subprocess.PIPE
        )
        output = process.communicate()[0].replace(b'\r\n', b'\n')

        img = cv2.imdecode(np.frombuffer(output, dtype=np.uint8), cv2.IMREAD_COLOR)
        qes = cv2.cvtColor(img[rect[2]:rect[3], rect[0]:rect[1]], cv2.COLOR_BGR2GRAY)
        ret, qes = cv2.threshold(qes, 170, 255, cv2.THRESH_BINARY)
        # cv2.imwrite('qes.png', qes)
        # cv2.imwrite('img.png', img)

        cuted_img, success = horizontalCut(qes)
        if not success:
            print('horizontal target failed.')
            continue
        cv2.imwrite('./horizontalCut.png',cuted_img)
        imgarr, pos = verticalCut(cuted_img)
        if len(imgarr) == 0:
            print('vertical target failed.')
            continue

        ans = [cal.cal_sim(img) for img in imgarr]

        l, r = 0, 0
        flag = False
        success = True
        cnt = 0
        for i in range(len(ans)):
            if ans[i] == '?':
                cnt += 1
                if cnt > 1:
                    success = False
                if i == 0 or i == len(ans)-1:
                    success = False
                if success:
                    if (pos[i] == 'l' and pos[i+1] == 'l') or (pos[i] == 'r' and pos[i-1] == 'r'):
                        success = False
            else:
                if pos[i] == 'r':
                    flag = True
                if not flag:
                    l = l*10+ans[i]
                else:
                    r = r*10+ans[i]

        if not success:
            print(f'wrong return >> {ans}')
            wrong += 1
            continue

        if l != old_l or r != old_r:
            question_num += 1
            print(f'roud {epoch}: question {question_num}')
            print(ans)
            print(pos)

            if l > r:
                print("Left")
                locate.sim_left()
            else:
                print("Right")
                locate.sim_right()
            print(f'time cost: {time.time()-st}')
            st = time.time()

        old_l, old_r = l, r

    locate.click_next()

os.system('adb kill-server')
