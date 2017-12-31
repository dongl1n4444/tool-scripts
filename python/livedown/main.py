#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import re
import join_flv
import subprocess
import wx

reload(sys)
sys.setdefaultencoding('utf-8')

def convertGrfFolder(grfFolder, isOutputMP4):
    if not os.path.isdir(grfFolder):
        print 'Folder not exit: ' + grfFolder
        return
        
    input_path_list = []
    for parent, dirnames, filenames in os.walk(grfFolder):
        for filename in filenames:
            # if str.find(filename, '.grf') != -1 or str.find(filename, '.flv') != -1:
            if filename[len(filename)-4:] == '.grf':
                input_path_list.append(parent + '/' + filename)
                
    if len(input_path_list) == 0:
        wx.MessageBox("在目录 (%s) 不能找到任何 grf 文件"%grfFolder, 'Warning', wx.OK | wx.ICON_WARNING)
        return

    # check num prefix
    isNumPrefix = False
    isNumSuffix = False
    for path in input_path_list:
        mm = re.search(r'^\d+', path)
        if mm:
            isNumPrefix = True
            break
        else:
            mm = re.search(r'\d+.grf', path)
            if mm:
                isNumSuffix = True
                break

    if not isNumPrefix and not isNumSuffix:
        wx.MessageBox("未找到有效的数字标记", 'Warning', wx.OK | wx.ICON_WARNING)
        return

    unhandler_paths = []
    dict_paths = {}

    if isNumSuffix:
        for path in input_path_list:
            mm = re.search(r'\d+.grf', path)
            if mm:
                dict_paths[int(mm.group(0)[0:-4])] = path
            else:
                unhandler_paths.append(path)
    elif isNumPrefix:
        for path in input_path_list:
            mm = re.search(r'^\d+')
            if mm:
                dict_paths[int(mm.group(0))] = path
            else:
                unhandler_paths.append(path)

    # sort
    input_path_list = []
    keys = dict_paths.keys()
    keys.sort()
    for i in keys:
        input_path_list.append(dict_paths[i])

    if len(input_path_list) == 0:
        wx.MessageBox("未找到可转换的有效文件", 'Warning', wx.OK | wx.ICON_WARNING)
        return

    # Wrong file path.
    # print '---start join---'
    # for path in input_path_list:
    #     print path
    #     if not os.path.isfile(path):
    #         print 'File not exit: ' + path
    #         return
        
    # dir_path = os.path.dirname(input_path_list[0])
    # Output file is created in the same directory as the first input file.
    output_path = os.path.join(grfFolder, 'output.flv')
    
    join_flv.join_flv(output_path, input_path_list)
    print 'Succeed!'
    print 'Output file path is ' + output_path
    print '---end join---'

    # convert to mp4
    if isOutputMP4:
        pydir = os.path.dirname(os.path.realpath(__file__))
        ffmpeg_path = os.path.join(pydir, "ffmpeg\\bin\\ffmpeg.exe")
        script_path = os.path.join(pydir, "output_mp4.bat")
        if os.path.isfile(ffmpeg_path) == False or os.path.isfile(script_path) == False:
            wx.MessageBox("文件缺失，无法导出 mp4", 'Warning', wx.OK | wx.ICON_WARNING)
        else:
            mp4_output_path = os.path.join(grfFolder, 'output.mp4')

            tmp_file = open('tmp.dat', 'wb')
            tmp_file.write(output_path)
            tmp_file.write('\n')
            tmp_file.write(mp4_output_path)
            tmp_file.close()

            os.system(script_path)

    if len(unhandler_paths) > 0:
        wx.MessageBox('\n'.join(unhandler_paths), "未处理文件，请查看文件名是否规范", wx.OK | wx.ICON_INFORMATION)

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300, 200))

        self.grfFolder = u"";
        self.isOutputMP4 = True

        self.CreateStatusBar()

        self.txtPath = wx.TextCtrl(self, pos=(10, 10), size=(260, 30), style=wx.TE_READONLY)

        self.btnSelect = wx.Button(self, label=u"选择文件", pos=(10, 50), size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.onClickBtnSelect, self.btnSelect)

        self.btnConvert = wx.Button(self, label=u"开始转换", pos=(150, 50), size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.onClickBtnConvert, self.btnConvert)
        self.btnConvert.Enable(False)

        self.checkMp4 = wx.CheckBox(self, label=u"导出MP4格式", pos=(10, 100))
        self.Bind(wx.EVT_CHECKBOX, self.onClickCheckMP4, self.checkMp4)
        self.checkMp4.SetValue(True)

    def onClickBtnSelect(self, event):
        dlg = wx.DirDialog(self, u"选择 grf 文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.grfFolder = dlg.GetPath()
            self.txtPath.AppendText(self.grfFolder)
            self.btnConvert.Enable(True)

    def onClickBtnConvert(self, event):
        # try:
            self.btnSelect.Enable(False)
            self.btnConvert.Enable(False)

            convertGrfFolder(self.grfFolder, self.isOutputMP4)

            self.btnSelect.Enable(True)
            self.btnConvert.Enable(True)
        # except:
        #     print 'ERROR>unknow error.'
        #     self.btnSelect.Enable(True)
        #     self.btnConvert.Enable(True)

    def onClickCheckMP4(self, event):
        self.isOutputMP4 = self.checkMp4.GetValue()

def main():
    app = wx.App(False)
    frame = MainFrame(None, "grf converter")
    frame.Show(True)
    app.MainLoop()
    return

if __name__ == '__main__':
    main()