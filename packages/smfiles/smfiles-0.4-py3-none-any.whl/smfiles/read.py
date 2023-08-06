# !usr\bin\env python
# -*- coding:utf-8 -*-

from warnings import filterwarnings
filterwarnings('ignore')


def is_smfile(file_name):
    with open(file_name) as file:
        read = file.read()
        title = '#TITLE:' in read
        subtitle = '#SUBTITLE:' in read
        artist = '#ARTIST:' in read
        titletranslit = '#TITLETRANSLIT:' in read
        subtitletranslit = '#SUBTITLETRANSLIT:' in read
        artisttranslit = '#ARTISTTRANSLIT:' in read
        genre = '#GENRE:' in read
        credit = '#CREDIT:' in read
        banner = '#BANNER:' in read
        background = '#BACKGROUND:' in read
        lyricspath = '#LYRICSPATH:' in read
        cdtitle = '#CDTITLE:' in read
        music = '#MUSIC:' in read
        offset = '#OFFSET:' in read
        samplestart = '#SAMPLESTART:' in read
        samplelength = '#SAMPLELENGTH:' in read
        selectable = '#SELECTABLE:' in read
        bpms = '#BPMS:' in read
        stops = '#STOPS:' in read
        backgroundchanges = '#BGCHANGES:' in read
        true = str(file.readlines()[0:20]).count(';') >= 20
        read2 = file.readlines()

        if not read2[8][9] == ';':
            file_banner = read2[8][9:-1]
            try:
                open(file_banner).close()
            except FileNotFoundError:
                raise ValueError("Banner image file doesn't exist or the path is incorrect!")

        if not read2[9][12] == ';':
            file_background = read2[9][12:-1]
            try:
                open(file_background).close()
            except FileNotFoundError:
                raise ValueError("The background image file doesn't exist or the path is incorrect!")

        if not read2[10][12] == ';':
            file_lyric = read2[10][12:-1]
            try:
                open(file_lyric).close()
            except FileNotFoundError:
                raise ValueError("The lyric file doesn't exist or the path is incorrect!")

        if not file_name.endswith('.sm'):
            raise OSError('')

        if read2[12][8] == ';':
            raise ValueError("There's no music file!")

        return title and \
            subtitle and \
            artist and \
            titletranslit and \
            subtitletranslit and \
            artisttranslit and \
            genre and \
            credit and \
            banner and \
            background and \
            lyricspath and \
            cdtitle and \
            music and \
            offset and \
            samplelength and \
            samplestart and \
            selectable and \
            bpms and \
            stops and \
            backgroundchanges and \
            true


class StepMania:
    def __init__(self, file_name):
        try:
            is_smfile(file_name)
        except ValueError as e:
            raise ValueError(str(e))
        if not is_smfile(file_name):
            raise ValueError("This file isn't an effective .sm file.")
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

