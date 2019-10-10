from PyQt5 import QtWidgets, QtCore
import sys
from math import sin, cos, pi
import simpy.rt
import fuzzyControl
import model

import ui_main
import pyqtgraph
from threading import Thread, Lock

class ExampleApp(QtWidgets.QMainWindow, ui_main.Ui_MainWindow):
    signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        pyqtgraph.setConfigOption('antialias', True)
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.btnPlay.clicked.connect(self.play)
        self.btnPause.clicked.connect(self.pause)
        self.btnPause.setDisabled(True)
        self.btnStop.clicked.connect(self.stop)
        self.btnStop.setDisabled(True)
        self.btnDin.clicked.connect(self.toggleDin)

        self.flagPause = False
        self.flagStop = False
        self.mainTh = Thread(target=self.simTh)
        self.mainMtx = Lock()
        self.listPoints = [[0, 0]]
        self.objPoint = []

        self.grPlot.plotItem.showGrid(True, False, 0.3)
        self.grPlot.plotItem.getViewBox().setMouseEnabled(False,False)
        self.grPlot.getPlotItem().hideAxis('left')
        self.grPlot.setYRange(-3, 7)
        self.grPlot.setXRange(-10, 10)
        self.grPlot.setFixedSize(600, 300)
        self.setFixedSize(622, 383)
        self.grPlot.getPlotItem().getAxis('top').setFixedHeight(25)
        self.grPlot.getPlotItem().getAxis('bottom').setFixedHeight(25)
        self.grPlot.getPlotItem().getAxis('left').setFixedWidth(25)
        self.grPlot.getPlotItem().getAxis('right').setFixedWidth(25)

        self.signal.connect(self.draw)

        # model object
        self.mdl = model.model([0, 30*pi/180])
        self.rdoDin.setChecked(True)
        self.mdl.enableDin()
        # controller object
        self.ctrl = fuzzyControl.fuzzyControl()

    def pause(self):
        self.grPlot.sceneObj.sigMouseClicked.disconnect()
        self.mainMtx.acquire()
        self.btnPause.setDisabled(True)
        self.btnPlay.setEnabled(True)
        self.flagPause = True

    def stop(self):
        if self.flagPause:
            self.flagPause = False
            self.flagStop = True

        if not self.flagStop:
            self.mainMtx.acquire()
            self.flagStop = True

        self.btnPlay.setEnabled(True)
        self.btnStop.setDisabled(True)
        self.btnPause.setDisabled(True)

    def play(self):
        if self.flagStop:
            self.mdl.reset()

        if self.mainTh.isAlive():
            self.mainMtx.release()
        else:
            self.mainTh.start()

        self.btnStop.setEnabled(True)
        self.btnPause.setEnabled(True)
        self.btnPlay.setDisabled(True)
        self.flagPause = False
        self.flagStop = False

    def simulation(self, env):
        tm = 0
        while True:
            self.mainMtx.acquire()

            F = self.ctrl.control(self.mdl)
            self.mdl.integrate(F)

            if tm > 0.1:
                self.signal.emit()
                tm = 0

            tm = tm + self.mdl.dt
            self.mainMtx.release()
            yield env.timeout(self.mdl.dt)


    def simTh(self):
        # simulation environment
        self.env = simpy.rt.RealtimeEnvironment(factor=1, strict=0)
        # simulation process definition
        proc = self.env.process(self.simulation(self.env))
        # simulation start
        self.env.run()

    def draw(self):
        points = self.mdl.kinematics()
        pen1 = pyqtgraph.mkPen(color='k', width=3)
        self.grPlot.plotItem.clear()
        for set in points:
            self.grPlot.plotItem.plot(set[0], set[1], pen=pen1)

    def toggleDin(self):
        if self.mdl.dinEnable:
            self.rdoDin.setChecked(False)
            self.mdl.disableDin()
        else:
            self.rdoDin.setChecked(True)
            self.mdl.enableDin()

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
