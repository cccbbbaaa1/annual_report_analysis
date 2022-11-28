# 年报pdf转txt
import os
import pdfplumber

if __name__=='__main__':
    pathlist=os.listdir('.')
    for eachfile in pathlist:
        if not (eachfile[-3:]) == '.py':
            try:
                txt_path = eachfile.replace(eachfile,'.\\结果\\'+eachfile).replace(".PDF", ".txt")
                print(txt_path)
                with open(txt_path, 'w', encoding='utf-8') as txt:
                    with pdfplumber.open(eachfile) as pdf:
                        for page in pdf.pages:
                            txt.write(page.extract_text())
                print(eachfile + "成功转为txt文件！")
            except:
                print(eachfile + "转为txt文件失败！！！")