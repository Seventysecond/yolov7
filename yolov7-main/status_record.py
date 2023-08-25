import os
import cv2
import csv
import pytesseract
import numpy as np

#將圖片左半邊文字部分切割開
def GetTxtImg(imgFullName):
    #-------------------
    #imgFullName:str,圖片路徑
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

#將圖片再次切割目的找到scratch length
def cut_image(image,x,y):
    #-------------------
    #image:array,原圖
    #x,y:int,切割起始座標
    #-------------------
    w = 300
    h = 300
    image_text = image[y:y+h, x:x+w]
    return image_text

#將圖片轉成數字陣列
def pic2num_list(img):
    #-------------------
    #img:array 圖片資訊
    #-------------------
    #--oem 3:使用 Tesseract 原生 OCR 引擎進行文字識別
    #--psm 6:假設有一個統一的文本塊，並嘗試識別這個區域內的文字
    #outputbase digits:此為專門偵測數字
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    text = pytesseract.image_to_string(img, config=custom_config)
    text = ''.join(text)
    result = []    #儲存每一欄字串
    number = ""
    for char in text:
        #以換行作為斷點，將字元結合成字串
        if char == "\n":
            if number:
                result.append(number)
                number =""
        else:
            number += char

    return result

#將圖片轉成字串陣列
def pic2str_list(img):
    #-------------------
    #img:array 圖片資訊
    #-------------------
    #--oem 3:使用 Tesseract 原生 OCR 引擎進行文字識別
    #--psm 6:假設有一個統一的文本塊，並嘗試識別這個區域內的文字
    #-l eng:偵測語言，此為專門偵測英文
    custom_config = r'--oem 3 --psm 6 -l eng' 
    text = pytesseract.image_to_string(img, config=custom_config)   #ocr
    text = ''.join(text)
    result = []   #儲存每一欄字串
    string = ""
    for char in text:
        #以換行作為斷點，將字元結合成字串
        if char == "\n":
            if string:
                result.append(string)
                string =""
        elif char == "S":
            char = 's'
            string += char
        else:
            string += char
    return result

#檢查detect出來歸類為ok的是否真的為ok
def check_state(path, state='ok', threhold = 0):
    #-------------------------
    #path:str,圖片路徑
    #state:str,wafer AI預測狀態,default='ok'
    #threshold:int,scratch length閥值
    #-------------------------
    OCR = state  #OCR檢測結果
    img = GetTxtImg(path)
    image_num = cut_image(img,270,800)
    image_text = cut_image(img,25,800)
    num_list = pic2num_list(image_num)
    str_list = pic2str_list(image_text)
    try:
            idx = str_list.index('scratch length:')
            if float(num_list[idx]) > threhold:
                OCR = 'scratch'
            else:
                OCR = 'ok'
    except ValueError:
        OCR = state
    return OCR
    
    

#配合檢測出來的結果紀錄進
def record_state(save_path, state, method):
    #-------------------------
    #save_path:str,存檔路徑
    #state:str,最後儲存狀態
    #method:str,檢測方法
    #-------------------------
    csv_path = os.path.dirname(save_path)
    folder1 = csv_path + '\state_result'  #new folder 
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    csv_path = folder1 + '\output.csv'
    
    with open(csv_path, 'a', newline='') as csvfile:
    # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        #避免標頭重複寫入
        with open(csv_path, 'r', newline='') as csvfile:
            row = csv.reader(csvfile)
            first_row = next(row, None)
            if first_row is None:
                with open(csv_path, 'a', newline='') as csvfile:
                    # 建立 CSV 檔寫入器
                    writer = csv.writer(csvfile)
                    # 寫入一列資料
                    writer.writerow(['LOT', 'WAFER', 'Pattern','Method'])
    file_name = save_path.split("\\")[-1]   
    base_name, extension = file_name.split(".")
    LWname = base_name.split('_')
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 寫入一列資料
        writer.writerow([LWname[2],LWname[3],state,method])
        
        
#===============================================================================
#example
#===============================================================================\
    
#import satatus_record as sr
#save_path = csv儲存路徑
#state = 'ok'
#method = 'AI'
#sr.record_state(save_path, state,method)

#path=test image path
#state='ok',
#threhold = 0
#sr.check_state(path, state, threshold)

