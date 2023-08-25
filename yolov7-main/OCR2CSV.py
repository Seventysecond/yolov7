import os
import pytesseract
import cv2
import numpy as np
import csv
import argparse

def GetTxtImg(imgFullName):
    #-------------------
    #將圖片左半邊文字部分切割開
    #-------------------
    img_org = cv2.imdecode(np.fromfile(imgFullName,
                                       dtype=np.uint8), cv2.IMREAD_COLOR)  # 读取检测图
    img_gray = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
    height, width = img_gray.shape[:2]
    img_blur = cv2.blur(img_gray, (1, height))
    line_blur = img_blur[0:1, 0:width]
    lessThre = np.flatnonzero(line_blur < 20)
    txtRight = 460
    if (len(lessThre) >= 1):
        txtRight = int(lessThre[0])
    TxtImg = img_org[:, :txtRight]
    return TxtImg

def cut_image(image,x,y):
    #-------------------
    #將圖片再次切割
    #目的找到scratch length
    #-------------------
    w = 300
    h = 300
    image_text = image[y:y+h, x:x+w]
    return image_text

def pic2num_list(img):
    #-------------------
    #將圖片轉成數字陣列
    #-------------------
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    text = pytesseract.image_to_string(img, config=custom_config)
    text = ''.join(text)
    result = []
    number = ""
    for char in text:

        if char == "\n":
            if number:
                result.append(number)
                number =""
        else:
            number += char

    return result

def pic2str_list(img):
    #-------------------
    #將圖片轉成字串陣列
    #-------------------
    custom_config = r'--oem 3 --psm 6 -l eng'
    text = pytesseract.image_to_string(img, config=custom_config)
    text = ''.join(text)
    result = []
    string = ""
    for char in text:

        if char == "\n":
            if string:
                result.append(string)
                string =""
        else:
            string += char
    return result

def scratch_num(imgPath,savefilePath):
    #-------------------
    #紀錄LOT_ID WAFFER_ID
    #紀錄對應的status
    #儲存進csv檔案中
    #-------------------
    
    #csv檔建立
    print(imgPath)
    file_path = savefilePath + 'output1.csv'
    with open(file_path, 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入一列資料
        writer.writerow(['LOT', 'WAFER', 'Pattern'])
    img_file = os.listdir(imgPath)
    imgPath = [imgPath + i for i in img_file]
    print(imgPath[0])
    for i in imgPath:
         #img檔名拆分
        
        file_name = i.split("\\")[-1]
        base_name, extension = file_name.split(".")
        LWname = base_name.split('_')
        
        #圖片切割與圖轉字串
        img = GetTxtImg(i)
        image_num = cut_image(img,270,800)
        image_text = cut_image(img,25,800)
        num_list = pic2num_list(image_num)
        str_list = pic2str_list(image_text)
        try:
            idx = str_list.index('Scratch length:')
            if float(num_list[idx]) > 0:
                with open(file_path, 'a', newline='') as csvfile:
                    # 建立 CSV 檔寫入器
                    writer = csv.writer(csvfile)
                    # 寫入一列資料
                    writer.writerow([LWname[2],LWname[3],'scratch'])
            else:
                with open(file_path, 'a', newline='') as csvfile:
                    # 建立 CSV 檔寫入器
                    writer = csv.writer(csvfile)
                    # 寫入一列資料
                    writer.writerow([LWname[2],LWname[3],'ok'])
        except ValueError:
            with open(file_path, 'a', newline='') as csvfile:
                    # 建立 CSV 檔寫入器
                    writer = csv.writer(csvfile)
                    # 寫入一列資料
                    writer.writerow([LWname[2],LWname[3],'none'])
    print('finish')
    
if __name__ == '__main__':
    
     parser = argparse.ArgumentParser()
     parser.add_argument('--source', type=str, default='D:/yzu_learnig/intership/learning/final/data/scratched/labelimg/', help='輸入圖片路徑')
     parser.add_argument('--savepath', type=str, default='D:/yzu_learnig/intership/learning/final/data/scratched/', help='輸入檔案存取位置')
     args = parser.parse_args()
     scratch_num(args.source,args.savepath)
