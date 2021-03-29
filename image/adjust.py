import os
from os.path import isfile, isdir, dirname, abspath, join, basename, splitext
import sys
import argparse
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tqdm
import glob
import shutil

dir_script = dirname(abspath(__file__))
dir_script = abspath(join(dir_script, '..'))

def adjust(img, alpha=1.0, beta=0.0):
    # 積和演算を行う。
    dst = alpha * img + beta
    # [0, 255] でクリップし、uint8 型にする。
    return np.clip(dst, 0, 255).astype(np.uint8)

def main():

    # vottからエクスポートされたpascalVOCのディレクトリを収集
    files = glob.glob(f"{dir_input}/*")

    # 全対象フォルダの画像パスを選別
    for i in tqdm.trange(len(files)):
        with Image.open(files[i-1]) as img:
            fname = files[i-1]

            # img_gray = img.convert("L").convert("RGB")
            # # img_gray = img.convert("L")
            # img_gray.save(fname)
            # ar_gray = np.asarray(img_gray, np.uint8)
            # plt.imshow(ar_gray)
            # plt.show()

            img = cv2.imread(fname)
            img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

            if args.color != 1.0:
                img_hsv[:,:,(0)] = img_hsv[:,:,(0)] * args.color  # 色相
            if args.saturation != 1.0:
                img_hsv[:,:,(1)] = img_hsv[:,:,(1)] * args.saturation  # 彩度
            if args.value != 1.0:
                img_hsv[:,:,(2)] = img_hsv[:,:,(2)] * args.value  # 明度

            if args.alpha != 1.0 or args.beta != 0.0:
                img_hsv = adjust(img_hsv, args.alpha, args.beta)

            img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)

            # plt.imshow(img_bgr)
            # plt.show()

            dst = join(dir_output, basename(fname))
            cv2.imwrite(dst, img_bgr)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This script convert image to grayscale')
    parser.add_argument('dir_input', help='directory contain original images.')
    parser.add_argument('dir_output', help='directory for output.')

    # コントラスト、輝度
    parser.add_argument('--alpha', '-a', help='change contrast.(based 1.0)', type=float, default=1.0)
    parser.add_argument('--beta', '-b', help='change luminance. (based 0.0)', type=float, default=0.0)

    # 色相、彩度、明度
    parser.add_argument('--color', '-c', help='change hue.', type=float, default=1.0)
    parser.add_argument('--saturation', '-s', help='change saturation.', type=float, default=1.0)
    parser.add_argument('--value', '-v', help='change value.', type=float, default=1.0)

    args = parser.parse_args()

    dir_input = abspath(join(dir_script, args.dir_input))
    if not isdir(dir_input):
        print(f"[error] dataset not exist.")

    dir_output = abspath(join(dir_script, args.dir_output))
    if isdir(dir_output):
        shutil.rmtree(dir_output)
    os.makedirs(dir_output)

    print(args)

    main()
