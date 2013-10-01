import os

path='.'

dirList=os.listdir(path)

for fname in dirList:
    if ('name_' in fname):
        newfname = fname.replace('name_','')
        #newfname = newfname.replace('Appt-','Appt_')
        os.rename(fname, newfname)
        print fname, ' ->', newfname

print 'done'
