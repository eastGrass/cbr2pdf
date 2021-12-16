from tkinter import *
# 引入字体模块
import tkinter.font as tkFont
from tkinter import filedialog
import shutil # copy file
import patoolib # rar file
import glob
import fitz # from image to pdf
import os
from tempfile import TemporaryDirectory

def inFileCallback(inVar):
    inFileTypes = [ ('bcr files', '* .cbr'),('All files','*') ]
    inFileName = filedialog.askopenfilename(title='Select the source file',\
                                            defaultextension='.cbr', \
                                            filetypes=inFileTypes)
    inVar.set(inFileName)

def outFileCallback(outVar):
    outFileTypes = [ ('pdf files', '* .pdf'),('All files','*') ]

    outFileName = filedialog.asksaveasfilename(title='Select the target file for saving records',\
                                        defaultextension='.pdf',\
                                        filetypes=outFileTypes) 

    outVar.set(outFileName)


def pic2pdf(picDir, destFile):
    doc = fitz.open()
  
    # images 所在目录
    fileList = glob.glob(os.path.join(picDir, "*"))
    # print("file list=%s" %(fileList))

    # 读取图片，按文件名排序
    for img in sorted(fileList, key=lambda x: x.split("\\")[-1].split(".")[0]):
        imgdoc = fitz.open(img)  # 打开图片
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(imgpdf) # 将当前页插入文档

    # assert pdf file
    if os.path.exists(destFile):
        os.remove(destFile)

    doc.save(destFile)  # 保存pdf文件
    doc.close()

"""
1. create a temporary dir
2. copy cbr file
3. rename cbr ext into rar
4. unzip rar in temporary dir
5. change images into pdf
"""
def transferCbr2pdf(srcFilePath, destFilePath):
    # 创建 临时目录
    with TemporaryDirectory() as zipTmpDir:
        cbrFilePath = shutil.copy(srcFilePath, zipTmpDir)

        # 分离文件名与扩展名
        fileName, fileExtName = os.path.splitext(cbrFilePath)
        # 如果后缀是jpg
        if fileExtName == '.cbr':
            # 重新组合文件名和后缀名
            rarFilePath = fileName + '.rar'
            os.rename(cbrFilePath, rarFilePath)

        print("new file = %s" % (rarFilePath))

        with TemporaryDirectory() as imgTmpDir:
            patoolib.extract_archive(rarFilePath, outdir=imgTmpDir)

            print("img dir = %s" % (imgTmpDir))
            pic2pdf(imgTmpDir, destFilePath)


#创建主窗口
win = Tk()
win.title(string="from CBR to PDF")

ft = tkFont.Font(family='Fixdsys', size=30, weight=tkFont.BOLD)
Label(win, text='C b R', font=ft).grid(row=0, column=1)

# input & output file
inFilePath = StringVar()
outFilePath = StringVar()

labelIn = Label(win,text="input file path：")
inEntry = Entry(win,width=45,textvariable = inFilePath)
# 定义按钮并指定触发函数
btnIn = Button(win,text='source',width=10, \
               command = lambda: inFileCallback(inFilePath))

labelIn.grid(row=1, column=0)
inEntry.grid(row=1, column=1)
btnIn.grid(row=1, column=2)

# out file dialgo
labelOut = Label(win,text="output file path：")
outEntry = Entry(win,width=45,textvariable = outFilePath)
btnOut = Button(win,text='target',width=10, \
                command = lambda: outFileCallback(outFilePath))

labelOut.grid(row=2, column=0)
outEntry.grid(row=2, column=1)
btnOut.grid(row=2, column=2)

# transform using temporary dir and files
# Tkinter button事件绑定 & 参数传递
btnTransfer = Button(win,text='transform',width=10, \
                     command = lambda : transferCbr2pdf(inFilePath.get(),outFilePath.get()))
btnTransfer.grid(row=3, column=2)

win.mainloop()