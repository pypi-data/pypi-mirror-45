from PIL import ImageFont, ImageDraw, Image
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip
from PLC.DatabaseTools import LoadDb
from PLC.FilmTools import Trim, Concatenate
from PLC.TextTools import RemoveSpaces
from PLC.Tools import CreateDirectory
from PLC.TextToVoiceApi import CreateBrowser, ConvertTextToVoice
import pathlib
import textwrap
import cv2
import os

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
    IM = Image.open(
        '/home/kingurl/Parsian Language Center/ParsianLanguageCenter/PLC/statics/MovieGenerator/Back.jpg')
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
    IM = Image.open(
        '/home/kingurl/Parsian Language Center/ParsianLanguageCenter/PLC/statics/MovieGenerator/BackNoneField.jpg')  # BackNoneField.jpg')
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

class Movie():
    def genMoviePart(self, file):

        data = LoadDb(file, 'MP')
        print(data)
        CreateDirectory('temp', True)
        for i, row in enumerate(data):
            print(row[1])
            Trim('Movies/' + row[0], int(row[1].split('-')[0]), int(row[1].split('-')[1]), 'temp//' + str(i) + '.mp4')
        videos = []

        for filename in pathlib.Path('temp').glob('*.mp4'):
            videos.append(filename.as_posix())
        videos.sort()
        Concatenate(videos, 'output.mp4')
        video = VideoFileClip('output.mp4')
        return video
    def genNewWords(self, datas, browser=CreateBrowser()):
        Path = os.curdir
        NewWords = []
        for i, Result in enumerate(datas):
            Pronouncer = Result[-1]
            if Pronouncer[-1] == "*":
                Pronouncer = Pronouncer[0:-1]
            if Pronouncer != Pronouncer:
                Name = Pronouncer
            Others = ".".join(Result[0:-1])
            Others = RemoveSpaces(Others, addDot=False)
            Bytes = ConvertTextToVoice(Name, Others, Speed=1, browser=browser, browserRemainOpen=True)

            File = open('temp.mp3', 'wb')  # Path + "//" + Part + "_" + str(i) + ".mp3", "wb")
            File.write(Bytes)
            File.close()
            Page = GenerateNewWordsPage(Result[0], Result[1], Result[2])
            # else:
            #     Page = GenerateMiddleofPage(Result[0])
            Audio = AudioFileClip('temp' + ".mp3")
            Page.save('temp.jpg')
            ImageFake = cv2.imread('temp.jpg')
            Image = cv2.cvtColor(ImageFake, cv2.COLOR_BGR2RGB)
            print("DUE", Audio.duration, int((Audio.duration) * Audio.fps))
            new_clip = ImageSequenceClip([Image] * int((Audio.duration + 2)), fps=1)
            new_clip.write_videofile('temp.mp4')
            # newaudio = new_clip.set_audio(Audio.set_duration(new_clip.duration))
            # newaudio.write_videofile('temp1.mp4')#Path + "//" + Part + "_" + str(i) + ".mp4")
            video = VideoFileClip('temp.mp4')
            video = video.set_audio(AudioFileClip("temp.mp3").set_duration(video.duration))

            NewWords.append(Path + "/raw/NewWords_" + str(i) + ".mp4")
            # elif Part == 'Chunks':
            #     Chunks.append(Path + "/raw/" + Part + "_" + str(i) + ".mp4")
            # elif Part == 'ComprehensionCheckQuestions':
            #     Comp.append(Path + "/raw/" + Part + "_" + str(i) + ".mp4")
            # elif Part == 'MakeTrueSentences':
            #     MakeTS.append(Path + "/raw/" + Part + "_" + str(i) + ".mp4")
            new_clip.write_videofile(Path + "/raw/NewWords_" + str(i) + ".mp4")
        Concatenate(NewWords, "OutputNewWords.mp4")
        return VideoFileClip("OutputNewWords.mp4")
    def genComps(self, datas, browser=CreateBrowser()):
        Path = os.curdir
        Comp = []
        for i, Result in enumerate(datas):
            Pronouncer = Result[-1]
            if Pronouncer[-1] == "*":
                Pronouncer = Pronouncer[0:-1]
            if Pronouncer != Pronouncer:
                Name = Pronouncer
            Others = ".".join(Result[0:-1])
            Others = RemoveSpaces(Others, addDot=False)
            Bytes = ConvertTextToVoice(Name, Others, Speed=1, browser=browser, browserRemainOpen=True)

            File = open('temp.mp3', 'wb')  # Path + "//" + Part + "_" + str(i) + ".mp3", "wb")
            File.write(Bytes)
            File.close()
            Page = GenerateMiddleofPage(Result[0])
            Audio = AudioFileClip('temp' + ".mp3")
            Page.save('temp.jpg')
            ImageFake = cv2.imread('temp.jpg')
            Image = cv2.cvtColor(ImageFake, cv2.COLOR_BGR2RGB)
            print("DUE", Audio.duration, int((Audio.duration) * Audio.fps))
            new_clip = ImageSequenceClip([Image] * int((Audio.duration + 2)), fps=1)
            new_clip.write_videofile('temp.mp4')
            # newaudio = new_clip.set_audio(Audio.set_duration(new_clip.duration))
            # newaudio.write_videofile('temp1.mp4')#Path + "//" + Part + "_" + str(i) + ".mp4")
            video = VideoFileClip('temp.mp4')
            video = video.set_audio(AudioFileClip("temp.mp3").set_duration(video.duration))
            # elif Part == 'Chunks':
            #     Chunks.append(Path + "/raw/" + Part + "_" + str(i) + ".mp4")
            Comp.append(Path + "/raw/ComprehensionCheckQuestions_" + str(i) + ".mp4")
            # elif Part == 'MakeTrueSentences':
            #     MakeTS.append(Path + "/raw/" + Part + "_" + str(i) + ".mp4")
            new_clip.write_videofile(Path + "/raw/ComprehensionCheckQuestions_" + str(i) + ".mp4")
        Concatenate(Comp, "OutputComprehensionCheckQuestions.mp4")
        return VideoFileClip("OutputComprehensionCheckQuestions.mp4")
    def genChunks(self, datas):
        pass
    def genMakeTSs(self, datas):
        pass
    def genMovie(self, file):
        NewWords = LoadDb(file, "NewWords")
        CompCheckQuestions = LoadDb(file, "Comp")
        Chunks = LoadDb(file, "Chunks")
        MakeTSs = LoadDb(file, "MakeTS")
        "what"
        NewWordsPart = self.genNewWords(NewWords)
        CompCheckQuestionPart = self.genComps(CompCheckQuestions)
        ChunksPart = self.genChunks(Chunks)
        MakeTSsPart = self.genMakeTSs(MakeTSs)