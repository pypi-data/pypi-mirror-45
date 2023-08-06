from PIL import ImageFont, ImageDraw, Image
import textwrap

def getSize(text, font):
    maxwidth = 0
    height = 0
    for line in text.split('\n'):
        if font.getsize(line)[0]>maxwidth:
            maxwidth = font.getsize(line)[0]
        height += font.getsize(line)[1]
    return maxwidth, height
def getMaxChar(font, maxwidth):
    text = ''
    while getSize(text, font)[0]<=maxwidth:
        text+='A'
    return len(text[:-1])
def getWrap(text, font, maxwidth):
    OutList = textwrap.wrap(text, width=getMaxChar(font, maxwidth))
    Out = '\n'.join(OutList)
    return Out
def AutoSizeAdjust(text, fontname, maxfontsize, maxwidth, maxheight):
    fontsize = 0
    for fontsize in range(maxfontsize, 0, -1):
        font = ImageFont.truetype(fontname, fontsize)
        if getSize(getWrap(text, font, maxwidth), font)[1]<=maxheight:
            break
    return fontsize
def AlignCenter(text, Font, width, height, addtoW = 0, addtoH = 0):
    #Text = getWrap(text, Font, width)
    textWidth, textHeight = getSize(text, Font)
    print("A", textWidth, textHeight)
    print("B", width, height)
    print("C", addtoW, addtoH)
    print("D", addtoW, addtoH)
    print("E1", int((width-textWidth)/2))
    print("E2", int((height-textHeight)/2))
    return addtoW + int((width-textWidth)/2), addtoH + int((height-textHeight)/2)
def GenerateNewWordsPage(Word, Def, Sen):
    IM = Image.open('/home/kingurl/Parsian Language Center/ParsianLanguageCenter/PLC/statics/MovieGenerator/Back.jpg')
    Im_Draw = ImageDraw.Draw(IM)
    fontname = '/home/kingurl/Parsian Language Center/ParsianLanguageCenter/PLC/statics/fonts/Coiny-Regular.ttf'


    WordFieldwidth = 1000
    WordFieldheight = 200

    Wordfontsize = AutoSizeAdjust(Word, fontname, 110, WordFieldwidth, WordFieldheight)
    WordFont = ImageFont.truetype(fontname, Wordfontsize)
    Word = getWrap(Word, WordFont, WordFieldwidth)
    Im_Draw.text((150, 100), Word, 'white', WordFont)

    DefFieldwidth = 1700
    DefFieldheight = 200

    Deffontsize = AutoSizeAdjust(Def, fontname, 85, DefFieldwidth, DefFieldheight)
    DefFont = ImageFont.truetype(fontname, Deffontsize)
    Def = getWrap(Def, DefFont, DefFieldwidth)
    DefFieldMarginWidth = IM.size[0] - 660
    DefFieldMarginHeight = IM.size[1] - 1000
    DefLocation = AlignCenter(Def, DefFont, DefFieldMarginWidth, DefFieldMarginHeight, 330, 520)
    Im_Draw.text(DefLocation, Def, 'white', DefFont)


    SenFieldwidth = 1700
    SenFieldheight = 200

    Senfontsize = AutoSizeAdjust(Sen, fontname, 85, SenFieldwidth, SenFieldheight)
    SenFont = ImageFont.truetype(fontname, Senfontsize)
    Sen = getWrap(Sen, SenFont, SenFieldwidth)
    SenFieldMarginWidth = IM.size[0] - 660
    SenFieldMarginHeight = IM.size[1] - 80
    SenLocation = AlignCenter(Sen, SenFont, SenFieldMarginWidth, SenFieldMarginHeight, 330, 380)
    Im_Draw.text(SenLocation, Sen, 'white', SenFont)

    return IM
def GenerateMiddleofPage(Question):
    IM = Image.open('/home/kingurl/Parsian Language Center/ParsianLanguageCenter/PLC/statics/MovieGenerator/BackNoneField.jpg')#BackNoneField.jpg')
    Im_Draw = ImageDraw.Draw(IM)
    fontname = '/home/kingurl/Parsian Language Center/ParsianLanguageCenter/PLC/statics/fonts/Coiny-Regular.ttf'
    Q = Question
    QFieldwidth = 2000
    QFieldheight = 500

    Qfontsize = AutoSizeAdjust(Q, fontname, 85, QFieldwidth, QFieldheight)
    QFont = ImageFont.truetype(fontname, Qfontsize)
    Q = getWrap(Q, QFont, QFieldwidth)
    QFieldMarginWidth = IM.size[0]
    QFieldMarginHeight = IM.size[1]
    QLocation = AlignCenter(Q, QFont, QFieldMarginWidth, QFieldMarginHeight)
    Im_Draw.text(QLocation, Q, 'white', QFont)
    return IM
