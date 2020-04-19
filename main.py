
from firstgui import Ui_MainWindow
# from appV2 import audioSpectogram

import appV2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
import sys
    

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.song1 = 0
        self.song2 = 0
        self.song1Flag = None
        self.song2Flag = None
        self.mode = None

    def open_file(self):
        filename = QFileDialog.getOpenFileName(None,"open file",'/home/adel/dsp-task4/songs',"signals(*.mp3)")
        path = filename[0]
        # pathList= path.split('/')
        print(path)
        return path

    def SongName(self,path:str):
        path = path.split('/')
        return path[-1]    
    def readSong1(self):
        self.song1 = self.open_file()
        self.song1Flag = 1 
        self.ui.lineEdit.setText(self.SongName(self.song1))
        print("song1 selected")

    def readSong2(self):
        self.song2 = self.open_file()
        self.song2Flag = 1 
        self.ui.lineEdit_2.setText(self.SongName(self.song2))
        print("song2 selected")

    def mixIt(self):
        ratio = self.ui.percentage_slider.value()/100  
        print(ratio*100)
        appV2.mix(self.song1,self.song2,ratio)
        print("DONE MIXING")

    def readMode(self):
        if self.ui.average.isChecked():
            self.mode = "average"
        elif self.ui.difference.isChecked():
            self.mode = "difference"
        elif self.ui.perception.isChecked():
            self.mode = "perception"        
        # print(self.mode)  
    def compare(self):
        mixedInput = appV2.audioSpectogram('mixed.mp3',hashingMode=self.mode)   
        appV2.generateTxt(mixedInput,hashMode=self.mode)
        print("OOF,done hasing")                 
        scores = appV2.sortedScores()
        for i in range(len(scores)):
            self.ui.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(scores[i][0]))
            self.ui.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(scores[i][-1]))
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = App()

    application.ui.audio1.clicked.connect(application.readSong1)
    application.ui.audio2.clicked.connect(application.readSong2)
    application.ui.mix.clicked.connect(application.mixIt)
    application.ui.average.toggled.connect(application.readMode)
    application.ui.difference.toggled.connect(application.readMode)
    application.ui.perception.toggled.connect(application.readMode)
    application.ui.compare.clicked.connect(application.compare)
    # application.ui.comp2_slider.valueChanged.connect(application.output)

    # application.ui.comboBox_comp2F.activated.connect(application.hideModes)
    
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()        