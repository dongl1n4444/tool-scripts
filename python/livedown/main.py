import os
import sys
import Tkinter, tkFileDialog, tkMessageBox
import join_flv

global gFolderDir
gFolderDir = ''

global btnSelect
global btnJoin
global statusBar

global isSortByTime 
isSortByTime = False

def startJoin():
    global gFolderDir, btnSelect, btnJoin, isSortByTime
    
    flv_folder = str(gFolderDir)
    if not os.path.isdir(flv_folder):
        print 'Folder not exit: ' + flv_folder
        return
        
    input_path_list = []
    for parent, dirnames, filenames in os.walk(flv_folder):
        for filename in filenames:
            # if str.find(filename, '.grf') != -1 or str.find(filename, '.flv') != -1: 
            if str.find(filename, '.grf') != -1:
                input_path_list.append(parent + '/' + filename)
                
    if len(input_path_list) == 0:
        tkMessageBox.showwarning("Open file", "Cannot find any grfs in folder (%s)"%flv_folder)        
        return
    
    if isSortByTime:
        dictFiles = {}
        for path in input_path_list:
            ftime = int(os.path.getmtime(path))
            dictFiles[ftime] = path
            
        keyList = dictFiles.keys()
        keyList.sort()
        
        input_path_list = []
        for ftime in keyList:
            input_path_list.append(dictFiles[ftime])
        
    else:
        input_path_list.sort()

    # Wrong file path.
    print '---start join---'
    for path in input_path_list:
        print path
        if not os.path.isfile(path):
            print 'File not exit: ' + path
            return
        
    dir_path = os.path.dirname(input_path_list[0])
    # Output file is created in the same directory as the first input file.
    output_path = os.path.join(dir_path, 'output.flv')
    
    btnSelect.configure(state='disabled')
    btnJoin.configure(state='disabled')
    statusBar.set('Waiting, now joining grfs')
    
    join_flv.join_flv(output_path, input_path_list)
    print 'Succeed!'
    print 'Output file path is ' + output_path
    print '---end join---'
    
    statusBar.set('Join Succeed')
    
    btnSelect.configure(state='normal')
    btnJoin.configure(state='normal')
    
class StatusBar(Tkinter.Frame):
    def __init__(self, master):
        global labStatus
        Tkinter.Frame.__init__(self, master, padx=5, pady=5)
        self.label = Tkinter.Label(self, bd=1, relief=Tkinter.SUNKEN, anchor=Tkinter.W)
        self.label.pack(fill=Tkinter.X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

def main():
    global btnSelect, btnJoin, statusBar
    
    root = Tkinter.Tk()
    root.title('JoinFlv')
    
    frm = Tkinter.Frame(root)
    # frm.pack_propagate(0)
    frm.pack(fill=Tkinter.X, padx=5, pady=5)
    
    #lab = Tkinter.Label(frm, text="gafs/flvs folder path", justify=Tkinter.LEFT)
    #lab.pack()
    
    #txt = Tkinter.Text(frm, state='disabled')
    #txt.insert('1.0', 'gafs/flvs folder path')
    #txt.pack()
    
    ety = Tkinter.Entry(frm, state='readonly', relief=Tkinter.SUNKEN)
    # ety.pack(fill=Tkinter.X)
    # ety.grid(columnspan=2)
    ety.pack(fill=Tkinter.X)
    
    chbVal = Tkinter.IntVar()
    def onClickCheckBox():
        global isSortByTime
        isSortByTime = chbVal.get()
    
    chb = Tkinter.Checkbutton(frm, text="Auto sort by file create time", command=onClickCheckBox, variable=chbVal)
    chb.pack()    
    
    btnJoin = Tkinter.Button(frm, text="Join", command=startJoin, state="disabled", width=10)
    btnJoin.pack(side=Tkinter.RIGHT, padx=2, pady=2, fill=Tkinter.X)
    # btnJoin.grid(row=1, column=1)    
    
    def onClickBtnChooseFolder():
        #ety.configure(state="normal")
        #ety.delete(0, 'end')
        #ety.insert(0, 'your name')
        #ety.configure(state="disabled")
        global gFolderDir                
        gFolderDir = tkFileDialog.askdirectory()
        
        ety.configure(state="normal")
        ety.delete(0, 'end')
        ety.insert(0, gFolderDir)
        ety.configure(state="readonly")  
        
        btnJoin.configure(state='normal')
    
    btnSelect = Tkinter.Button(frm, text="Select", command=onClickBtnChooseFolder, width=10)
    btnSelect.pack(side=Tkinter.LEFT, padx=2, pady=2, fill=Tkinter.X)
    # btnSelect.grid(row=1, column=0)
    
    frmStatus = StatusBar(root)
    frmStatus.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
    frmStatus.set('%s', "Choose grf folder")
    statusBar = frmStatus
    
    root.mainloop()
    return

if __name__ == '__main__':
    main()