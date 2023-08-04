#!/usr/bin/python3
#-*-encoding:utf8-*-




import os
import math
import tkinter as tk
from tkinter import ttk


PI = 3.141592653589793

# 距离
METER_NMI = 1852.0
METER_YD = 0.91440183

METER_FT = 3.2808398950131
METER_IN = METER_FT * 12.0
METER_FM = METER_FT / 6.0
METER_MI = METER_FT / 6.0 / 880.0

METER_CHI = 0.3333333333333333

# 重量
KG_CT = 5000.0
KG_LB = 2.2046226218488
KG_OZ = 35.2739619

# 温度 (开氏度K)
T_FACTOR = 273.15
T_K_R = 1.8    #兰氏度
T_K_RE = 1.25  #列氏度

# 速度
LIGHT_SPEED = 299792458
MACH_SPEED = 340.3




# 
def toInt(value):
    
    val = 0
    try:
        val = int(value)
    except:
        pass
    
    return val

def toReal(value):
    
    val = 0.0
    try:
        val = float(value)
    except:
        pass
    
    return val
        
def toBool(value):

    val = False
    try:
        val = bool(value)
    except:
        pass
    
    return val
   


class LabelValue(tk.Label):
    
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.bind("<Button-3>", self.onPopupMenu) 
        
    def onPopupMenu(self, event):
        
        self._menu = tk.Menu(self, tearoff=False)
        self._menu.add_command(label="复制", command=self.onCopy)
        self._menu.post(event.x_root, event.y_root)
        
    def onCopy(self):
        
        self.clipboard_clear()
        self.clipboard_append(self.cget("text"))
        self._menu.grab_release()
        self._menu = None
        



class SubFrame(tk.Frame):

    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "距离转换"
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("千米", "km"), ("米", "m"), ("分米", "dm"), ("厘米", "cm"), ("毫米", "mm"), ("微米", "um"), ("纳米", "nm"), ("皮米", "pm"),
                 ("码", "yd"), ("海里", "nmi"), ("英里", "mi"), ("英寻", "fm"), ("英尺", "ft"), ("英寸", "in"),
                 ("里", "里"), ("丈", "丈"), ("尺", "尺"), ("寸", "寸"), ("分", "分"), ("厘", "厘"), ("毫", "毫")]
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="距离:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(1)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(6, 0), pady=(10, 0), sticky=tk.W)
        sel.grid(row=0, column=2, padx=(6, 0), pady=(10, 0), sticky=tk.W)
        btn.grid(row=0, column=3, padx=(6, 0), pady=(10, 0), sticky=tk.W)
        
        self.units = []
        for index in range(len(units)):
            
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            if index < 14:
                row = index + 1
                title.grid(row=row, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
                content.grid(row=row, column=1, padx=(6, 0), pady=(10, 0), sticky=tk.W)
            else:
                row = (index + 1) % 14
                title.grid(row=row, column=2, padx=(30, 0), pady=(10, 0), sticky=tk.E)
                content.grid(row=row, column=3, padx=(6, 0), pady=(10, 0), sticky=tk.W)                
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
        
    def setItemValue(self, item, dValue):
        
        decimal = math.modf(dValue)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(dValue), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(dValue, item["unit"][1])
        else:
            text = "{:.6f} {}".format(dValue, item["unit"][1])
        
        item["value"].set(text)
        
    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())


    def convertValue(self, dValue, unit):
        
        dMeter = 0
        if unit == "千米":
            dMeter = self.convertKM2Meter(dValue)
        elif unit == "米":
            dMeter = self.convertM2Meter(dValue)
        elif unit == "分米":
            dMeter = self.convertDM2Meter(dValue)
        elif unit == "厘米":
            dMeter = self.convertCM2Meter(dValue)
        elif unit == "毫米":
            dMeter = self.convertMM2Meter(dValue)
        elif unit == "微米":
            dMeter = self.convertUM2Meter(dValue)
        elif unit == "纳米":
            dMeter = self.convertNM2Meter(dValue)
        elif unit == "皮米":
            dMeter = self.convertPM2Meter(dValue)
        elif unit == "码":
            dMeter = self.convertYD2Meter(dValue)
        elif unit == "海里":
            dMeter = self.convertNMI2Meter(dValue)
        elif unit == "英里":
            dMeter = self.convertMI2Meter(dValue)
        elif unit == "英寻":
            dMeter = self.convertFM2Meter(dValue)
        elif unit == "英尺":
            dMeter = self.convertFT2Meter(dValue)
        elif unit == "英寸":
            dMeter = self.convertIN2Meter(dValue)
        elif unit == "里":
            dMeter = self.convertLii2Meter(dValue)
        elif unit == "丈":
            dMeter = self.convertZhang2Meter(dValue)
        elif unit == "尺":
            dMeter = self.convertChi2Meter(dValue)
        elif unit == "寸":
            dMeter = self.convertCun2Meter(dValue)
        elif unit == "分":
            dMeter = self.convertFen2Meter(dValue)
        elif unit == "厘":
            dMeter = self.convertLi2Meter(dValue)
        elif unit == "毫":
            dMeter = self.convertHao2Meter(dValue)            
        
        for item in self.units:
            
            dUnitValue = 0
            if item["unit"][0] == "千米":
                dUnitValue = self.convertMeter2KM(dMeter)
            elif item["unit"][0] == "米":
                dUnitValue = self.convertMeter2M(dMeter)
            elif item["unit"][0] == "分米":
                dUnitValue = self.convertMeter2DM(dMeter)
            elif item["unit"][0] == "厘米":
                dUnitValue = self.convertMeter2CM(dMeter)
            elif item["unit"][0] == "毫米":
                dUnitValue = self.convertMeter2MM(dMeter)
            elif item["unit"][0] == "微米":
                dUnitValue = self.convertMeter2UM(dMeter)
            elif item["unit"][0] == "纳米":
                dUnitValue = self.convertMeter2NM(dMeter)
            elif item["unit"][0] == "皮米":
                dUnitValue = self.convertMeter2PM(dMeter)
            elif item["unit"][0] == "码":
                dUnitValue = self.convertMeter2YD(dMeter)
            elif item["unit"][0] == "海里":
                dUnitValue = self.convertMeter2NMI(dMeter)
            elif item["unit"][0] == "英里":
                dUnitValue = self.convertMeter2MI(dMeter)
            elif item["unit"][0] == "英寻":
                dUnitValue = self.convertMeter2FM(dMeter)
            elif item["unit"][0] == "英尺":
                dUnitValue = self.convertMeter2FT(dMeter)
            elif item["unit"][0] == "英寸":
                dUnitValue = self.convertMeter2IN(dMeter)
            elif item["unit"][0] == "里":
                dUnitValue = self.convertMeter2Lii(dMeter)
            elif item["unit"][0] == "丈":
                dUnitValue = self.convertMeter2Zhang(dMeter)
            elif item["unit"][0] == "尺":
                dUnitValue = self.convertMeter2Chi(dMeter)
            elif item["unit"][0] == "寸":
                dUnitValue = self.convertMeter2Cun(dMeter)
            elif item["unit"][0] == "分":
                dUnitValue = self.convertMeter2Fen(dMeter)
            elif item["unit"][0] == "厘":
                dUnitValue = self.convertMeter2Li(dMeter)
            elif item["unit"][0] == "毫":
                dUnitValue = self.convertMeter2Hao(dMeter)                
                
            self.setItemValue(item, dUnitValue)
    
    
    #--
    def convertKM2Meter(self, dKM):
        
        return dKM * 1000.0
    
    def convertM2Meter(self, dM):
        
        return dM
    
    def convertDM2Meter(self, dDM):
        
        return dDM / 10.0
    
    def convertCM2Meter(self, dCM):
        
        return dCM / 100.0
    
    def convertMM2Meter(self, dMM):
        
        return dMM / 1000.0
    
    def convertUM2Meter(self, dUM):
        
        return dUM / 1000.0 / 10.0 ** 3
    
    def convertNM2Meter(self, dNM):
        
        return dNM / 1000.0 / 10.0 ** 6
    
    def convertPM2Meter(self, dPM):
        
        return dPM / 1000.0 / 10.0 ** 9
    
    def convertYD2Meter(self, dYD):
        
        return dYD * METER_YD
    
    def convertNMI2Meter(self, dNMI):
        
        return dNMI * METER_NMI
    
    def convertMI2Meter(self, dMI):
        
        return dMI / METER_MI
    
    def convertFM2Meter(self, dFM):
        
        return dFM / METER_FM
    
    def convertFT2Meter(self, dFT):
        
        return dFT / METER_FT
    
    def convertIN2Meter(self, dIN):
        
        return dIN / METER_IN
    
    def convertLii2Meter(self, dLii):
        
        return dLii * METER_CHI * 10.0 * 150.0
    
    def convertZhang2Meter(self, dZhang):
        
        return dZhang * METER_CHI * 10.0
        
    def convertChi2Meter(self, dChi):
        
        return dChi * METER_CHI
        
    def convertCun2Meter(self, dCun):
        
        return dCun * METER_CHI / 10.0
        
    def convertFen2Meter(self, dFen):
        
        return dFen * METER_CHI / 10.0 ** 2
        
    def convertLi2Meter(self, dLi):
        
        return dLi * METER_CHI / 10.0 ** 3
    
    def convertHao2Meter(self, dHao):
        
        return dHao * METER_CHI / 10.0 ** 4
    
    #--
    def convertMeter2KM(self, dMeter):
        
        return dMeter / 1000.0
    
    def convertMeter2M(self, dMeter):
        
        return dMeter
    
    def convertMeter2DM(self, dMeter):
        
        return dMeter * 10.0
    
    def convertMeter2CM(self, dMeter):
        
        return dMeter * 100.0
    
    def convertMeter2MM(self, dMeter):
        
        return dMeter * 1000.0
    
    def convertMeter2UM(self, dMeter):
        
        return dMeter * 1000.0 * 10.0 ** 3
    
    def convertMeter2NM(self, dMeter):
        
        return dMeter * 1000.0 * 10 ** 6
    
    def convertMeter2PM(self, dMeter):
        
        return dMeter * 1000.0 * 10 ** 9
    
    def convertMeter2YD(self, dMeter):
        
        return dMeter / METER_YD
    
    def convertMeter2NMI(self, dMeter):
        
        return dMeter / METER_NMI
    
    def convertMeter2MI(self, dMeter):
        
        return dMeter * METER_MI
    
    def convertMeter2FM(self, dMeter):
        
        return dMeter * METER_FM
    
    def convertMeter2FT(self, dMeter):
        
        return dMeter * METER_FT
    
    def convertMeter2IN(self, dMeter):
        
        return dMeter * METER_IN
     
    def convertMeter2Lii(self, dMeter):
        
        return dMeter / METER_CHI / 10.0 / 150.0
        
    def convertMeter2Zhang(self, dMeter):
        
        return dMeter / METER_CHI / 10.0
        
    def convertMeter2Chi(self, dMeter):
        
        return dMeter / METER_CHI
        
    def convertMeter2Cun(self, dMeter):
        
        return dMeter / METER_CHI * 10.0
        
    def convertMeter2Fen(self, dMeter):
        
        return dMeter / METER_CHI * 10.0 ** 2
        
    def convertMeter2Li(self, dMeter):
        
        return dMeter / METER_CHI * 10.0 ** 3
        
    def convertMeter2Hao(self, dMeter):
        
        return dMeter / METER_CHI * 10.0 ** 4
        
    
class SubFrame1(tk.Frame):
    
    
    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "时间转换"
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("年", "years"), ("月", "months"), ("周", "weeks"), ("天", "days"), ("小时", "hours"), ("分钟", "minutes"), ("秒", "s"), ("毫秒", "ms"), ("微秒", "us"), ("纳秒", "ns"), ("皮秒", "ps")]
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="时间:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(3)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        sel.grid(row=0, column=2, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        btn.grid(row=0, column=3, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        
        self.units = []
        for index in range(len(units)):
            row = index + 1
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            title.grid(row=row, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
            content.grid(row=row, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W, columnspan=4)            
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
    

    def setItemValue(self, item, value):
        
        decimal = math.modf(value)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(value), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(value, item["unit"][1])
        else:
            text = "{:.6f} {}".format(value, item["unit"][1])
        
        item["value"].set(text)
        
        
    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        

    def convertValue(self, dValue, unit):
        
        dSeconds = 0
        if unit == "年":
            dSeconds = self.convertYears2Seconds(dValue)
        elif unit == "月":
            dSeconds = self.convertMonths2Seconds(dValue)
        elif unit == "周":
            dSeconds = self.convertWeeks2Seconds(dValue)
        elif unit == "天":
            dSeconds = self.convertDays2Seconds(dValue)
        elif unit == "小时":
            dSeconds = self.convertHours2Seconds(dValue)            
        elif unit == "分钟":
            dSeconds = self.convertMinutes2Seconds(dValue)            
        elif unit == "秒":
            dSeconds = self.convertSeconds2Seconds(dValue)            
        elif unit == "毫秒":
            dSeconds = self.convertMilliseconds2Seconds(dValue)            
        elif unit == "微秒":
            dSeconds = self.convertMicroseconds2Seconds(dValue)
        elif unit == "纳秒":
            dSeconds = self.convertNanoseconds2Seconds(dValue)            
        elif unit == "皮秒":
            dSeconds = self.convertPicoseconds2Seconds(dValue)            
            
        for item in self.units:
            
            value = 0
            if item["unit"][0] == "年":
                value = self.convertSeconds2Years(dSeconds)
            elif item["unit"][0] == "月":
                value = self.convertSeconds2Months(dSeconds)
            elif item["unit"][0] == "周":
                value = self.convertSeconds2Weeks(dSeconds)
            elif item["unit"][0] == "天":
                value = self.convertSeconds2Days(dSeconds)
            elif item["unit"][0] == "小时":
                value = self.convertSeconds2Hours(dSeconds)
            elif item["unit"][0] == "分钟":
                value = self.convertSeconds2Minutes(dSeconds)
            elif item["unit"][0] == "秒":
                value = self.convertSeconds2Seconds(dSeconds)
            elif item["unit"][0] == "毫秒":
                value = self.convertSeconds2Milliseconds(dSeconds)
            elif item["unit"][0] == "微秒":
                value = self.convertSeconds2Microseconds(dSeconds)
            elif item["unit"][0] == "纳秒":
                value = self.convertSeconds2Nanoseconds(dSeconds)
            elif item["unit"][0] == "皮秒":
                value = self.convertSeconds2Picoseconds(dSeconds)                
            
            self.setItemValue(item, value)
            
     
    def convertYears2Seconds(self, dYears):
        
        return dYears * 365.0 * 24.0 * 3600.0
    
    def convertMonths2Seconds(self, dMonths):
        
        return dMonths * (365.0 / 12.0) * 24.0 * 3600.0
    
    def convertWeeks2Seconds(self, dWeeks):
        
        return dWeeks * 7.0 * 24.0 * 3600.0    
            
    def convertDays2Seconds(self, dDays):
        
        return dDays * 24.0 * 3600.0
    
    def convertHours2Seconds(self, dHours):
        
        return dHours * 3600.0
    
    def convertMinutes2Seconds(self, dMinutes):
        
        return dMinutes * 60.0
    
    def convertSeconds2Seconds(self, dSeconds):
        
        return dSeconds
    
    def convertMilliseconds2Seconds(self, dMilliseconds):
        
        return dMilliseconds / 10.0 ** 3
    
    def convertMicroseconds2Seconds(self, dMicroseconds):
        
        return dMicroseconds / 10.0 ** 6
    
    def convertNanoseconds2Seconds(self, dNanoseconds):
        
        return dNanoseconds / 10.0 ** 9
    
    def convertPicoseconds2Seconds(self, dPicoseconds):
        
        return dPicoseconds / 10.0 ** 12
    
    #--
    def convertSeconds2Years(self, dSeconds):
        
        return dSeconds / 365.0 / 24.0 / 3600.0    
           
    def convertSeconds2Months(self, dSeconds):
        
        return dSeconds / (365.0 / 12.0) / 24.0 / 3600.0
    
    def convertSeconds2Weeks(self, dSeconds):
        
        return dSeconds / 7.0 / 24.0 / 3600.0
    
    def convertSeconds2Days(self, dSeconds):
        
        return dSeconds / 24.0 / 3600.0
    
    def convertSeconds2Hours(self, dSeconds):
        
        return dSeconds / 3600.0
    
    def convertSeconds2Minutes(self, dSeconds):
        
        return dSeconds / 60.0
    
    def convertSeconds2Milliseconds(self, dSeconds):
        
        return dSeconds * 10.0 ** 3
    
    def convertSeconds2Microseconds(self, dSeconds):
        
        return dSeconds * 10.0 ** 6
    
    def convertSeconds2Nanoseconds(self, dSeconds):
        
        return dSeconds * 10.0 ** 9
    
    def convertSeconds2Picoseconds(self, dSeconds):
        
        return dSeconds * 10.0 ** 12
    

    
    
            
            
class SubFrame2(tk.Frame):
    
    
    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "频率转换"
    
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("千兆赫兹", "GHz"), ("兆赫兹", "MHz"), ("千赫兹", "KHz"), ("赫兹", "Hz")]
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="频率:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(1)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        sel.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))
        btn.grid(row=0, column=3, padx=(10, 0), pady=(10, 0))
        
        self.units = []
        for index in range(len(units)):
            row = index + 1
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            title.grid(row=row, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
            content.grid(row=row, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W, columnspan=4)            
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
    
    
    
    def setItemValue(self, item, value):
        
        decimal = math.modf(value)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(value), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(value, item["unit"][1])
        else:
            text = "{:.6f} {}".format(value, item["unit"][1])
        
        item["value"].set(text)
        
        
    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        

    def convertValue(self, dValue, unit):
        
        dHz = 0
        if unit == "千兆赫兹":
            dHz = self.convertGHz2Hz(dValue)
        elif unit == "兆赫兹":
            dHz = self.convertMHz2Hz(dValue)
        elif unit == "千赫兹":
            dHz = self.convertKHz2Hz(dValue)
        elif unit == "赫兹":
            dHz = self.convertHz2Hz(dValue)            
            
            
        for item in self.units:
            
            value = 0
            if item["unit"][0] == "千兆赫兹":
                value = self.convertHz2GHz(dHz)
            elif item["unit"][0] == "兆赫兹":
                value = self.convertHz2MHz(dHz)
            elif item["unit"][0] == "千赫兹":
                value = self.convertHz2KHz(dHz)
            elif item["unit"][0] == "赫兹":
                value = self.convertHz2Hz(dHz)
                
            self.setItemValue(item, value)
            
            
            
            
    def convertGHz2Hz(self, dGHz):
        
        return dGHz * 10.0 ** 9
    
    def convertMHz2Hz(self, dMHz):
        
        return dMHz * 10.0 ** 6
    
    def convertKHz2Hz(self, dKHz):
        
        return dKHz * 10.0 ** 3
    
    def convertHz2Hz(self, dHz):
        
        return dHz
    
    def convertHz2GHz(self, dHz):
        
        return dHz / 10.0 ** 9
    
    def convertHz2MHz(self, dHz):
        
        return dHz / 10.0 ** 6
    
    def convertHz2KHz(self, dHz):
        
        return dHz / 10.0 ** 3
    
    
    
    
class SubFrame3(tk.Frame):
    
    
    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "功率转换"
    
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("千兆瓦", "Kmw"), ("兆瓦", "Mw"), ("千瓦", "Kw"), ("瓦", "w")]
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="功率:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(1)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        sel.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))
        btn.grid(row=0, column=3, padx=(10, 0), pady=(10, 0))
        
        self.units = []
        for index in range(len(units)):
            row = index + 1
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            title.grid(row=row, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
            content.grid(row=row, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W, columnspan=4)            
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
    
    
    def setItemValue(self, item, value):
        
        decimal = math.modf(value)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(value), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(value, item["unit"][1])
        else:
            text = "{:.6f} {}".format(value, item["unit"][1])
        
        item["value"].set(text)
        

    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
        
    def convertValue(self, dValue, unit):
        
        dW = 0
        if unit == "千兆瓦":
            dW = self.convertKmw2W(dValue)        
        elif unit == "兆瓦":
            dW = self.convertMw2W(dValue)
        elif unit == "千瓦":
            dW = self.convertKw2W(dValue)
        elif unit == "瓦":       
            dW = self.convertW2W(dValue)         
            
            
        for item in self.units:
            
            value = 0
            if item["unit"][0] == "千兆瓦":
                value = self.convertW2Kmw(dW)            
            elif item["unit"][0] == "兆瓦":
                value = self.convertW2Mw(dW)
            elif item["unit"][0] == "千瓦":
                value = self.convertW2Kw(dW)
            elif item["unit"][0] == "瓦":
                value = self.convertW2W(dW)
      
                
            self.setItemValue(item, value)
            
            
    def convertKmw2W(self, dKmw):
        
        return dKmw * 10.0 ** 9
    
    def convertMw2W(self, dMw):
        
        return dMw * 10.0 ** 6
    
    def convertKw2W(self, dKw):
        
        return dKw * 10.0 ** 3
    
    def convertW2W(self, dW):
        
        return dW
    
    def convertW2Kmw(self, dW):
        
        return dW / 10.0 ** 9
    
    def convertW2Mw(self, dW):
        
        return dW / 10.0 ** 6
    
    def convertW2Kw(self, dW):
        
        return dW / 10.0 ** 3
            
            
            
        
class SubFrame4(tk.Frame):
    
    
    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "质量转换"
    
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("吨", "t"), ("千克", "Kg"), ("克", "g"), ("毫克", "mg"), ("微克", "ug"),
                 ("克拉", "ct"),
                 ("磅", "lb"), ("盎司", "oz")]
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="功率:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(1)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        sel.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))
        btn.grid(row=0, column=3, padx=(10, 0), pady=(10, 0))
        
        self.units = []
        for index in range(len(units)):
            row = index + 1
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            title.grid(row=row, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
            content.grid(row=row, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W, columnspan=4)            
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
    
    
    def setItemValue(self, item, value):
        
        decimal = math.modf(value)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(value), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(value, item["unit"][1])
        else:
            text = "{:.6f} {}".format(value, item["unit"][1])
        
        item["value"].set(text)
        

    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
        
    def convertValue(self, dValue, unit):
        
        dKg = 0
        if unit == "吨":
            dKg = self.convertT2Kg(dValue)
        elif unit == "千克":
            dKg = self.convertKg2Kg(dValue)
        elif unit == "克":       
            dKg = self.convertG2Kg(dValue)         
        elif unit == "毫克":      
            dKg = self.convertMg2Kg(dValue)
        elif unit == "微克":      
            dKg = self.convertUg2Kg(dValue)
        elif unit == "克拉":      
            dKg = self.convertCt2Kg(dValue)
        elif unit == "磅":      
            dKg = self.convertLb2Kg(dValue)
        elif unit == "盎司":      
            dKg = self.convertOz2Kg(dValue)             
            
        for item in self.units:
            
            value = 0
            if item["unit"][0] == "吨":
                value = self.convertKg2T(dKg)
            elif item["unit"][0] == "千克":
                value = self.convertKg2Kg(dKg)
            elif item["unit"][0] == "克":
                value = self.convertKg2G(dKg)
            elif item["unit"][0] == "毫克":
                value = self.convertKg2Mg(dKg)
            elif item["unit"][0] == "微克":
                value = self.convertKg2Ug(dKg)
            elif item["unit"][0] == "克拉":
                value = self.convertKg2Ct(dKg)
            elif item["unit"][0] == "磅":
                value = self.convertKg2Lb(dKg)
            elif item["unit"][0] == "盎司":
                value = self.convertKg2Oz(dKg)                
                
            self.setItemValue(item, value)            
            
        
        
    
    def convertT2Kg(self, dT):
        
        return dT * 1000.0
    
    def convertKg2Kg(self, dKg):
        
        return dKg
    
    def convertG2Kg(self, dG):
        
        return dG / 10.0 ** 3
    
    def convertMg2Kg(self, dMg):
        
        return dMg / 10.0 ** 6
    
    def convertUg2Kg(self, dUg):
        
        return dUg / 10.0 ** 9
    
    def convertCt2Kg(self, dCt):
        
        return dCt / KG_CT
    
    def convertLb2Kg(self, dLb):
        
        return dLb / KG_LB
    
    def convertOz2Kg(self, dOz):
        
        return dOz / KG_OZ
    
    #--
    def convertKg2T(self, dKg):
        
        return dKg / 1000.0   
    
    def convertKg2G(self, dKg):
        
        return dKg * 1000.0
    
    def convertKg2Mg(self, dKg):
        
        return dKg * 10.0 ** 6
    
    def convertKg2Ug(self, dKg):
        
        return dKg * 10.0 ** 9
    
    def convertKg2Ct(self, dKg):
        
        return dKg * KG_CT
    
    def convertKg2Lb(self, dKg):
        
        return dKg * KG_LB
    
    def convertKg2Oz(self, dKg):
        
        return dKg * KG_OZ
    
    
    

class SubFrame5(tk.Frame):
    
    
    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "存储转换"
    
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("比特", "bit"), ("字节", "B"), ("千字节", "KB"), ("兆字节", "MB"), ("千兆字节", "GB"),
                 ("太字节", "TB"), ("拍字节", "PB"), ("艾字节", "EB")]
        
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="存储:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(1)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        sel.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))
        btn.grid(row=0, column=3, padx=(10, 0), pady=(10, 0))
        
        self.units = []
        for index in range(len(units)):
            row = index + 1
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            title.grid(row=row, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
            content.grid(row=row, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W, columnspan=4)            
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
    
    
    def setItemValue(self, item, value):
        
        decimal = math.modf(value)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(value), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(value, item["unit"][1])
        else:
            text = "{:.6f} {}".format(value, item["unit"][1])
        
        item["value"].set(text)
        

    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
        
    def convertValue(self, dValue, unit):
      
        dSpeed = 0
        if unit == "比特":
            dByte = self.convertBit2Byte(dValue)
        elif unit == "字节":
            dByte = self.convertByte2Byte(dValue)
        elif unit == "千字节":       
            dByte = self.convertKB2Byte(dValue)         
        elif unit == "兆字节":      
            dByte = self.convertMB2Byte(dValue)
        elif unit == "千兆字节":      
            dByte = self.convertGB2Byte(dValue)
        elif unit == "太字节":      
            dByte = self.convertTB2Byte(dValue)
        elif unit == "拍字节":      
            dByte = self.convertPB2Byte(dValue)
        elif unit == "艾字节":      
            dByte = self.convertEB2Byte(dValue)             
            
        for item in self.units:
            
            value = 0
            if item["unit"][0] == "比特":
                value = self.convertByte2Bit(dByte)
            elif item["unit"][0] == "字节":
                value = self.convertByte2Byte(dByte)
            elif item["unit"][0] == "千字节":
                value = self.convertByte2KB(dByte)
            elif item["unit"][0] == "兆字节":
                value = self.convertByte2MB(dByte)
            elif item["unit"][0] == "千兆字节":
                value = self.convertByte2GB(dByte)
            elif item["unit"][0] == "太字节":
                value = self.convertByte2TB(dByte)
            elif item["unit"][0] == "拍字节":
                value = self.convertByte2PB(dByte)
            elif item["unit"][0] == "艾字节":
                value = self.convertByte2EB(dByte)                
                
            self.setItemValue(item, value)          
    
    
    
    
    def convertBit2Byte(self, dBit):
        
        return dBit / 8.0
    
    def convertByte2Byte(self, dByte):
        
        return dByte
    
    def convertKB2Byte(self, dKB):
        
        return dKB * 1024.0
    
    def convertMB2Byte(self, dMB):
        
        return dMB * 1024.0 ** 2
    
    def convertGB2Byte(self, dGB):
        
        return dGB * 1024.0 ** 3
    
    def convertTB2Byte(self, dTB):
        
        return dTB * 1024.0 ** 4
    
    def convertPB2Byte(self, dPB):
        
        return dPB * 1024.0 ** 5
    
    def convertEB2Byte(self, dEB):
        
        return dEB * 1024.0 ** 6
    
    #
    def convertByte2Bit(self, dByte):
        
        return dByte * 8.0
    
    def convertByte2KB(self, dByte):
        
        return dByte / 1024.0
    
    def convertByte2MB(self, dByte):
        
        return dByte / 1024.0 ** 2
    
    def convertByte2GB(self, dByte):
        
        return dByte / 1024.0 ** 3
    
    def convertByte2TB(self, dByte):
        
        return dByte / 1024.0 ** 4
    
    def convertByte2PB(self, dByte):
        
        return dByte / 1024.0 ** 5
    
    def convertByte2EB(self, dByte):
        
        return dByte / 1024.0 ** 6
    
    
    
    
class SubFrame6(tk.Frame):
    
    
    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "速度转换"
    
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("千米/时", "Km/h"), ("千米/秒", "Km/s"), ("米/时", "m/h"), ("米/秒", "m/s"),
                 ("海里/时", "nmi/h"), ("海里/秒", "nmi/s"), ("码/时", "yd/h"), ("码/秒", "yd/s"),
                 ("英里/时", "mi/h"), ("英里/秒", "mi/s"), ("英尺/时", "ft/h"), ("英尺/秒", "ft/s"),
                 ("英寸/时", "in/h"), ("英寸/秒", "in/s"), ("光速", "c"), ("马赫", "mach")]
        
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="速度:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(0)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        sel.grid(row=0, column=2, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        btn.grid(row=0, column=3, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        
        self.units = []
        for index in range(len(units)):
            row = index % 8 + 1
            col = index // 8 * 2
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            title.grid(row=row, column=col + 0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
            content.grid(row=row, column=col + 1, padx=(10, 0), pady=(10, 0), sticky=tk.W)            
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
    
    
    def setItemValue(self, item, value):
        
        decimal = math.modf(value)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(value), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(value, item["unit"][1])
        else:
            text = "{:.6f} {}".format(value, item["unit"][1])
        
        item["value"].set(text)
        

    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
        
    def convertValue(self, dValue, unit):
      
        dSpeed = 0 # m/s
        if unit == "千米/时":
            dSpeed = self.convertKmh2Speed(dValue)
        elif unit == "千米/秒":
            dSpeed = self.convertKms2Speed(dValue)
        elif unit == "米/时":       
            dSpeed = self.convertMh2Speed(dValue)         
        elif unit == "米/秒":      
            dSpeed = self.convertMs2Speed(dValue)
        elif unit == "海里/时":      
            dSpeed = self.convertNmih2Speed(dValue)
        elif unit == "海里/秒":      
            dSpeed = self.convertNmis2Speed(dValue)
        elif unit == "码/时":      
            dSpeed = self.convertYdh2Speed(dValue)
        elif unit == "码/秒":      
            dSpeed = self.convertYds2Speed(dValue)            
        elif unit == "英里/时":      
            dSpeed = self.convertMih2Speed(dValue)
        elif unit == "英里/秒":      
            dSpeed = self.convertMis2Speed(dValue)
        elif unit == "英尺/时":      
            dSpeed = self.convertFth2Speed(dValue)
        elif unit == "英尺/秒":      
            dSpeed = self.convertFts2Speed(dValue)            
        elif unit == "英寸/时":      
            dSpeed = self.convertInh2Speed(dValue)
        elif unit == "英寸/秒":      
            dSpeed = self.convertIns2Speed(dValue)
        elif unit == "光速":      
            dSpeed = self.convertC2Speed(dValue)
        elif unit == "马赫":      
            dSpeed = self.convertMach2Speed(dValue)            
            
            
        for item in self.units:
            
            value = 0
            if item["unit"][0] == "千米/时":
                value = self.convertSpeed2Kmh(dSpeed)
            elif item["unit"][0] == "千米/秒":
                value = self.convertSpeed2Kms(dSpeed)
            elif item["unit"][0] == "米/时":
                value = self.convertSpeed2Mh(dSpeed)
            elif item["unit"][0] == "米/秒":
                value = self.convertSpeed2Ms(dSpeed)
            elif item["unit"][0] == "海里/时":
                value = self.convertSpeed2Nmih(dSpeed)
            elif item["unit"][0] == "海里/秒":
                value = self.convertSpeed2Nmis(dSpeed)
            elif item["unit"][0] == "码/时":
                value = self.convertSpeed2Ydh(dSpeed)
            elif item["unit"][0] == "码/秒":
                value = self.convertSpeed2Yds(dSpeed)                
            elif item["unit"][0] == "英里/时":
                value = self.convertSpeed2Mih(dSpeed)
            elif item["unit"][0] == "英里/秒":
                value = self.convertSpeed2Mis(dSpeed)
            elif item["unit"][0] == "英尺/时":
                value = self.convertSpeed2Fth(dSpeed)
            elif item["unit"][0] == "英尺/秒":
                value = self.convertSpeed2Fts(dSpeed)                
            elif item["unit"][0] == "英寸/时":
                value = self.convertSpeed2Inh(dSpeed)
            elif item["unit"][0] == "英寸/秒":
                value = self.convertSpeed2Ins(dSpeed)
            elif item["unit"][0] == "光速":
                value = self.convertSpeed2C(dSpeed)
            elif item["unit"][0] == "马赫":
                value = self.convertSpeed2Mach(dSpeed)                   
                
            self.setItemValue(item, value)          
    
    
    def convertKmh2Speed(self, dSpeed):
        
        return dSpeed * 1000.0 / 3600.0 
 
    def convertKms2Speed(self, dSpeed):
        
        return dSpeed * 1000.0

    def convertMh2Speed(self, dSpeed):
        
        return dSpeed * 3600.0

    def convertMs2Speed(self, dSpeed):
        
        return dSpeed

    def convertNmih2Speed(self, dSpeed):
        
        return dSpeed * METER_NMI / 3600.0

    def convertNmis2Speed(self, dSpeed):
        
        return dSpeed * METER_NMI
    
    def convertYdh2Speed(self, dSpeed):
        
        return dSpeed * METER_YD / 3600.0

    def convertYds2Speed(self, dSpeed):
        
        return dSpeed * METER_YD

    def convertMih2Speed(self, dSpeed):
        
        return dSpeed / METER_MI / 3600.0
  
    def convertMis2Speed(self, dSpeed):
        
        return dSpeed / METER_MI
    
    def convertFth2Speed(self, dSpeed):
        
        return dSpeed / METER_FT / 3600.0

    def convertFts2Speed(self, dSpeed):
        
        return dSpeed / METER_FT    
  
    def convertInh2Speed(self, dSpeed):
        
        return dSpeed / METER_IN / 3600.0

    def convertIns2Speed(self, dSpeed):
        
        return dSpeed / METER_IN

    def convertC2Speed(self, dSpeed):
        
        return dSpeed * LIGHT_SPEED

    def convertMach2Speed(self, dSpeed):
        
        return dSpeed * MACH_SPEED    
    
    #--
    def convertSpeed2Kmh(self, dSpeed):
        
        return dSpeed / 1000.0 * 3600.0
 
    def convertSpeed2Kms(self, dSpeed):
        
        return dSpeed / 1000.0

    def convertSpeed2Mh(self, dSpeed):
        
        return dSpeed / 3600.0

    def convertSpeed2Ms(self, dSpeed):
        
        return dSpeed

    def convertSpeed2Nmih(self, dSpeed):
        
        return dSpeed / METER_NMI * 3600.0

    def convertSpeed2Nmis(self, dSpeed):
        
        return dSpeed / METER_NMI
    
    def convertSpeed2Ydh(self, dSpeed):
        
        return dSpeed / METER_YD * 3600.0

    def convertSpeed2Yds(self, dSpeed):
        
        return dSpeed / METER_YD    

    def convertSpeed2Mih(self, dSpeed):
        
        return dSpeed * METER_MI * 3600.0
  
    def convertSpeed2Mis(self, dSpeed):
        
        return dSpeed * METER_MI
    
    def convertSpeed2Fth(self, dSpeed):
        
        return dSpeed * METER_FT * 3600.0

    def convertSpeed2Fts(self, dSpeed):
        
        return dSpeed * METER_FT    
  
    def convertSpeed2Inh(self, dSpeed):
        
        return dSpeed * METER_IN * 3600.0

    def convertSpeed2Ins(self, dSpeed):
        
        return dSpeed * METER_IN

    def convertSpeed2C(self, dSpeed):
        
        return dSpeed / LIGHT_SPEED

    def convertSpeed2Mach(self, dSpeed):
        
        return dSpeed / MACH_SPEED
    
    
    

class SubFrame7(tk.Frame):
    
    
    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "温度转换"
    
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("摄氏度", "℃"), ("开氏度", "K"), ("列氏度", "°Re"), ("华氏度", "℉"), ("兰氏度", "°R")]
        
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="温度:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(0)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        sel.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))
        btn.grid(row=0, column=3, padx=(10, 0), pady=(10, 0))
        
        self.units = []
        for index in range(len(units)):
            row = index + 1
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            title.grid(row=row, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
            content.grid(row=row, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W, columnspan=4)            
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
    
    
    def setItemValue(self, item, value):
        
        decimal = math.modf(value)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(value), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(value, item["unit"][1])
        else:
            text = "{:.6f} {}".format(value, item["unit"][1])
        
        item["value"].set(text)
        

    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
        
    def convertValue(self, dValue, unit):
      
        dTemperature = 0 # K
        if unit == "摄氏度":
            dTemperature = self.convertShesd2Temperature(dValue)
        elif unit == "开氏度":
            dTemperature = self.convertKaisd2Temperature(dValue)
        elif unit == "列氏度":       
            dTemperature = self.convertLiesd2Temperature(dValue)         
        elif unit == "华氏度":      
            dTemperature = self.convertHuasd2Temperature(dValue)
        elif unit == "兰氏度":      
            dTemperature = self.convertLansd2Temperature(dValue)        
            
            
        for item in self.units:
            
            value = 0
            if item["unit"][0] == "摄氏度":
                value = self.convertTemperature2Shesd(dTemperature)
            elif item["unit"][0] == "开氏度":
                value = self.convertTemperature2Kaisd(dTemperature)
            elif item["unit"][0] == "列氏度":
                value = self.convertTemperature2Liesd(dTemperature)
            elif item["unit"][0] == "华氏度":
                value = self.convertTemperature2Huasd(dTemperature)
            elif item["unit"][0] == "兰氏度":
                value = self.convertTemperature2Lansd(dTemperature)
                 
                
            self.setItemValue(item, value)
            
            
      
    def convertShesd2Temperature(self, dTemperature):
     
        return dTemperature + T_FACTOR
      
    def convertKaisd2Temperature(self, dTemperature):
        
        return dTemperature
            
    def convertLiesd2Temperature(self, dTemperature):
    
        return dTemperature * T_K_RE + T_FACTOR
    
    def convertHuasd2Temperature(self, dTemperature):
       
        return ((dTemperature - 32) * 5 / 9) + T_FACTOR
    
    def convertLansd2Temperature(self, dTemperature):
        
        return dTemperature / T_K_R
    
    #
    def convertTemperature2Shesd(self, dTemperature):
    
        return dTemperature - T_FACTOR
    
    def convertTemperature2Kaisd(self, dTemperature):
        
        return dTemperature
    
    def convertTemperature2Liesd(self, dTemperature):
        
        return (dTemperature - T_FACTOR) / T_K_RE
    
    def convertTemperature2Huasd(self, dTemperature):
        
        return (dTemperature - T_FACTOR) * 9 / 5 + 32
        
    def convertTemperature2Lansd(self, dTemperature):
        
        return dTemperature * T_K_R
    

class SubFrame8(tk.Frame):
    
    
    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)
        self.initUI()
        
    def title(self):
        
        return "角度转换"
    
    
    def initUI(self):
        
        self.dValue = tk.StringVar()
        self.sUnit = tk.StringVar()
        self.dValue.set(1.0)
        
        units = [("圆周", "圆周"), ("直角", "直角"), ("百分度", "gon"), ("度", "°"), ("角分", "'"), ("角秒", "''"), ("弧度", "rad"), ("毫弧度", "mrad")]
        
        unit_values = []
        for item in units:
            unit_values.append(item[0])
        
        lab = tk.Label(self, text="角度:")
        val = tk.Entry(self, width=24, textvariable=self.dValue)
        sel = ttk.Combobox(self, width=8, textvariable=self.sUnit, values=unit_values, state='readonly')
        btn = tk.Button(self, width=8, text="转换", command=self.onConvertValue)
        sel.current(0)
        
        lab.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
        val.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        sel.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))
        btn.grid(row=0, column=3, padx=(10, 0), pady=(10, 0))
        
        self.units = []
        for index in range(len(units)):
            row = index + 1
            item = units[index]
            lab_titile = "{}:".format(item[0])
            lab_content = "0 {}".format(item[1])
            value = tk.StringVar()
            value.set(lab_content)
            self.units.append({"value": value, "unit": item})
            title = tk.Label(self, text=lab_titile)
            content = LabelValue(self, textvariable=value)
            title.grid(row=row, column=0, padx=(30, 0), pady=(10, 0), sticky=tk.E)
            content.grid(row=row, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W, columnspan=4)            
            
            
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
    
    
    def setItemValue(self, item, value):
        
        decimal = math.modf(value)[0]
        if decimal == 0:
            text = "{} {}".format(toInt(value), item["unit"][1])
        elif decimal < 0.000001:
            text = "{:.3e} {}".format(value, item["unit"][1])
        else:
            text = "{:.6f} {}".format(value, item["unit"][1])
        
        item["value"].set(text)
        

    def onConvertValue(self):
        
        self.convertValue(toReal(self.dValue.get()), self.sUnit.get())
        
        
    def convertValue(self, dValue, unit):
      
        dDeg = 0 # 
        if unit == "圆周":
            dDeg = self.convertCircle2Deg(dValue)
        elif unit == "直角":      
            dDeg = self.convertAngle2Deg(dValue)              
        elif unit == "百分度":
            dDeg = self.convertGon2Deg(dValue)
        elif unit == "度":       
            dDeg = self.convertDeg2Deg(dValue)         
        elif unit == "角分":      
            dDeg = self.convertArcmin2Deg(dValue)
        elif unit == "角秒":      
            dDeg = self.convertArcsec2Deg(dValue)        
        elif unit == "弧度":       
            dDeg = self.convertRad2Deg(dValue)         
        elif unit == "毫弧度":      
            dDeg = self.convertMrad2Deg(dValue)
             
            
        for item in self.units:
            
            value = 0
            if item["unit"][0] == "圆周":
                value = self.convertDeg2Circle(dDeg)
            elif item["unit"][0] == "直角":
                value = self.convertDeg2Angle(dDeg)
            elif item["unit"][0] == "百分度":
                value = self.convertDeg2Gon(dDeg)
            elif item["unit"][0] == "度":
                value = self.convertDeg2Deg(dDeg)
            elif item["unit"][0] == "角分":
                value = self.convertDeg2Arcmin(dDeg)
            elif item["unit"][0] == "角秒":
                value = self.convertDeg2Arcsec(dDeg)
            elif item["unit"][0] == "弧度":
                value = self.convertDeg2Rad(dDeg)
            elif item["unit"][0] == "毫弧度":
                value = self.convertDeg2Mrad(dDeg)                 
                
            self.setItemValue(item, value)
            

    def convertCircle2Deg(self, dCircle):
        
        return dCircle * 360.0
    
    def convertAngle2Deg(self, dAngle):
        
        return dAngle * 90.0
    
    def convertGon2Deg(self, dGon):
        
        return dGon / 1.111111
    
    def convertDeg2Deg(self, dDeg):
        
        return dDeg
    
    def convertArcmin2Deg(self, dArcmin):
        
        return dArcmin / 60.0
    
    def convertArcsec2Deg(self, dArcsec):
        
        return dArcsec / 3600.0
    
    def convertRad2Deg(self, dRad):
        
        return dRad * 180.0 / PI
    
    def convertMrad2Deg(self, dMrad):
        
        return dMrad * 180.0 / PI / 1000.0
    
    
    #
    def convertDeg2Circle(self, dDeg):
        
        return dDeg / 360.0
    
    def convertDeg2Angle(self, dDeg):
        
        return dDeg / 90.0
    
    def convertDeg2Gon(self, dDeg):
        
        return dDeg * 1.111111
    
    def convertDeg2Arcmin(self, dDeg):
        
        return dDeg * 60.0
    
    def convertDeg2Arcsec(self, dDeg):
        
        return dDeg * 3600.0
    
    def convertDeg2Rad(self, dDeg):
        
        return dDeg / 180.0 * PI
    
    def convertDeg2Mrad(self, dDeg):
        
        return dDeg / 180.0 * PI * 1000.0   
       
       
       
       
       
#
class MainDialog:
    
    def __init__(self):
        
        width = 560
        height = 480
        self.frame = tk.Tk()
        #self.frame.geometry("{}x{}".format(width, height))
        self.frame.minsize(width, height)
        #self.frame.maxsize(width, height)
        #self.frame.resizable(0, 0)
        self.frame.title("计算小工具")
        

    def initUI(self):
        
        tab_frame = ttk.Notebook(self.frame)
        
        frames = [
            SubFrame(tab_frame),
            SubFrame1(tab_frame),
            SubFrame2(tab_frame),
            SubFrame3(tab_frame),
            SubFrame4(tab_frame),
            SubFrame5(tab_frame),
            SubFrame6(tab_frame),
            SubFrame7(tab_frame),
            SubFrame8(tab_frame),
        ]
        
        for frame in frames:
            tab_frame.add(frame, text=frame.title())
    
        tab_frame.pack(pady=(0, 16), fill=tk.BOTH, expand=True)
        
    def runloop(self):
        
        self.frame.mainloop()
        

if __name__ == "__main__":
    
    dialog = MainDialog()
    dialog.initUI()
    dialog.runloop()