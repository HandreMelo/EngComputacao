from math import sin, cos, pi
import numpy as np
import math


class model(object):
    def __init__(self, q=[0, 0], dt=0.002):
        self.q = np.array([q]).transpose()
        self.qd = np.array([[0, 0]]).transpose()
        self.qdd = np.array([[0, 0]]).transpose()
        self.qini = self.q

        self.dinEnable = False

        self.lc = 1
        self.l = 0.3
        self.mp = 0.2
        self.mc = 0.5
        self.g = 9.8
        self.I = 0.006

        self.dt = dt

    def getState(self):
        return[self.q[0][0], self.q[1][0], self.qd[0][0], self.qd[1][0]]

    def setPos(self, q=[0, 0]):
        self.q = np.array([q]).transpose()

    def enableDin(self):
        self.dinEnable = True

    def disableDin(self):
        self.dinEnable = False

    def dinamics(self, F=0):
#formula da dinâmica
        self.qdd[0][0] = (self.mp*self.l*(self.qd[1][0]**2*sin(self.q[1][0])-self.qdd[1][0]*cos(self.q[1][0]))+F)/(self.mc+self.mp)
        self.qdd[1][0] = (self.mp*self.l*(self.g*sin(self.q[1][0])-self.qdd[0][0]*cos(self.q[1][0])))/(self.I+self.mp*self.l**2)

    def integrate(self, inpt=0):

        if self.dinEnable:
            self.dinamics(inpt)
        else:
            return

        self.qd = self.qd + self.qdd * self.dt
        self.q = self.q + self.qd * self.dt

    def kinematics(self):
        xc1 = self.q[0][0] - self.lc/2
        xc2 = self.q[0][0] + self.lc/2
        yc = 0

        xp = self.q[0][0] + self.l*sin(self.q[1][0])*10
        yp = self.l*cos(self.q[1][0])*10

        return [[[xc1, xc2], [yc, yc]], [[self.q[0][0], xp], [0, yp]]]

    def reset(self):
        self.q = self.qini
        self.qd = np.array([[0, 0]]).transpose()
        self.qdd = np.array([[0, 0]]).transpose()
        return 0
