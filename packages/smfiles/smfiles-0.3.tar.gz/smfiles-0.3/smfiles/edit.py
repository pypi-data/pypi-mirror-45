# !usr\bin\env python
# -*- coding:utf-8 -*-

from .read import is_smfile
from warnings import filterwarnings
filterwarnings('ignore')


class StepMania:
    def __init__(self, file_name):
        try:
            is_smfile(file_name)
        except ValueError as e:
            raise ValueError(str(e))
        except OSError as e:
            raise OSError(str(e))
        if not is_smfile(file_name):
            raise ValueError("This file isn't an effective .sm file.")
        self._file = open(file_name, 'r+')

    def SetTitle(self, title):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[0] = '#TITLE:' + title + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetSubtitle(self, subtitle):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[1] = '#SUBTITLE:' + subtitle + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetArtist(self, artist):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[2] = '#ARTIST:' + artist + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetTitletranslit(self, titletranslit):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[3] = '#TITLETRANSLIT:' + titletranslit + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetSubtitletranslit(self, subtitletranslit):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[4] = '#SUBTITLETRANSLIT:' + subtitletranslit + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetArtisttranslit(self, artisttranslit):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[5] = '#ARTISTTRANSLIT:' + artisttranslit + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetGenre(self, genre):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[6] = '#GENRE:' + genre + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetCredit(self, credit):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[7] = '#CREDIT:' + credit + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetBanner(self, banner):
        list1 = self._file.readlines()
        try:
            with open(banner) as file:
                pass
        except FileNotFoundError:
            raise FileNotFoundError('Banner image file does not exist or the path is incorrect!')
        list1[8] = '#BANNER:' + banner + ';'
        self._file.seek(0)
        self._file.truncate()
        self._file.writelines(list1)

    def SetBackground(self, background):
        self._file.seek(0)
        list1 = self._file.readlines()
        try:
            with open(background) as file:
                pass
        except FileNotFoundError:
            raise FileNotFoundError('Background image file does not exist or the path is incorrect!')
        list1[9] = '#TITLE:' + background + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetLyricpath(self, path):
        self._file.seek(0)
        list1 = self._file.readlines()
        try:
            with open(path) as file:
                pass
        except FileNotFoundError:
            raise FileNotFoundError('Lyric file does not exist or path is incorrect')
        list1[10] = '#LYRICPATH:' + path + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetCDtitle(self, cd):
        self._file.seek(0)
        list1 = self._file.readlines()
        try:
            with open(cd) as file:
                pass
        except FileNotFoundError:
            raise FileNotFoundError('CDtitle image file does not exist or path is incorrect')
        list1[11] = '#CDTITLE:' + cd + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetMusic(self, music):
        self._file.seek(0)
        list1 = self._file.readlines()
        try:
            with open(music) as file:
                pass
        except FileNotFoundError:
            raise FileNotFoundError('Banner image file does not exist or path is incorrect')
        list1[12] = '#MUSIC:' + music + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetOffset(self, offset):
        offset = float(str(offset))
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[13] = '#OFFSET:' + str(offset) + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetSamplestart(self, start):
        start = float(str(start))
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[14] = '#SAMPLESTART:' + str(start) + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetSamplelength(self, length):
        length = float(str(length))
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[15] = '#SAMPLELENGTH:' + length + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetSelectable(self, able):
        if able != 'NO' or able != 'ROULETTE' or able != 'YES':
            raise ValueError
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[16] = '#SELECTABLE:' + able + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetBPM(self, bpm):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[17] = '#BPMS:' + bpm + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetStop(self, stop):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[18] = '#STOPS:' + stop + ';'
        self._file.truncate()
        self._file.writelines(list1)

    def SetBGChanges(self, changes):
        self._file.seek(0)
        list1 = self._file.readlines()
        list1[19] = '#BGCHANGES:' + changes + ';'
        self._file.truncate()
        self._file.writelines(list1)

