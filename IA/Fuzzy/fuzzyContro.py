from numpy import max
from decimal import *
from math import sin, cos, pi

class fuzzyControl(object):
    def __init__(self):
        return

    def control(self, mdl):
            state = mdl.getState()
            position = state[0]
            inclination = state[1]
            linear_vel = state[2]
            angular_vel = state[3]

        # -------------------------------------------------------------
        # Inclination
        # -------------------------------------------------------------
        # Negative membership determination for inclination
            if inclination <= -0.1:
                negative_th = 1
            elif -0.1 < inclination < 0:
                negative_th = -10 * inclination
            else:
                negative_th = 0

        # Zero membership determination for inclination
            if -0.1 < inclination < -0.03:
                zero_th = -(100/7) * inclination + 10/7
            elif -0.03 <= inclination <= 0.03:
                if inclination<=0:
                    zero_th= 1#+inclination
                else:
                    zero_th=1-inclination
            elif 0.03 < inclination < 0.1:
                zero_th = (100 / 7) * inclination + 10 / 7
            else:
                zero_th = 0

        # Positive membership determination for inclination
            if inclination <= 0:
                positive_th = 0
            elif 0 < inclination < 0.1:
                positive_th = 10 * inclination
            else:
                positive_th = 1

        # -------------------------------------------------------------
        # Angular Velocity
        # -------------------------------------------------------------
        # Negative membership determination for angluar velocity
            if angular_vel <= -0.1:
                negative_thd = 1
            elif -0.1 < angular_vel < 0:
                negative_thd = -10 * angular_vel
            else:
                negative_thd = 0

        # Zero membership determination for angluar velocity
            if -0.15 < angular_vel < -0.03:
                zero_thd = -(100/12) * angular_vel + 15/12
            elif -0.03 <= angular_vel <= 0.03:
                if angular_vel<=0:
                    zero_thd = 1#+angular_vel
                else:
                    zero_thd = 1 - angular_vel
            elif 0.03 < angular_vel < 0.15:
                zero_thd = (100/12) * angular_vel + 15/12 # 1/(0.15-0.03)(que é = 8.333 = 100/12) * angular_vel + 0.15/(0.12-0.03)= 1.25 = 15/12
            else:
                zero_thd = 0

        # Positive membership determination for angular velocity
            if angular_vel <= 0:
                positive_thd = 0
            elif 0 < angular_vel < 0.1:
                positive_thd = 10 * angular_vel
            else:
                positive_thd = 1

                ######################## novas regras

         # -------------------------------------------------------------
        # Position
        # -------------------------------------------------------------
        # Negative membership determination for position
            if position <= -2:
                negative_x = 1
            elif -2 < position < 0:
                negative_x = -0.5 * position
            else:
                negative_x = 0

        # Zero membership determination for position
            if -1.5 < position < -0.5:
                zero_x = -position + 1.5
            elif -0.5 <= position <= 0.5:
                if position<=0:
                    zero_x=1# + position
                else:
                    zero_x=1-position
            elif 0.5 < position < 1.5:
                zero_x = position + 1.5
            else:
                zero_x = 0

        # Positive membership determination for position
            if position <= 0:
                positive_x = 0
            elif 0 < position < 2:
                positive_x = 0.5 * position
            else:
                positive_x = 1

        # -------------------------------------------------------------
        # Linear Velocity
        # -------------------------------------------------------------
        # Negative membership determination for linear velocity
            if linear_vel <= -3:
                negative_xd = 1
            elif -3 < linear_vel < 0:
                negative_xd = -(1/3) * linear_vel
            else:
                negative_xd = 0

        # Zero membership determination for linear velocity
            if -1.5 < linear_vel < -0.5:
                zero_xd = linear_vel + 1.5
            elif -0.5 <= linear_vel <= 0.5:
                if linear_vel<=0:
                    zero_xd=1#+linear_vel
                else:
                    zero_xd=1-linear_vel
            elif 0.5 < linear_vel < 1.5:
                zero_xd = linear_vel + 1.5
            else:
                zero_xd = 0

        # Positive membership determination for angular velocity
            if linear_vel <= 0:
                positive_xd = 0
            elif 0 < linear_vel < 3:
                positive_xd = (1/3) * linear_vel
            else:
                positive_xd = 1

    #inclination & ang. vel.
            NL_iav = [0]
            NM_iav = [0]
            NS_iav = [0]
            Z_iav = [0]
            PS_iav = [0]
            PM_iav =[0]
            PL_iav = [0]
    #position & lin. veloc.
            NL_plv = [0]
            NM_plv = [0]
            NS_plv = [0]
            Z_plv = [0]
            PS_plv = [0]
            PM_plv = [0]
            PL_plv = [0]
        # -------------------------------------------------------------
        # Output membership determination - pendulum rules
        # -------------------------------------------------------------
        # Pendulum rule # 1
            NL_iav.append(min(negative_th, negative_thd))
        # Pendulum rule # 2
            NM_iav.append(min(negative_th, zero_thd))
        # Pendulum rule # 3
            Z_iav.append(min(negative_th, positive_thd))
        # Pendulum rule # 4
            NS_iav.append(min(zero_th, negative_thd))
        # Pendulum rule # 5
            Z_iav.append(min(zero_th, zero_thd))
        # Pendulum rule # 6
            PS_iav.append(min(zero_th, positive_thd))
        # Pendulum rule # 7
            Z_iav.append(min(positive_th, negative_thd))
        # Pendulum rule # 8
            PM_iav.append(min(positive_th, zero_thd))
        # Pendulum rule # 9
            PL_iav.append(min(positive_th, positive_thd))

    # -------------------------------------------------------------
        # Output membership determination - CAR rules
        # -------------------------------------------------------------
        # CAR rule # 1
            NL_plv.append(min(negative_x, negative_xd))
        # CAR rule # 2
            NM_plv.append(min(negative_x, zero_xd))
        # CAR rule # 3
            Z_plv.append(min(negative_x, positive_xd))
        # CAR rule # 4
            NS_plv.append(min(zero_x, negative_xd))
        # CAR rule # 5
            Z_plv.append(min(zero_x, zero_xd))
        # CAR rule # 6
            PS_plv.append(min(zero_x, positive_xd))
        # CAR rule # 7
            Z_plv.append(min(positive_x, negative_xd))
        # CAR rule # 8
            PM_plv.append(min(positive_x, zero_xd))
        # CAR rule # 9
            PL_plv.append(min(positive_x, positive_xd))

        # Determination of the force applied to the car 1 // inclination and ang. velocity//-19/+19
            num_iav = max(NL_iav)*-120 + max(NM_iav)*-60 + max(NS_iav)*-6 + max(Z_iav)*0 + max(PS_iav)*6 + max(PM_iav)*60 + max(PL_iav)*120
            den_iav = max(NL_iav)+max(NM_iav)+max(NS_iav)+max(Z_iav)+max(PS_iav)+max(PM_iav)+max(PL_iav)

        # Determination of the force applied to the car (position + linear vel)
            num_plv = max(NL_plv)*-80 + max(NM_plv)*-17 + max(NS_plv)*-5 + max(Z_plv)*0 + max(PS_plv)*5 + max(PM_plv)*17 + max(PL_plv)*80
            den_plv = max(NL_plv)+max(NM_plv)+max(NS_plv)+max(Z_plv)+max(PS_plv)+max(PM_plv)+max(PL_plv)

            iav = num_iav / den_iav
            plv = num_plv / den_plv
            resp = (iav+plv)

            return resp
