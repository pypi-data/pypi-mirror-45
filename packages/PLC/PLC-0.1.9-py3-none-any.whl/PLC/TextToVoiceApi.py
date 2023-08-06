from selenium import webdriver
import time
from PLC.AudioTools import DownloadBlob
from PLC.TextTools import RemoveSpaces
def CreateBrowser():
    try:
        browser = webdriver.Chrome()
    except:
        browser = webdriver.Chrome(executable_path='C:\chromedriver.exe')
    browser.get('https://www.naturalreaders.com/online/')
    return browser
def ConvertTextToVoice(Name, Text, Speed=1, browser=None, browserRemainOpen=False):
    if browser == None:
        browser = CreateBrowser()
    Byte = b''
    currentName = GetCurrentName(browser)
    if Name not in currentName:
        ChangeName(Name, browser)
    currentSpeed = GetCurrentSpeed(browser)
    #print(currentSpeed)
    if Speed != currentSpeed:
       ChangeSpeed(Speed, browser)
    Text = RemoveSpaces(Text, addDot=False)
    for Sentence in Text.split("."):
        for Sen in Sentence.split("?"):
            for Se in Sen.split("!"):
                Byte += Get(Se, browser)
    if not browserRemainOpen:
        browser.quit()
    return Byte
def GetCurrentName(browser=None):
    if browser == None:
        browser = CreateBrowser()
    Name = browser.find_element_by_id('chooseVoice').text
    return Name
def GetCurrentSpeed(browser=None):
    if browser == None:
        browser = CreateBrowser()
    Speed = browser.find_element_by_id('selectedSpeed').text
    return Speed
def Get(text, browser):

    Text = browser.find_element_by_id('inputDiv')
    Cleared = Text.text == ''
    try:
        TextClear = browser.find_elements_by_class_name('btnClose')[0]
        TextClear.click()
    except:
        while not Cleared:
            try:
                Text.clear()
                Cleared = True
            except:
                time.sleep(0.1)
    Text.send_keys(text)
    PageSource = browser.page_source
    Failed = True
    while Failed:
        try:
            PreAudioSrc = FindAudioPart(PageSource)
            Button = browser.find_element_by_class_name("playPause")
            Button.click()
            Failed = False
        except:
            input('Configure new proxy and then click enter.')
    Bytes1 = b''
    while "pause" in Button.get_attribute('class'):
        try:
            PageSource = browser.page_source
            Now = FindAudioPart(PageSource)
            if Now != PreAudioSrc:
                Bytes1 += DownloadBlob(browser, Now)
                PreAudioSrc = Now
        except:
            input('Error occured when solved press enter')
            time.sleep(0.01)
    #AudioSrc = PageSource.split('<audio id="audio" controls="controls" src="')[1].split('">')[0]#.split("blob:")[1]
    #
    # Found = False
    # while not Found:
    #     time.sleep(0.1)
    #     PageSource = browser.page_source
    #     Found = 'src' in PageSource.split('<audio id="audio" controls="controls"')[1].split('>')[0]
    #     if Found:
    #         AudioSrc = PageSource.split('<audio id="audio" controls="controls" src="')[1].split('">')[0]#.split("blob:")[1]
    #         if AudioSrc == PreAudioSrc:
    #             Found = not Found

    #Bytes1 = DownloadBlob(browser, AudioSrc)
    return Bytes1
def ChangeName(Name, browser):
    SelectBtn = browser.find_element_by_id('chooseVoice')
    SelectBtn.click()

    F1 = browser.find_element_by_id("dropdownMenuvoicelist")
    F2 = F1.find_element_by_class_name("languageContent")
    F3 = F2.find_element_by_class_name("tabContainer")
    F4 = F3.find_element_by_class_name("premiumContent")
    F5 = F4.find_element_by_id("onlinecontent")
    F6 = F5.find_element_by_class_name("content")
    ul = F6.find_element_by_tag_name("ul")
    li_s = ul.find_elements_by_tag_name('li')

    for li in li_s:
        NameDiv = li.find_element_by_class_name("personName")
        if NameDiv.text == Name:
            li.click()
            break
def ChangeSpeed(Speed, browser):
    SelectBtn = browser.find_element_by_id('selectedSpeed')
    SelectBtn.click()
    F1 = browser.find_element_by_class_name('selectaSpeed')
    F2 = F1.find_element_by_class_name('dropdownGroup')
    F1 = F2.find_element_by_class_name("dropdownMenu")
    ul = F1.find_element_by_tag_name("ul")
    li_s = ul.find_elements_by_tag_name('li')
    for li in li_s:
        SpeedLi = li.get_attribute('innerHTML')
        if SpeedLi != ' ' and (str(Speed) in str(SpeedLi) or str(SpeedLi) in str(Speed)):
            clicked = False
            while not clicked:
                try:
                    li.click()
                    clicked = True
                except:
                    time.sleep(0.01)
            break
def FindAudioPart(source):

    PageSource = source
    Found = 'src' in PageSource.split('<audio id="audio" controls="controls"')[1].split('>')[0]
    if Found:
      PreAudioSrc = PageSource.split('<audio id="audio" controls="controls" src="')[1].split('">')[0]
    else:
      PreAudioSrc = ''
    return PreAudioSrc
if __name__ == '__main__':
    f = open('testfile.txt', 'r')
    Text = f.read()
    Text = ' '.join(Text.split('\n'))
    Text = Text.split('|SPLITTHISPART|')
    f.close()
    browser = CreateBrowser()
    for i, Part in enumerate(Text):
        o = open("Maman{}.mp3".format(i), 'wb')
        o.write(ConvertTextToVoice("English (US) - Susan", Part, Speed=0, browser=browser, browserRemainOpen=True))
        o.close()
    browser.quit()