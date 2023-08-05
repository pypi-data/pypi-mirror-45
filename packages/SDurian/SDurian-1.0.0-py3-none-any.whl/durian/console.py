#-*- coding:utf-8 -*-

'''
    | durian/ -> author & version & donate_wechatpay() & donate_alipay() & donate_paypal()
    |  => console.py <=
    |  => gui.py (PyGtk/PyGobject)
    |  => user.py
    |  => network.py
    |  => os.py
    |  => tools.py
    |  => ctools.py
    2019-4-18 in 深圳福永
    By Binn Louis Zeng
    PyDurian -> pygi
             -> Github
'''
__STD_INPUT_HANDLE__ = -10
__STD_OUTPUT_HANDLE__ = -11
__STD_ERROR_HANDLE__ = -12


#/* fore ground color */
#define FOREGROUND_BLUE 0x1
#define FOREGROUND_GREEN 0x2
#define FOREGROUND_RED 0x4
#define FOREGROUND_INTENSITY 0x8
FG_BLUE    = 0x1                            #1.蓝
FG_GREEN   = 0x2                            #2.绿
FG_RED     = 0x4                            #3.红
FG_DEEP    = 0x8                            #*.深
FG_BLACK   = 0x0                            #4.黑
FG_CYAN    = FG_BLUE | FG_GREEN             #5.青色
FG_PINK    = FG_BLUE | FG_RED               #6.粉红
FG_WHITE   = FG_BLUE | FG_GREEN | FG_RED    #7.白色
FG_YELLOW  = FG_GREEN | FG_RED              #8黄色
FG_DEFAULT = FG_BLUE | FG_GREEN | FG_RED

#/* back ground color */
#define BACKGROUND_BLUE 0x10
#define BACKGROUND_GREEN 0x20
#define BACKGROUND_RED 0x40
#define BACKGROUND_INTENSITY 0x80

BG_BLUE    = 0x10
BG_GREEN   = 0x20
BG_RED     = 0x40
BG_DEEP    = 0x80
BG_BLACK   = 0x0
BG_CYAN    = BG_BLUE | BG_GREEN
BG_PINK    = BG_BLUE | BG_RED
BG_WHITE   = BG_BLUE | BG_GREEN | BG_RED
BG_YELLOW  = BG_GREEN | BG_RED
BG_DEFAULT = BG_BLACK

#/*
# * 修饰 
# */
TOP = 0x400
UNDER = 0x8000
AA =  0x800 | 0x400
DEFAULT = FG_DEFAULT | BG_DEFAULT

import ctypes as __durian_ctypes__
import time as __durian_time__
import os as __durian_os__

#-> __durian_kernel32__ as ctypes.windll.kernel32
__durian_kernel32__ = __durian_ctypes__.windll.kernel32
__durian_shell32__ = __durian_ctypes__.windll.shell32
__durian_user32__ = __durian_ctypes__.windll.user32
'''
/*
 * Test STD device (istty)
 */
'''
def istty() -> bool:
    if(bool(__durian_kernel32__.GetStdHandle(__STD_INPUT_HANDLE__)) != True):return False
    elif(bool(__durian_kernel32__.GetStdHandle(__STD_OUTPUT_HANDLE__)) != True):return False
    elif(bool(__durian_kernel32__.GetStdHandle(__STD_ERROR_HANDLE__)) != True):return False
    else:return True
class ConsoleError(Exception):
    def __init__(self,meessage):
        self.value = meessage
class CPNotSupported(Exception):
    def __init__(self,meessage):
        self.value = meessage
class TypeError(Exception):
    def __init__(self,meessage):
        self.value = meessage

'''
/*
 * Set Console ICON
 */
'''
def set_icon(path) -> bool:
    WM_SETICON = 0x80
    ICON_SMALL = 0x0
    if(type(path) != str):
        raise TypeError("set_icon(path) -> path type is string")
    if(__durian_os__.path.exists(path) == False):
        return False
    try:
        self_ = __durian_kernel32__.GetModuleHandleW(0)             #获得自己的实例 instance:HINSTANCE
        icon_ = __durian_shell32__.ExtractIconW(self_,path,0)       #获得一个HICON
        hwnd_ = __durian_kernel32__.GetConsoleWindow()              #获得控制台句柄
        __durian_user32__.SendMessageW(hwnd_,WM_SETICON,ICON_SMALL,icon_)
    except:
        return False
    else:
        return True
'''
/*
 * Set ICON for default
 */
'''
def set_default_icon() -> bool:
    WM_SETICON = 0x80
    ICON_SMALL = 0x0
    try:
        hwnd_ = __durian_kernel32__.GetConsoleWindow()              #获得控制台句柄
        __durian_user32__.SendMessageW(hwnd_,WM_SETICON,ICON_SMALL,None)
    except:
        return False
    else:
        return True
#Console CP
__cp__ = {
            437:"ascii",
            936:"gbk",
            950:"big5"
        }

'''
/*
 * Get Code Page(CP)
 */
'''
def get_cp() -> int:
    return __durian_kernel32__.GetConsoleCP()
'''
/*
 * Set Code Page(CP)
 */
'''
#def set_cp(CP_code) -> bool:
#    if(type(CP_code) != int):
#        raise TypeError("set_cp(CP_code) -> CP_code Should be a string type.")
#    return bool(__durian_kernel32__.SetConsoleCP(CP_code))
'''
/*
 * Set Console Title
 */
'''
def set_title(string) -> bool:
    if(type(string) != str):
        raise "arg string need type[str] -> set_title(string)参数应该是个字符串"
    return bool(__durian_kernel32__.SetConsoleTitleW(string))
'''
/*
 * Get Console Title
 */
'''
def get_title() -> str:
    title = __durian_ctypes__.create_string_buffer(255)
    #创建一个字符串缓冲区
    title_p = __durian_ctypes__.pointer(title)
    __durian_kernel32__.GetConsoleTitleA(title_p,255)
    
    try:
        re = str(title.value,__cp__[get_cp()])
    except KeyError:
        raise CPNotSupported("Sorry, event code page %d is not yet supported" %get_cp())
    return re

def cprint(string,code):
    if(type(string) != str):
        raise "arg string need type[str] -> cprint(string,code)"
    std_h = __durian_kernel32__.GetStdHandle(__STD_OUTPUT_HANDLE__)
    __durian_kernel32__.SetConsoleTextAttribute(std_h,code)
    print(string,end = "",flush = True)
    __durian_kernel32__.SetConsoleTextAttribute(std_h,DEFAULT)

def cprintln(string,code):
    if(type(string) != str):
        raise "arg string need type[str] -> cprintln(string,code)"
    std_h = __durian_kernel32__.GetStdHandle(__STD_OUTPUT_HANDLE__)
    __durian_kernel32__.SetConsoleTextAttribute(std_h,code)
    print(string,flush = True)
    __durian_kernel32__.SetConsoleTextAttribute(std_h,DEFAULT)

'''
/*
 * Flash Word ->
 */
'''
'''
def fprint(string,timer = 1):
    if(type(string) != str):
        raise "arg string need type[str] -> fprint(string,time)"
    if(type(timer) != int):
        raise "arg time need type[int] -> fprint(string,time)"
    
    while True:
        print(string,end = "",flush = True)
        __durian_time__.sleep(timer / 2)
        for i in string:
            print("\b \b",end = "",flush = True)
        __durian_time__.sleep(timer / 2)
'''
def print_color_demo():

    #/* fore ground BLACK */
    print(" ==>  [",end = "",flush = True)
    cprint("FG_BLACK | BG_WHITE",FG_BLACK | BG_WHITE)
    cprint("] [",DEFAULT)
    cprint("FG_BLACK | FG_DEEP | BG_WHITE",FG_BLACK | FG_DEEP | BG_WHITE)
    print("]")

    #/* fore ground BLUE */
    print(" ==>  [",end = "",flush = True)
    cprint("FG_BLUE",FG_BLUE)
    cprint("] [",DEFAULT)
    cprint("FG_BLUE | FG_DEEP",FG_BLUE | FG_DEEP)
    print("]")

    #/* fore ground GREEN */
    print(" ==>  [",end = "",flush = True)
    cprint("FG_GREEN",FG_GREEN)
    cprint("] [",DEFAULT)
    cprint("FG_GREEN | FG_DEEP",FG_GREEN | FG_DEEP)
    print("]")

    #/* fore ground RED */
    print(" ==>  [",end = "",flush = True)
    cprint("FG_RED",FG_RED)
    cprint("] [",DEFAULT)
    cprint("FG_RED | FG_DEEP",FG_RED | FG_DEEP)
    print("]")

    #/* fore ground CYAN */
    print(" ==>  [",end = "",flush = True)
    cprint("FG_CYAN",FG_CYAN)
    cprint("] [",DEFAULT)
    cprint("FG_CYAN | FG_DEEP",FG_CYAN | FG_DEEP)
    print("]")

    #/* fore ground PINK */
    print(" ==>  [",end = "",flush = True)
    cprint("FG_PINK",FG_PINK)
    cprint("] [",DEFAULT)
    cprint("FG_PINK | FG_DEEP",FG_PINK | FG_DEEP)
    print("]")

    #/* fore ground YELLOW */
    print(" ==>  [",end = "",flush = True)
    cprint("FG_YELLOW",FG_YELLOW)
    cprint("] [",DEFAULT)
    cprint("FG_YELLOW | FG_DEEP",FG_YELLOW | FG_DEEP)
    print("]")
    
    #/* fore ground WHITE */
    print(" ==>  [",end = "",flush = True)
    cprint("FG_WHITE",FG_WHITE)
    cprint("] [",DEFAULT)
    cprint("FG_WHITE | FG_DEEP",FG_WHITE | FG_DEEP)
    print("]\n")
    
    #/* Back Ground color */
    #/* BLUE */
    print(" ==>  %-30s" %("BG_BLUE:"),"%-30s" %("BG_BLUE | BG_DEEP:"),flush = True)
    print("      [",end = "",flush = True)
    cprint(" " * 28,BG_BLUE)
    print("] [",end = "",flush = True)
    cprint(" " * 28,BG_BLUE | BG_DEEP)
    print("]")

    #/* GREEN */
    print(" ==>  %-30s" %("BG_GREEN:"),"%-30s" %("BG_GREEN | BG_DEEP:"),flush = True)
    print("      [",end = "",flush = True)
    cprint(" " * 28,BG_GREEN)
    print("] [",end = "",flush = True)
    cprint(" " * 28,BG_GREEN | BG_DEEP)
    print("]")

    #/* RED */
    print(" ==>  %-30s" %("BG_RED:"),"%-30s" %("BG_RED | BG_DEEP:"),flush = True)
    print("      [",end = "",flush = True)
    cprint(" " * 28,BG_RED)
    print("] [",end = "",flush = True)
    cprint(" " * 28,BG_RED | BG_DEEP)
    print("]")

    #/* CYAN */
    print(" ==>  %-30s" %("BG_CYAN:"),"%-30s" %("BG_CYAN | BG_DEEP:"),flush = True)
    print("      [",end = "",flush = True)
    cprint(" " * 28,BG_CYAN)
    print("] [",end = "",flush = True)
    cprint(" " * 28,BG_CYAN | BG_DEEP)
    print("]")

    #/* PINK */
    print(" ==>  %-30s" %("BG_PINK:"),"%-30s" %("BG_PINK | BG_DEEP:"),flush = True)
    print("      [",end = "",flush = True)
    cprint(" " * 28,BG_PINK)
    print("] [",end = "",flush = True)
    cprint(" " * 28,BG_PINK | BG_DEEP)
    print("]")

    #/* YELLOW */
    print(" ==>  %-30s" %("BG_YELLOW:"),"%-30s" %("BG_YELLOW | BG_DEEP:"),flush = True)
    print("      [",end = "",flush = True)
    cprint(" " * 28,BG_YELLOW)
    print("] [",end = "",flush = True)
    cprint(" " * 28,BG_YELLOW | BG_DEEP)
    print("]")
    
    #/* WHITE */
    print(" ==>  %-30s" %("BG_WHITE:"),"%-30s" %("BG_WHITE | BG_DEEP:"),flush = True)
    print("      [",end = "",flush = True)
    cprint(" " * 28,BG_WHITE)
    print("] [",end = "",flush = True)
    cprint(" " * 28,BG_WHITE | BG_DEEP)
    print("]")
    
    #/* BLACK */
    print(" ==>  %-30s" %("BG_BLACK:"),"%-30s" %("BG_BLACK | BG_DEEP:"),flush = True)
    print("      [",end = "",flush = True)
    cprint(" " * 28,BG_BLACK)
    print("] [",end = "",flush = True)
    cprint(" " * 28,BG_BLACK | BG_DEEP)
    print("]")

if(istty() != True):
    raise ConsoleError("this is not console.")
