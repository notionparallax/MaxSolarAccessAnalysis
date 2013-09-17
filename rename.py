import re

path='/home/ben/Dropbox/Public/sites/dataStory/MaxSolarAccessAnalysis/Images'

dirList=os.listdir(path)

for fname in dirList:
    if ('Diversity_Wall' in fname):
        newfname = fname.replace('Diversity_Wall','Diversity-Wall')
        os.rename(fname, newfname)
        print fname, ' ->', newfname
    if ('Growth_RoomA' in fname):
        newfname = fname.replace('Growth_RoomA','Growth-RoomA')
        os.rename(fname, newfname)
        print fname, ' ->', newfname
    if ('Growth_RoomB' in fname):
        newfname = fname.replace('Growth_RoomB','Growth-RoomB')
        os.rename(fname, newfname)
        print fname, ' ->', newfname

print 'done'
