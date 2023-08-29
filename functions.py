import os
import time
from pyautogui import size, screenshot, click, press, typewrite, locateOnScreen, hotkey, center
import pytesseract
import pygetwindow as gw
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

screenWidth, screenHeight = size()

originalScreenWidth = 1920
originalScreenHeight = 1080

def open_application():

    window = gw.getWindowsWithTitle('Valor PRO')
    if window:
        window[0].activate()
    else:
        hotkey('win', 'd')
        my_click(60, 380)
        my_click(60, 380)
        time.sleep(60)


def read_screen(x_start, y_start, x_end, y_end):
    global screenWidth, screenHeight, originalScreenWidth, originalScreenHeight

    region = (
        int(x_start * screenWidth / originalScreenWidth),
        int(y_start * screenHeight / originalScreenHeight),
        int(x_end * screenWidth / originalScreenWidth),
        int(y_end * screenHeight / originalScreenHeight)
    )
    im = screenshot(region=(x_start, y_start, x_end, y_end))
    return pytesseract.image_to_string(im).strip()

def my_click(x, y):
    global screenWidth, screenHeight, originalScreenWidth, originalScreenHeight

    click(
        int(x * screenWidth / originalScreenWidth),
        int(y * screenHeight / originalScreenHeight)
    )

def lookup_company(cnpj):
    # empty the search bar
    my_click(180, 85)
    my_click(180, 85)
    press('backspace')

    # type the company name
    typewrite(cnpj)
    time.sleep(2)

    # wait for the name to show and select it
    start_time = time.time()
    while read_screen(50,115,275,25) == 'Nao ha resultados para a busca.':
        if time.time() - start_time > 5:
            return False
        
    press('down')
    press('enter')

    # while Dados Cadastrais not available click it
    while not locateOnScreen('wait_for_this/(Dados Cadastrais).png'):
        my_click(180, 300)

    return True

def select_fields():
    start_time = time.time()
    while (time.time() - start_time) < 2:  # 2 seconds timeout
        location = locateOnScreen('wait_for_this/(Padrao).png', confidence=0.9)
        if location is not None:
            time.sleep(2)
            my_click(580, 165)
            time.sleep(0.1)
            my_click(640, 320)
            time.sleep(0.1)
            my_click(910, 500)
            time.sleep(0.1)
            my_click(910, 580)
            time.sleep(0.1)
            my_click(1165, 570)
            break
    else:
        return
    
def reset_program():
    os.system('taskkill /IM "ValorPRO.exe" /F')
    hotkey('win', 'd')
    time.sleep(0.5)
    my_click(60, 380)
    my_click(60, 380)

    start_time = time.time()
    while not locateOnScreen('wait_for_this/(Valor PRO).png', confidence=0.9):
        if time.time() - start_time > 60:
            return
        
    my_click(1015, 365)

    my_click(390, 420)

    time.sleep(10)
    click(center(locateOnScreen('wait_for_this/(Full Screen).png', confidence=0.9)))

def download(path):
    global empresa

    downloaded_dates = [x.split('__')[-1].split('.')[0] for x in os.listdir(path)]

    # current date being downloaded
    date = read_screen(335,160,110,20).replace('/', '_')

    if date not in downloaded_dates:
        
        # wait for VALORPRO to finish loading the data
        start_time = time.time()
        while not read_screen(330,240,150,25) == 'Administracao':
            if time.time() - start_time > 2:
                return True

        # position of the 'printer' button
        time.sleep(0.3)
        my_click(490, 90)

        # wait for the print menu to appear
        start_time = time.time()
        while (time.time() - start_time) < 5:
            location1 = locateOnScreen('wait_for_this/(1).png', confidence=0.9)
            location2 = locateOnScreen('wait_for_this/(Print).png', confidence=0.9)
            if location1 is not None:
                time.sleep(0.3)
                click(center(location1))
                found = True
                break
            elif location2 is not None:
                time.sleep(0.3)
                click(center(location2))
                found = True
                break
            found = False

        # if the print menu didn't appear, reset the program
        if not found:
            reset_program()
            return False

        # wait for the file explorer menu to appear
        start_time = time.time()
        while (time.time() - start_time) < 5:
            location = locateOnScreen('wait_for_this/(Save Print).png', confidence=0.9)
            if location is not None:
                found = True
                break
            found = False
        
        # if the file explorer menu didn't appear, reset the program
        if not found:
            reset_program()
            return False

        # position of the 'path'
        time.sleep(0.3)
        my_click(500, 80)

        # go to path
        time.sleep(0.3)
        typewrite(path)
        press('enter')

        # name of the file
        time.sleep(0.3)
        my_click(240, 550)
        typewrite(f"{path.split('/')[-2]}__{date}")

        time.sleep(1)
        # save
        my_click(700, 670)
        time.sleep(3)
        
    return True