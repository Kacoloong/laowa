# -*- coding: utf-8 -*-            
# @Time : 2024/07/11 11:27
# @Author: yxli
# @FileName: boolear.py
# @Software: PyCharm


def ifx(in1, in2, in3, out, cin1, cin2, cin3, cin4):
    for i in range(32):
        # =n==,=u==
        if in1[i] == '=' and (in2[i] == 'n' or in2[i] == 'u') and in3[i] == '=' and out[i] == '=':
            cin1[i] = '0'
        # =n=n
        elif in1[i] == '=' and in2[i] == 'n' and in3[i] == '=' and out[i] == 'n':
            cin1[i] = '1'
        # =u=u
        elif in1[i] == '=' and in2[i] == 'u' and in3[i] == '=' and out[i] == 'u':
            cin1[i] = '1'
        # ==n=,==u=
        elif in1[i] == '=' and in2[i] == '=' and (in3[i] == 'n' or in3[i] == 'u') and out[i] == '=':
            cin1[i] = '1'
        # ==uu
        elif in1[i] == '=' and in2[i] == '=' and in3[i] == 'u' and out[i] == 'u':
            cin1[i] = '0'
        # ==nn
        elif in1[i] == '=' and in2[i] == '=' and in3[i] == 'n' and out[i] == 'n':
            cin1[i] = '0'
        # n==n
        elif in1[i] == 'n' and in2[i] == '=' and in3[i] == '=' and out[i] == 'n':
            cin2[i] = '1'
            cin3[i] = '0'
        # u==n
        elif in1[i] == 'u' and in2[i] == '=' and in3[i] == '=' and out[i] == 'n':
            cin2[i] = '0'
            cin3[i] = '1'
        # n==u
        elif in1[i] == 'n' and in2[i] == '=' and in3[i] == '=' and out[i] == 'u':
            cin2[i] = '0'
            cin3[i] = '1'
        # u==u
        elif in1[i] == 'u' and in2[i] == '=' and in3[i] == '=' and out[i] == 'u':
            cin2[i] = '1'
            cin3[i] = '0'
        # nn==
        elif in1[i] == 'n' and in2[i] == 'n' and in3[i] == '=' and out[i] == '=':
            cin3[i] = '1'
        # nu==
        elif in1[i] == 'n' and in2[i] == 'u' and in3[i] == '=' and out[i] == '=':
            cin3[i] = '0'
        # uu==
        elif in1[i] == 'u' and in2[i] == 'u' and in3[i] == '=' and out[i] == '=':
            cin3[i] = '1'
        # un==
        elif in1[i] == 'u' and in2[i] == 'n' and in3[i] == '=' and out[i] == '=':
            cin3[i] = '0'
        # n=n=
        elif in1[i] == 'n' and in2[i] == '=' and in3[i] == 'n' and out[i] == '=':
            cin2[i] = '0'

        # n=u=
        elif in1[i] == 'n' and in2[i] == '=' and in3[i] == 'u' and out[i] == '=':
            cin2[i] = '1'

        # u=u=
        elif in1[i] == 'u' and in2[i] == '=' and in3[i] == 'u' and out[i] == '=':
            cin2[i] = '0'
        # u=n=
        elif in1[i] == 'u' and in2[i] == '=' and in3[i] == 'n' and out[i] == '=':
            cin2[i] = '1'
        # uu=u
        elif in1[i] == 'u' and in2[i] == 'u' and in3[i] == '=' and out[i] == 'u':
            cin3[i] = '0'
        # =unn
        elif in1[i] == '=' and in2[i] == 'u' and in3[i] == 'n' and out[i] == 'n':
            cin1[i] = '0'
        # u=nn
        elif in1[i] == 'u' and in2[i] == '=' and in3[i] == 'n' and out[i] == 'n':
            cin2[i] = '0'
        # =nuu
        elif in1[i] == '=' and in2[i] == 'n' and in3[i] == 'u' and out[i] == 'u':
            cin1[i] = '0'
        # u=uu
        elif in1[i] == 'u' and in2[i] == '=' and in3[i] == 'u' and out[i] == 'u':
            cin2[i] = '1'
        # n=uu
        elif in1[i] == 'n' and in2[i] == '=' and in3[i] == 'u' and out[i] == 'u':
            cin2[i] = '0'
        # nu=u
        elif in1[i] == 'n' and in2[i] == 'u' and in3[i] == '=' and out[i] == 'u':
            cin3[i] = '1'
        # un=n
        elif in1[i] == 'u' and in2[i] == 'n' and in3[i] == '=' and out[i] == 'n':
            cin3[i] = '1'
        # =unu
        elif in1[i] == '=' and in2[i] == 'u' and in3[i] == 'n' and out[i] == 'u':
            cin1[i] = '1'
        # nn=n
        elif in1[i] == 'n' and in2[i] == 'n' and in3[i] == '=' and out[i] == 'n':
            cin3[i] = '0'
        # =nun
        elif in1[i] == '=' and in2[i] == 'n' and in3[i] == 'u' and out[i] == 'n':
            cin1[i] = '1'
        # n=nn
        elif in1[i] == 'n' and in2[i] == '=' and in3[i] == 'n' and out[i] == 'n':
            cin2[i] = '1'
        # u===
        elif (in1[i] == 'u' or in1[i] == 'n') and (in2[i] == '=' and cin2[i] == '1') and in3[i] == '=' and out[
            i] == '=':
            cin3[i] = '1'
        elif (in1[i] == 'u' or in1[i] == 'n') and (in2[i] == '=' and cin2[i] == '0') and in3[i] == '=' and out[
            i] == '=':
            cin3[i] = '0'
        elif (in1[i] == 'u' or in1[i] == 'n') and cin2[i] == '=' and (in3[i] == '=' and cin3[i] == '1') and out[
            i] == '=':
            cin2[i] = '1'
        elif (in1[i] == 'u' or in1[i] == 'n') and cin2[i] == '=' and (in3[i] == '=' and cin3[i] == '0') and out[
            i] == '=':
            cin2[i] = '0'
        elif (in1[i] == 'u' or in1[i] == 'n') and (in2[i] == '=' and (cin2[i] == '=' or cin2[i] == '+')) and (
                in3[i] == '=' and (cin3[i] == '=' or cin3[i] == '+')) and out[i] == '=':
            cin2[i] = '+'
            cin3[i] = '+'
    for i in range(32):
        if cin4[i] == "+" and cin3[i] in ["0", "1"]:
            cin4[i] = cin3[i]
    return cin1, cin2, cin3, cin4


def Exor(x, z, cx, cy, cz):
    for i in range(32):
        ix = (6 + i) % 32
        iy = (11 + i) % 32
        iz = (25 + i) % 32
        # n==n==> n11n,n00n,n==u===>n10u,n01u
        if x[ix] == "n" and cx[iy] == "1" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "n":

            if cx[iz] == "=":
                cx[iz] = "1"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "1"
                    cz[iz] = "1"
                    cx[iz] = "1"
        elif x[ix] == "n" and cx[iy] == "0" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "n":

            if cx[iz] == "=":
                cx[iz] = "0"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "0"
                    cz[iz] = "0"
                    cx[iz] = "0"
        elif x[ix] == "n" and (cx[iy] == "=" or cx[iy] == "+") and cx[iz] == "1" and z[i] == "n":

            if cx[iy] == "=":
                cx[iy] = "1"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "1"
                    cy[iy] = "1"
                    cz[iy] = "1"
        elif x[ix] == "n" and (cx[iy] == "=" or cx[iy] == "+") and cx[iz] == "0" and z[i] == "n":
            if cx[iy] == "=":
                cx[iy] = "0"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cy[iy] = "0"
                    cz[iy] = "0"
                    cx[iy] = "0"








        # n==u===>n10u,n01u
        elif x[ix] == "n" and cx[iy] == "1" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "u":

            if cx[iz] == "=":
                cx[iz] = "0"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "0"
                    cz[iz] = "0"
                    cx[iz] = "0"
        elif x[ix] == "n" and cx[iy] == "0" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "u":

            if cx[iz] == "=":
                cx[iz] = "1"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "1"
                    cz[iz] = "1"
                    cx[iz] = "1"
        elif x[ix] == "n" and (cx[iy] == "=" or cx[iy] == "+") and cx[iz] == "1" and z[i] == "u":

            if cx[iy] == "=":
                cx[iy] = "0"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cy[iy] = "0"
                    cz[iy] = "0"
                    cx[iy] = "0"
        elif x[ix] == "n" and (cx[iy] == "=" or cx[iy] == "+") and cx[iz] == "0" and z[i] == "u":

            if cx[iy] == "=":
                cx[iy] = "1"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "1"
                    cy[iy] = "1"
                    cz[iy] = "1"







        elif x[ix] == "u" and cx[iy] == "1" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "u":

            if cx[iz] == "=":
                cx[iz] = "1"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "1"
                    cz[iz] = "1"
                    cx[iz] = "1"
        elif x[ix] == "u" and cx[iy] == "0" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "u":

            if cx[iz] == "=":
                cx[iz] = "0"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "0"
                    cz[iz] = "0"
                    cx[iz] = "0"
        elif x[ix] == "u" and (cx[iy] == "=" or cx[iy] == "+") and cx[iz] == "1" and z[i] == "u":

            if cx[iy] == "=":
                cx[iy] = "1"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "1"
                    cy[iy] = "1"
                    cz[iy] = "1"
        elif x[ix] == "u" and (cx[iy] == "=" or cx[iy] == "+") and cx[iz] == "0" and z[i] == "u":

            if cx[iy] == "=":
                cx[iy] = "0"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cy[iy] = "0"
                    cz[iy] = "0"
                    cx[iy] = "0"




        elif x[ix] == "u" and cx[iy] == "1" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "n":

            if cx[iz] == "=":
                cx[iz] = "0"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "0"
                    cz[iz] = "0"
                    cx[iz] = "0"
        elif x[ix] == "u" and cx[iy] == "0" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "n":

            if cx[iz] == "=":
                cx[iz] = "1"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "1"
                    cz[iz] = "1"
                    cx[iz] = "1"
        elif x[ix] == "u" and (cx[iy] == "=" or cx[iy] == "+") and cx[iz] == "1" and z[i] == "n":

            if cx[iy] == "=":
                cx[iy] = "0"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cy[iy] = "0"
                    cz[iy] = "0"
                    cx[iy] = "0"
        elif x[ix] == "u" and (cx[iy] == "=" or cx[iy] == "+") and cx[iz] == "0" and z[i] == "n":

            if cx[iy] == "=":
                cx[iy] = "1"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "1"
                    cy[iy] = "1"
                    cz[iy] = "1"





        # =n=n
        elif cx[ix] == "1" and x[iy] == "n" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "n":

            if cx[iz] == "=":
                cx[iz] = "1"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "1"
                    cz[iz] = "1"
                    cx[iz] = "1"
        elif cx[ix] == "0" and x[iy] == "n" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "n":

            if cx[iz] == "=":
                cx[iz] = "0"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "0"
                    cz[iz] = "0"
                    cx[iz] = "0"
        ## =n=n
        elif (cx[ix] == "=" or cx[ix] == "+") and x[iy] == "n" and cx[iz] == "1" and z[i] == "n":

            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"
        elif (cx[ix] == "=" or cx[ix] == "+") and x[iy] == "n" and cx[iz] == "0" and z[i] == "n":
            if cx[ix] == "=":
                cx[ix] = "0"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cy[ix] = "0"
                    cz[ix] = "0"
                    cx[ix] = "0"







        elif cx[ix] == "1" and x[iy] == "n" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "u":

            if cx[iz] == "=":
                cx[iz] = "0"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "0"
                    cz[iz] = "0"
                    cx[iz] = "0"
        elif cx[ix] == "0" and x[iy] == "n" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "u":

            if cx[iz] == "=":
                cx[iz] = "1"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "1"
                    cz[iz] = "1"
                    cx[iz] = "1"

        elif (cx[ix] == "=" or cx[ix] == "+") and x[iy] == "n" and cx[iz] == "1" and z[i] == "u":

            if cx[ix] == "=":
                cx[ix] = "0"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cy[ix] = "0"
                    cz[ix] = "0"
                    cx[ix] = "0"
            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"
        elif (cx[ix] == "=" or cx[ix] == "+") and x[iy] == "n" and cx[iz] == "0" and z[i] == "u":
            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "=" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"



        elif cx[ix] == "1" and x[iy] == "u" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "u":

            if cx[iz] == "=":
                cx[iz] = "1"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "1"
                    cz[iz] = "1"
                    cx[iz] = "1"
        elif cx[ix] == "0" and x[iy] == "u" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "u":

            if cx[iz] == "=":
                cx[iz] = "0"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "0"
                    cz[iz] = "0"
                    cx[iz] = "0"

        elif (cx[ix] == "=" or cx[ix] == "+") and x[iy] == "u" and cx[iz] == "1" and z[i] == "u":

            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"

        elif (cx[ix] == "=" or cx[ix] == "+") and x[iy] == "u" and cx[iz] == "0" and z[i] == "u":
            if cx[ix] == "=":
                cx[ix] = "0"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cy[ix] = "0"
                    cz[ix] = "0"
                    cx[ix] = "0"






        elif cx[ix] == "1" and x[iy] == "u" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "n":

            if cx[iz] == "=":
                cx[iz] = "0"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "0"
                    cx[iz] = "0"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "0"
                    cz[iz] = "0"
                    cx[iz] = "0"
        elif cx[ix] == "0" and x[iy] == "u" and (cx[iz] == "=" or cx[iz] == "+") and z[i] == "n":

            if cx[iz] == "=":
                cx[iz] = "1"
            elif cx[iz] == "+":
                if cy[iz] != "+" and cz[iz] == "+":
                    cz[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] != "+":
                    cy[iz] = "1"
                    cx[iz] = "1"
                elif cy[iz] == "+" and cz[iz] == "+":
                    cy[iz] = "1"
                    cz[iz] = "1"
                    cx[iz] = "1"


        elif (cx[ix] == "=" or cx[ix] == "+") and x[iy] == "u" and cx[iz] == "1" and z[i] == "n":

            if cx[ix] == "=":
                cx[ix] = "0"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cy[ix] = "0"
                    cz[ix] = "0"
                    cx[ix] = "0"

        elif (cx[ix] == "=" or cx[ix] == "+") and x[iy] == "u" and cx[iz] == "0" and z[i] == "n":
            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"






        elif cx[ix] == "1" and (cx[iy] == "=" or cx[iy] == "+") and x[iz] == "n" and z[i] == "n":

            if cx[iy] == "=":
                cx[iy] = "1"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "1"
                    cy[iy] = "1"
                    cz[iy] = "1"
        elif cx[ix] == "0" and (cx[iy] == "=" or cx[iy] == "+") and x[iz] == "n" and z[i] == "n":

            if cx[iy] == "=":
                cx[iy] = "0"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "0"
                    cy[iy] = "0"
                    cz[iy] = "0"


        elif (cx[ix] == "=" or cx[ix] == "+") and cx[iy] == "1" and x[iz] == "n" and z[i] == "n":
            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"


        elif (cx[ix] == "=" or cx[ix] == "+") and cx[iy] == "0" and x[iz] == "n" and z[i] == "n":

            if cx[ix] == "=":
                cx[ix] = "0"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cy[ix] = "0"
                    cz[ix] = "0"
                    cx[ix] = "0"


        elif cx[ix] == "0" and (cx[iy] == "=" or cx[iy] == "+") and x[iz] == "u" and z[i] == "n":

            if cx[iy] == "=":
                cx[iy] = "1"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "1"
                    cy[iy] = "1"
                    cz[iy] = "1"
        elif cx[ix] == "1" and (cx[iy] == "=" or cx[iy] == "+") and x[iz] == "u" and z[i] == "n":

            if cx[iy] == "=":
                cx[iy] = "0"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "0"
                    cy[iy] = "0"
                    cz[iy] = "0"


        elif (cx[ix] == "=" or cx[ix] == "+") and cx[iy] == "0" and x[iz] == "u" and z[i] == "n":

            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"


        elif (cx[ix] == "=" or cx[ix] == "+") and cx[iy] == "1" and x[iz] == "u" and z[i] == "n":

            if cx[ix] == "=":
                cx[ix] = "0"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cy[ix] = "0"
                    cz[ix] = "0"
                    cx[ix] = "0"


        elif cx[ix] == "1" and (cx[iy] == "=" or cx[iy] == "+") and x[iz] == "u" and z[i] == "u":

            if cx[iy] == "=":
                cx[iy] = "1"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "1"
                    cy[iy] = "1"
                    cz[iy] = "1"
        elif cx[ix] == "0" and (cx[iy] == "=" or cx[iy] == "+") and x[iz] == "u" and z[i] == "u":

            if cx[iy] == "=":
                cx[iy] = "0"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "0"
                    cy[iy] = "0"
                    cz[iy] = "0"


        elif (cx[ix] == "=" or cx[ix] == "+") and cx[iy] == "1" and x[iz] == "u" and z[i] == "u":

            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"


        elif cx[ix] in ["=", "+"] and cx[iy] == "0" and x[iz] == "u" and z[i] == "u":

            if cx[ix] == "=":
                cx[ix] = "0"
            elif cx[ix] == "+":
                if cz[ix] == "+" and cy[ix] != "+":
                    cz[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cy[ix] = "0"
                    cz[ix] = "0"
                    cx[ix] = "0"



        elif cx[ix] == "0" and (cx[iy] == "=" or cx[iy] == "+") and x[iz] == "n" and z[i] == "u":

            if cx[iy] == "=":
                cx[iy] = "1"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "1"
                    cx[iy] = "1"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "1"
                    cy[iy] = "1"
                    cz[iy] = "1"
        elif cx[ix] == "1" and (cx[iy] == "=" or cx[iy] == "+") and x[iz] == "n" and z[i] == "u":

            if cx[iy] == "=":
                cx[iy] = "0"
            elif cx[iy] == "+":
                if cy[iy] != "+" and cz[iy] == "+":
                    cz[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] != "+":
                    cy[iy] = "0"
                    cx[iy] = "0"
                elif cy[iy] == "+" and cz[iy] == "+":
                    cx[iy] = "0"
                    cy[iy] = "0"
                    cz[iy] = "0"


        elif (cx[ix] == "+" or cx[ix] == "=") and cx[iy] == "0" and x[iz] == "n" and z[i] == "u":

            if cx[ix] == "=":
                cx[ix] = "1"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "1"
                    cx[ix] = "1"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cx[ix] = "1"
                    cy[ix] = "1"
                    cz[ix] = "1"


        elif (cx[ix] == "=" or cx[ix] == "+") and cx[iy] == "1" and x[iz] == "n" and z[i] == "u":
            if cx[ix] == "=":
                cx[ix] = "0"
            elif cx[ix] == "+":
                if cy[ix] != "+" and cz[ix] == "+":
                    cz[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] != "+":
                    cy[ix] = "0"
                    cx[ix] = "0"
                elif cy[ix] == "+" and cz[ix] == "+":
                    cy[ix] = "0"
                    cz[ix] = "0"
                    cx[ix] = "0"


    return cx, cy, cz
