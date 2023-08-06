# !usr\bin\env python
# -*- coding:utf-8 -*-

from warnings import filterwarnings
filterwarnings('ignore')

version = '0.0.1'
author = '张乐涛'
datetime = '2019-05-02'


class StepMania:
    def __init__(self, file_name):
        with open(file_name) as file:
            read = file.readlines()
            self.title = read[read[0].find('#TITLE:') + 6:-1]
            self.subtitle = read[read[1].find('#SUBTITLE:') + 9:-1]
            self.artist = read[read[2].find('#ARTIST:') + 7:-1]
            self.titletranslit = read[read[3].find('#TITLETRANSLIT:') + 13:-1]
            self.subtitletranslit = read[read[4].find('#SUBTITLETRANSLIT:') + 16:-1]
            self.artisttranslit = read[read[5].find('#ARTISTTRANSLIT:') + 14:-1]
            self.genre = read[read[6].find('#GENRE:') + 6:-1]
            self.credit = read[read[7].find('#CREDIT:') + 7:-1]
            self.banner = read[read[8].find('#BANNER:') + 7:-1]
            self.background = read[read[9].find('#BACKGROUND:') + 11:-1]
            self.lyricspath = read[read[10].find('#LYRICSPATH:') + 11:-1]
            self.cdtitle = read[read[11].find('#CDTITLE:') + 8:-1]
            self.music = read[read[12].find('#MUSIC:') + 6:-1]
            self.offset = read[read[13].find('#OFFSET:') + 7:-1]
            self.samplestart = read[read[14].find('#SAMPLESTART:') + 12:-1]
            self.samplelength = read[read[15].find('#SAMPLELENGTH:') + 13:-1]
            self.selectable = read[read[16].find('#SELECTABLE:') + 11:-1]
            self.bpms = read[read[17].find('#BPMS:') + 5:-1]
            self.stops = read[read[18].find('#STOPS:') + 6:-1]
            self.backgroundchanges = read[read[19].find('#BGCHANGES:') + 10:-1]

