#!/usr/bin/python

import sys, os, shutil, subprocess, yaml

st = "concat:"
chapNames = []
chapPrefix = []
chapTimes = []

#reads toc.yaml and starts.txt, creates a new file (audiobook.chapters)
c = open('toc.yaml')
chapMap = yaml.safe_load(c)
c.close()

src = open('starts.txt')
lines = [line.rstrip('\n') for line in src]
src.close()

chapKeys = sorted(chapMap.keys())

with open('temp.chapters', 'a') as outfile:
    for i in sorted(chapMap.keys()):
        prefix = str(i.upper())
        chapPrefix.append( prefix )
        chapNames.append(str(i.upper() + 'NAME=' + chapMap[i]))
        subprocess.call(["echo", str(i.upper() + 'NAME=' + chapMap[i]) ], stdout=outfile)
        continue

    for i,line in enumerate(lines):
        chapTimes.append(chapPrefix[i] + "=" + lines[i])
        subprocess.call(["echo", chapTimes[i] ], stdout=outfile)
        continue

#make the chapters file like this:
# CHAPTER1=00:00:00.000
# CHAPTER1NAME=Introduction
# CHAPTER2=00:12:30.000
# CHAPTER2NAME=Chapter 001
# CHAPTER3=00:53:20.000
# CHAPTER3NAME=Chapter 002

#sort file lines
print '////////////////////////////////'
print 'Sorting chapters'
with open('temp.chapters') as f:
    sorted_file = sorted(f)

#save to a file
print '////////////////////////////////'
print 'Saving audiobook chapters into file'
with open('audiobook.chapters', 'w') as f:
    f.writelines(sorted_file)

os.remove('temp.chapters')

#concatenates mpe files into one
print '////////////////////////////////'
print 'Concatenating mp3 files into one'
for indx, filename in enumerate(os.listdir('mp3')):
    fullfilename = os.path.split('mp3')[1] + '/' + filename
    st += fullfilename
    if indx < (len(os.listdir('mp3')) - 1):
        st += "|"

#ffmpeg -i "concat:000.mp3|001.mp3|002.mp3" -q:a 0 chapters.mp3
#-q:a 0 will ensure higher quality mp3
args = ['ffmpeg', '-i', st , '-q:a', '0', 'chapters.mp3']
subprocess.check_call(args)

#removes duration/start files
print '////////////////////////////////'
print 'Deleting duration txt files'
os.remove('durations.txt')
os.remove('starts.txt')

#removes mp3 folder and files
print '////////////////////////////////'
print 'Deleting "mp3" folder and files'
shutil.rmtree('mp3')

#adds chapters to audio file
print '////////////////////////////////'
print 'Adding chapters to audio file'

#MP4Box -add chapters.mp3 -chap audiobook.chapters audiobook-mp3.mp4
mpargs = ['MP4Box', '-add', 'chapters.mp3', '-chap', 'audiobook.chapters',  'audiobook-mp3.mp4']
subprocess.check_call(mpargs)

#removes chapters file
os.remove('audiobook.chapters')
#removes concatenated mp3 files
os.remove('chapters.mp3')

#converts chapters into QT format
print '////////////////////////////////'
print 'Converting chapters into QT format'

#mp4chaps --convert --chapter-qt audiobook-mp3.mp4
chapargs = ['mp4chaps', '--convert', '--chapter-qt', 'audiobook-mp3.mp4']
subprocess.check_call(chapargs)

#adds metadata
print '////////////////////////////////'
print 'Adding metadata'
print '////////////////////////////////'
print 'Type the book\'s title:'
bookTitle = str(raw_input('bookTitle: '))
print 'Type the author\'s name(s):'
bookAuthor = str(raw_input('bookAuthor'))
print 'Type the book\'s publication year:'
bookYear = str(raw_input('bookYear'))

argTitle='album='+str(bookTitle)
argAuthor='album_author='+str(bookAuthor)
argYear='year='+str(bookYear)

#ffmpeg -i audiobook-mp3.mp4 -metadata album_author="Author Name" -metadata album="Book Title" -metadata year="2015" audiobook.final.m4a
metargs = ['ffmpeg', '-i', 'audiobook-mp3.mp4', '-metadata', argAuthor, '-metadata', argTitle, '-metadata', argYear, 'audiobook-tags.m4a']
subprocess.check_call(metargs)

#removes concatenated mp4 file
os.remove('audiobook-mp3.mp4')

#renames it to m4b
print '////////////////////////////////'
print 'Renaming file (m4a -> m4b)'

#mv audiobook-tags.m4a audiobook.m4b
args = ['mv', 'audiobook-tags.m4a', 'audiobook.m4b']
subprocess.check_call(args)

#adds cover pic
print '////////////////////////////////'
print 'Adding cover pic'

#mp4box -itags cover=cover.png audiobook.m4b
picargs = ['mp4box', '-itags', 'cover=cover.png', 'audiobook.m4b']
subprocess.check_call(picargs)
