import cv2
import numpy as np
import time


class caler:
    def __init__(self):
        self.numbers = [cv2.imread(
            f'./read/{i}.png', cv2.IMREAD_GRAYSCALE) for i in range(10)]
        self.numbers.append(cv2.imread(
            f'./read/wenhao.png', cv2.IMREAD_GRAYSCALE))

    def cal_sim(self, img):

        def mse(img1, img2):
            img1 = img1.astype(np.float32)/255
            img2 = img2.astype(np.float32)/255
            diff = img1 - img2
            diff_squared = diff ** 2
            mse = np.mean(diff_squared)
            return mse

        min_diff = 100
        ans = -1
        for i in range(len(self.numbers)):
            tmp_img = cv2.resize(
                img, (self.numbers[i].shape[1], self.numbers[i].shape[0]))
            diff = mse(self.numbers[i], tmp_img)
            if diff < min_diff:
                ans = i
                min_diff = diff

        # print('min_diff: ', min_diff)
        if min_diff > 0.2:
            return '?'
        # cv2.imwrite(f'./tmp/{time.time()}.png', img)
        if ans <= 9:
            return ans
        elif ans == 10:
            return '?'
