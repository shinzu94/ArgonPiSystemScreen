#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import logging
import spidev as SPI
from gpiozero import CPUTemperature
import signal


from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont
import datetime
import psutil


# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)


def DrawProcentBar(leftSide, rightSide, top, bottom, mid, width, height, part, background, border=2, showLine=True):
    draw.line([(leftSide, bottom), (rightSide, bottom)], fill=background, width=border)
    draw.line([(leftSide, top), (rightSide, top)], fill=background, width=border)
    draw.line([(leftSide, top), (leftSide, bottom)], fill=background, width=border)
    draw.line([(rightSide, top), (rightSide, bottom)], fill=background, width=border)
    if showLine:
        draw.line([(leftSide+border, mid), (leftSide+border + int((width-border*2) * part), mid)], fill=background, width=height)


def barWithText(leftSide, rightSide, top, bottom, mid, width, height, part, text, leftMargin, topMargin, color, font, background, showLine=True):
    DrawProcentBar(leftSide, rightSide, top, bottom, mid, width, height, part, background, 2, showLine)
    draw.text((leftSide+leftMargin, top + topMargin), text, fill=color, font=font)

def offSys(signum, frm):
    image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image1)

    for i in range(0, 3):
        draw.line([(0, 0), (disp.width, disp.width)], fill="BLACK", width=(int(disp.width)))
        Font4 = ImageFont.truetype(directPath + "/Font/Font02.ttf", 40)
        draw.text((75, disp.height/2-20), "Narazie", fill="YELLOW", font=Font4)

        if (i % 2 == 0):
            draw.arc((1, 1, 239, 239), 0, 360, fill="YELLOW")
            draw.arc((2, 2, 238, 238), 0, 360, fill="YELLOW")
            draw.arc((3, 3, 237, 237), 0, 360, fill="YELLOW")
            draw.arc((4, 4, 236, 236), 0, 360, fill="YELLOW")
            draw.arc((5, 5, 235, 235), 0, 360, fill="YELLOW")

        im_r = image1.rotate(rotate)
        disp.ShowImage(im_r)
        time.sleep(0.5)

    draw.line([(0, 0), (disp.width, disp.width)], fill="BLACK", width=(int(disp.width)))
    im_r = image1.rotate(rotate)
    disp.ShowImage(im_r)

    disp.module_exit()
    exit(200)

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch28.LCD_1inch28()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    directPath = "/home/pi/sambashare/ekranik"


    # draw.text((40, 50), 'WaveShare', fill = (128,255,128),font=Font2)
    rotate = 270
    tempMin = 30
    tempMax = 80
    lineWidth = 140
    leftSide = int(disp.width/2-lineWidth/2)
    rightSide = int(disp.width/2+lineWidth/2)
    lineHeight = 30
    tempTop = 138
    tempMid = tempTop + int(lineHeight / 2)
    tempBottom = tempTop + lineHeight

    ramTop = 105
    ramMid = ramTop + int(lineHeight / 2)
    ramBottom = ramTop + lineHeight
    ramCrit = 0.85


    cpuTop = 72
    cpuMid = cpuTop + int(lineHeight / 2)
    cpuBottom = cpuTop + lineHeight
    cpuCrit = 0.95
    cpuTempCrit = 0.8125

    diskCrit = 0.8

    a_funTemp = dict()
    f = open("/etc/argononed.conf", "r")
    cnt = 1
    line = f.readline()
    while line:
        if (line.strip()[0] != "#"):
            tmpArr = line.strip().split('=')
            a_funTemp[tmpArr[0]] = tmpArr[1]
        line = f.readline()
        cnt += 1
    f.close()

    diskTop = 38
    diskMid = diskTop + int(lineHeight / 2)
    diskBottom = diskTop + lineHeight



    Font1 = ImageFont.truetype(directPath + "/Font/Font01.ttf", 25)
    Font2 = ImageFont.truetype(directPath + "/Font/Font01.ttf", 35)
    Font3 = ImageFont.truetype(directPath + "/Font/Font02.ttf", 22)
    Font4 = ImageFont.truetype(directPath + "/Font/Font02.ttf", 40)
    Font5 = ImageFont.truetype(directPath + "/Font/Font02.ttf", 18)


    signal.signal(signal.SIGINT, offSys)
    # signal.signal(signal.SIGKILL, offSys)
    signal.signal(signal.SIGHUP, offSys)
    signal.signal(signal.SIGTERM, offSys)
    # signal.signal(signal.SIGSTOP, offSys)
    image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    for i in range(0, 8):
        draw.line([(0, 0), (disp.width, disp.width)], fill="BLACK", width=(int(disp.width)))
        draw.text((36, disp.height/2-20), "Siemaneczko", fill="YELLOW", font=Font4)
        if (i % 2 == 0):
            draw.arc((1, 1, 239, 239), 0, 360, fill="YELLOW")
            draw.arc((2, 2, 238, 238), 0, 360, fill="YELLOW")
            draw.arc((3, 3, 237, 237), 0, 360, fill="YELLOW")
            draw.arc((4, 4, 236, 236), 0, 360, fill="YELLOW")
            draw.arc((5, 5, 235, 235), 0, 360, fill="YELLOW")
        im_r = image1.rotate(rotate)
        disp.ShowImage(im_r)
        time.sleep(0.5)

    showCrit = True
    while True:
        draw.line([(0, 0), (disp.width, disp.width)], fill="BLACK", width=(int(disp.width)))

        now = datetime.datetime.now()

        hour = now.strftime("%H")
        minets = now.strftime("%M")

        disk = psutil.disk_usage('/')
        diskPercent = disk.percent
        diskUsed = round(disk.used/1024/1024/1024, 1)
        diskTotal = round(disk.total/1024/1024/1024, 1)

        barWithText(leftSide,
                    rightSide,
                    diskTop,
                    diskBottom,
                    diskMid,
                    lineWidth,
                    lineHeight,
                    diskPercent/100,
                    str(diskUsed)+" / "+str(diskTotal)+"GB",
                    2,
                    2,
                    "WHITE",
                    Font3,
                    "PURPLE",
                    (showCrit or diskCrit > diskPercent/100))

        cpuPercent = psutil.cpu_percent(interval=1)
        barWithText(leftSide,
                    rightSide,
                    cpuTop,
                    cpuBottom,
                    cpuMid,
                    lineWidth,
                    lineHeight,
                    cpuPercent/100,
                    str(cpuPercent)+"%",
                    50,
                    2,
                    "WHITE",
                    Font3,
                    "GREEN",
                    (showCrit or cpuCrit > cpuPercent/100))

        memory = psutil.virtual_memory()
        ramTotal = memory.total
        ramAvailable = memory.available
        ramUsed = ramTotal - ramAvailable
        ramPercent = memory.percent
        barWithText(leftSide,
                    rightSide,
                    ramTop,
                    ramBottom,
                    ramMid,
                    lineWidth,
                    lineHeight,
                    ramPercent/100,
                    str(round(ramUsed/1024/1024/1024, 1))+" / "+str(round(ramTotal/1024/1024/1024, 1))+"GB",
                    20,
                    2,
                    "WHITE",
                    Font3,
                    "BLUE",
                    (showCrit or ramCrit > ramPercent/100))


        cpu = CPUTemperature()
        cpuTemp = cpu.temperature
        tempFloat = (cpuTemp-tempMin)/(tempMax-tempMin)
        barWithText(leftSide,
                    rightSide,
                    tempTop,
                    tempBottom,
                    tempMid,
                    lineWidth,
                    lineHeight,
                    tempFloat,
                    str(round(cpuTemp, 1)) + " / " + str(tempMax) + "°C",
                    20,
                    2,
                    "WHITE",
                    Font3,
                    "RED",
                    (showCrit or cpuTempCrit > tempFloat))

        lastTempFun = 0
        lastPercentFun = 0
        for tempFun in a_funTemp:
            if (int(lastTempFun) <= int(tempFun) and int(tempFun) <= int(cpuTemp)):
                lastTempFun = tempFun
                lastPercentFun = int(a_funTemp[tempFun])

        funAxis = 360*(lastPercentFun/100)

        draw.arc((5, 5, 235, 235), -rotate/3, funAxis-(rotate/3), fill="YELLOW")
        draw.arc((6, 6, 234, 234), -rotate/3, funAxis-(rotate/3), fill="YELLOW")
        draw.arc((7, 7, 233, 233), -rotate/3, funAxis-(rotate/3), fill="YELLOW")

        fullClock = 60*24
        partClock = float(hour)*60 + float(minets)

        partOfTimeArc = partClock/fullClock;
        timeAxis = int(360 * partOfTimeArc)

        draw.text((52, 165), str(now.strftime("%H:%M:%S")), fill="WHITE", font=Font4)
        draw.text((73, 15), str(now.strftime("%d/%m/%Y")), fill="WHITE", font=Font5)
        draw.arc((1, 1, 239, 239), -rotate/3, timeAxis-(rotate/3), fill="WHITE")
        draw.arc((2, 2, 238, 238), -rotate/3, timeAxis-(rotate/3), fill="WHITE")
        draw.arc((3, 3, 237, 237), -rotate/3, timeAxis-(rotate/3), fill="WHITE")
        im_r = image1.rotate(rotate)
        disp.ShowImage(im_r)
        showCrit = not showCrit
        # time.sleep(1)
    time.sleep(3)
    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()