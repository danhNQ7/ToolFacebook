from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from functools import partial
import threading
class ThreadWork(QThread):
    processUpdate = pyqtSignal(int)
    processData = pyqtSignal(list)
    def __init__(self,n):
        self.n=n
        self.result = []
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    def getData(self):
        while self.n:
            self.n=self.n-1
            self.result.append(self.n)
            time.sleep(1)
            self.processUpdate.emit(self.n)
        self.processData.emit(self.result)
    def run(self):
        self.getData()
class main():

    def result(self,val,data):
        print(val)
        print(data)
    def show(self,val):
        print(val)
    def run(self):
        t = ThreadWork(10)
        t.processUpdate.connect(self.show)
        # t.processData.connect(partial(result,12))
        t.start()
        t.wait(20)
        print(data)
    
data =[]
if __name__ == "__main__":
    import sys
    a = QtCore.QCoreApplication(sys.argv)
    main = main()
    main.run()
    # t.wait()
    print(data)
    sys.exit(a.exec_())
