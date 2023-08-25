import xml.etree.ElementTree as ET
import os
import importlib
#------
#https://ithelp.ithome.com.tw/articles/10307097
#最好還要建立一個yolo資料夾存放結果
#------
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh

    return (x, y, w, h)
def convert_xml_to_voc(xmlPath):       #從DC槽一路到檔案名稱
    folder1 = os.path.join(opt.source, opt.xml)     
    folder1 = folder1.replace('xmls', 'yolo')
    for xml in xmlPath:
        tree = ET.parse(xml)
        root = tree.getroot()
        filename = xml.replace('.xml', '.txt').replace('xmls', 'yolo')  #路徑改變
        
        if not os.path.exists(folder1):
            os.makedirs(folder1)
        # 處理每個標註的Bounding box
        with open(filename, "w") as bbox:
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)

            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls = obj.find('name').text
                if cls not in classes or int(difficult) == 1:
                    continue
                cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), 
                     float(xmlbox.find('xmax').text), 
                     float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = convert((w, h), b)
                bbox.write(str(cls_id) + " " + 
                           " ".join([str(a) for a in bb]) + '\n')
    print('1. 將標籤從xml轉換成voc格式：完成')
    print('-'*50)

#刪除指定格式資料
def delete_file(filePath, endstring):    
    #------------------
    #filePath:str,檔案所在位置
    #endstring:str,檔案類型:.txt,.jpg
    #------------------ 
    txtPath = os.listdir(filePath)        #資料夾底下所有目錄
    for file_name in txtPath:
        file_path = os.path.join(filePath, file_name)   #位址+檔名
        if file_name.endswith(endstring):          #檔案類行為...的話
            os.remove(file_path)          #刪除
            
    print("刪除成功")
    
    
if __name__ == '__main__':
    opt = importlib.import_module("cfg.xml2yolo_config")
    source = opt.source
    # 讀取標籤類別
    with open(os.path.join(source, 'classes.txt'), encoding='utf-8') as f:      #要先準備好classes檔案
        classes = f.read().strip().split()
    # xml資料夾路徑********
    xmlDir = os.path.join(source, opt.xml)
    # xml檔案路徑
    xmlPath = os.listdir(xmlDir)
    xmlPath = [xmlDir + i for i in xmlPath]
    convert_xml_to_voc(xmlPath)    