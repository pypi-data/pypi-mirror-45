# How to use this package


from smfiles import read, edit, version, datetime


print(read.StepMania('xxx.sm').bpms)


>>> 0.000=156.000, 8.000=312.000


edit.StepMania('yyy.sm').SetTitle('mytitle')


print(version, datetime)

