#!/usr/bin/python

import os, subprocess, datetime

chapStarts = 0

with open('starts.txt', 'w') as outfile:
    for i in os.listdir('mp3'):
        if i.endswith(".mp3") :
            subprocess.call(["echo", str(datetime.timedelta(seconds=chapStarts))], stdout=outfile)
            print '////////////'
            print chapStarts
            print '////////////'
            #gets duration of mp3 files
            mp3f =  os.path.split('mp3')[1] + '/' +os.path.splitext(i)[0] + ".mp3"
            #outputs durations in seconds (use '-sexagesimal' for formatted output)
            sargs = ['ffprobe', '-of', 'default=noprint_wrappers=1:nokey=1' , '-show_entries', 'format=duration',  mp3f]
            s = subprocess.check_output(sargs)
            chapStarts = chapStarts + int(float(s))
            continue
        else:
            continue

