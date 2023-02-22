import numpy as np
import math as math
import matplotlib.pyplot as plt


def hole_af(file1,file2,chord,r,xloc):
    f = open(file1, "r")
    fn = open(file2, "w+")

    L = f.readlines()
    s = len(L) #number of coords

    xpoints = [1]*s
    ypoints = [1]*s

    for i in range(s): 
        if i != 0: 
            q = str.split(L[i])
            if len(q) > 1:
                xpoints[i] = float(q[0])
                ypoints[i] = float(q[1])

    #locate closest x coord to xloc on lower surface
    half = math.floor(s/2) +1
    index = half + abs(np.asarray(xpoints[half:s -1]) - xloc).argmin() #index lower surf at quarter chord

    height = abs(ypoints[index] - ypoints[index-half])
    #define the points for our hole
    c = chord #wing chord
    diff =  height/2 - r#distance from edge of circle to surface of af
    x_offset = c*xpoints[index] #xloc of circle
    y_offset =  c*ypoints[index] + diff #yloc of circle
    c_res = 16 #number of points along circle
    xpc=[1]*c_res
    ypc=[1]*c_res
    for j in range(c_res):
        xpc[j] = x_offset - r*math.cos(2*math.pi/(c_res-1)*j + math.pi/2) #start from lower point of circle
        ypc[j] = y_offset - r*math.sin(2*math.pi/(c_res-1)*j + math.pi/2)

    #insert points before hole

    for k in range(index+1):
        fn.writelines("  " + "{:.5f}".format((xpoints[k]*chord)) + "  " + "{:.5f}".format((ypoints[k]*chord)) +"\n")

    fn.writelines("  " + "{:.5f}".format((xpoints[index])) + "  " + "{:.5f}".format((ypoints[index])) +"\n")
    #insert circle
    for l in range(len(xpc)):
        fn.writelines("  " + "{:.5f}".format((xpc[l])) + "  " + "{:.5f}".format((ypc[l])) +"\n")

    #insert rest of foil
    fn.writelines("  " + "{:.5f}".format((xpoints[index]*chord)) + "  " + "{:.5f}".format((ypoints[index]*chord)) +"\n")
    for m in range(s-index):
        fn.writelines("  " + "{:.5f}".format((xpoints[m+index]*chord)) + "  " + "{:.5f}".format((ypoints[m+index]*chord)) +"\n")



file1 = input("Enter filename of airfoil: ")
file2 = input("Enter filename of new airfoil: ")
chord = float(input("Enter chord of new airfoil: "))
r = float(input("Enter radius of circular hole desired: "))
xloc = float(input("Enter the xloc of the hole (from 0 to 1: "))

hole_af(file1,file2,chord,r,xloc)