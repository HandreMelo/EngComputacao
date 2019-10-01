from numpy import max
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
    #
    #        X = A· θ + B·
    #        dθ
    #        dt...........(4)#

    #        Y = C· x + D·
    #        dx
    #        dt............(5)
    #
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
                zero_th = (100/7) * inclination + 10/7
            elif -0.03 <= inclination <= 0.03:
                zero_th = 1
            elif 0.03 < inclination < 0.1:
                zero_th = -(100 / 7) * inclination + 10 / 7
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
                zero_thd = (100/12) * angular_vel + 15/12
            elif -0.03 <= angular_vel <= 0.03:
                zero_thd = 1
            elif 0.03 < angular_vel < 0.15:
                zero_thd = -(100/12) * angular_vel + 15/12 # 1/(0.15-0.03)(que é = 8.333 = 100/12) * angular_vel + 0.15/(0.12-0.03)= 1.25 = 15/12
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
                zero_x = position + 3
                #print(position)
            elif -0.5 <= position <= 0.5:
                zero_x = 1
            elif 0.5 < position < 1.5:
                zero_x = -position + 3
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
                zero_xd = linear_vel + 3
            elif -0.5 <= linear_vel <= 0.5:
                zero_xd = 1
            elif 0.5 < linear_vel < 1.5:
                zero_xd = -linear_vel + 3
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

        # Determination of the force applied to the car 1
            num_p_iav = max(NL_iav)*-100 + max(NM_iav)*-40 + max(NS_iav)*-5 + max(Z_iav)*0 + max(PS_iav)*5 + max(PM_iav)*40 + max(PL_iav)*100
            den_p_iav = max(NL_iav)+max(NM_iav)+max(NS_iav)+max(Z_iav)+max(PS_iav)+max(PM_iav)+max(PL_iav)

        # Determination of the force applied to the car 2
            num_p_plv = max(NL_plv)*-50 + max(NM_plv)*-5 + max(NS_plv)*-1 + max(Z_plv)*0 + max(PS_plv)*1 + max(PM_plv)*5 + max(PL_plv)*50
            den_p_plv = max(NL_plv)+max(NM_plv)+max(NS_plv)+max(Z_plv)+max(PS_plv)+max(PM_plv)+max(PL_plv)
            #return ((num_p_iav+num_p_plv) / (den_p_iav+den_p_plv))
            #return (num_p_iav / den_p_plv) + (num_p_plv / den_p_iav)
            return (num_p_iav / den_p_iav) + (num_p_plv / den_p_plv)
