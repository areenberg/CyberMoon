import math

def defineColors(name):

    if name=="red":
        color = (255,0,0)
    elif name=="lightred":
        color = (202,63,63)
    elif name=="green":
        color = (0,255,0)
    elif name=="darkGreen":
        color = (0,60,0)
    elif name=="darkMagenta":
        color = (204, 0, 102)
    elif name=="blue":
        color = (0,0,255)
    elif name=="darkBlue":
        color = (0,0,128)
    elif name=="white":
        color = (255,255,255)
    elif name=="black":
        color = (0,0,0)
    elif name=="pink":
        color = (255,153,204)
    elif name=="levelBackground":
        color = (0,40,100)
    elif name=="playerColor":
        color = (250,255,0)

    else:
        print("Color is not indexed.")
    return color


def glow(temp,lifeTime):
    #grenade color

    lft = lifeTime+1
    red = 255*1.01**(-lft+temp)
    green = 128*1.8**(-lft+temp)
    color = (int(math.floor(red)),int(math.floor(green)),0)

    return color


def cool(temp):
    #cooling of shrap metal

    red = 255-150*1.2**(-temp)
    green = 128-60*1.01**(-temp)
    blue = max(0,(240-red))
    color = (math.floor(red),math.floor(green),math.floor(blue))

    return color


def enemyColor(wingAngle,colout,colin):
    #color of enemies
    #takes wingAngle as fraction
    if wingAngle<0:
        wingAngle = 0
    wa = [1.0140000000000027,0.0]
    a = [0]*3
    for i in range(3):
        alpha = (colout[i]-colin[i])/(wa[0]-wa[1])
        beta = colout[i]-alpha*wa[0]
        a[i] = wingAngle*alpha+beta
    color = (a[0],a[1],a[2])
    return color
