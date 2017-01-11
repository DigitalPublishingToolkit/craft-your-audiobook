#!/usr/bin/python

import os, subprocess

#makes empty directories to hold txt, wav and mp3 files
p = os.getcwd()
os.mkdir( p+'/txt', 0755 );
os.mkdir( p+'/wav', 0755 );
os.mkdir( p+'/mp3', 0755 );
os.mkdir( p+'/tmp-md', 0755);
os.mkdir( p+'/txt-ref', 0755);

#will store chapter duration values
durations = []



#converts all markdown files inside folder "md" into plain text (will be saved inside folder "txt")
for i in os.listdir('md'):
    if i.endswith(".md") :
        # mdf = os.path.split('md')[1] + '/' + i

        # inliner - converts reference-style Markdown endnotes to Pandoc Markdown's inline footnotes
        # by Louis Goddard <louisgoddard@gmail.com>

        with open('md/'+i, "r") as input:
            text = input.read()
            #remove * as they do not translate well into plain txt
            text = text.replace('*','')
            counter = 0

            while True:
                try:

                    counter = counter + 1

                    ref = "[^" + str(counter) + "]:"
                    nextRef = "[^" + str(counter + 1) + "]:"
                    cite = "[^" + str(counter) + "]"

                    refStart = text.index(ref)
                    tLength = len(text)

                    try:
                        refEnd = text.index(nextRef) - 2
                    except ValueError:
                        break
                        # refEnd = -1
                        # refEnd = text.index(tLength) - 2

                    offset = len(str(counter)) + 5

                    note = "^[" + text[refStart+offset:refEnd] + "]"
                    text = text.replace(cite, note)



                except ValueError:
                    refStart = False

                    break

            # if counter >= 1:
            if refStart == False:
                print("No notes in the document.")
                pass
            else:
                offset = len(str(counter)) + 5

                note = "^[" + text[refStart+offset:len(text)-1] + "]"
                text = text.replace(cite, note)
                text = text.replace("\n    ", " ")
                cutPoint = text.index("\n^")
                text = text[0:cutPoint]
                if counter == 1:
                    print(str(counter) + " note now inline.")
                else:
                    print(str(counter) + " notes now inline.")

            with open('tmp-md/'+i, "w") as output:
                output.write(text)

        #end inliner

        print '////////////////////////////////'
        # print 'Converting ' + mdf
        mdclean = os.path.split('tmp-md')[1] + '/' + i
        print 'Converting ' + mdclean
        txtf =  os.path.split('txt')[1] + '/' +os.path.splitext(i)[0] + ".txt"
        pandoc_args = ['pandoc', '-f', 'markdown-inline_notes', mdclean, '-t', 'plain', '-o', txtf]
        # -f markdown_strict+footnotes (would also work)
        # pandoc -f markdown-inline_notes FINAL.md -t plain -o FINAL-INLINE_NOTES.txt
        subprocess.check_call(pandoc_args)
        print 'Converted ' + mdclean + ' into ' + txtf

        print '////////////////////////////////'
        print 'Deleting file ' + mdclean
        os.remove(mdclean)
        print 'Deleted file ' + mdclean
        continue
    else:
        continue

#removes empty tmp-md folder
print '////////////////////////////////'
print 'Deleting empty "tmp-md" folder'
os.rmdir('tmp-md')

#converts txt files inside folder "txt" into wav (places inside "wav" folder)
for i in os.listdir('txt'):
    if i.endswith(".txt") :
        # f = os.path.split('txt')[1] + '/' + i

        #replace ^ with 'Reference' (more clear and user-friendly to the listener)
        with open('txt/'+i, "r") as input:
            text = input.read()
            text = text.replace('^[',' Reference[')

        with open('txt-ref/'+i, "w") as output:
            output.write(text)

        f = os.path.split('txt-ref')[1] + '/' + i
        forig = os.path.split('txt')[1] + '/' + i

        print '////////////////////////////////'
        print 'Converting ' + f
        fileout =  os.path.split('wav')[1] + '/' +os.path.splitext(i)[0] + ".wav"
        args = ['flite', '-f', f, '-voice', 'rms', '-o', fileout]
        subprocess.check_call(args)
        print 'Converted ' + f + ' into ' + fileout

        print '////////////////////////////////'
        print 'Deleting txt files ' + f + ' and ' + forig
        os.remove(f)
        os.remove(forig)
        print 'Deleted files '  + f + ' and ' + forig

        continue
    else:
        continue

#removes empty txt folder
print '////////////////////////////////'
print 'Deleting empty "txt" folder'
os.rmdir('txt')
os.rmdir('txt-ref')

#adds 1s padding to audio files and converts from wav to mp3
for i in os.listdir('wav'):
    if i.endswith(".wav") :
        wf = os.path.split('wav')[1] + '/' + i
        print 'Adding 1s padding to ' + wf
        finalfile = os.path.split('wav')[1] + '/' +os.path.splitext(i)[0] + "-pad.wav"
        args = ['sox', wf, finalfile, 'pad', '1', '1']
        subprocess.check_call(args)
        print '////////////////////////////////'
        print 'Added 1s padding into ' + finalfile


        #converts wav to mp3
        print '////////////////////////////////'
        print 'Converting ' + finalfile
        mp3f =  os.path.split('mp3')[1] + '/' +os.path.splitext(i)[0] + ".mp3"
        args = ['ffmpeg', '-i', finalfile, '-q:a', '0', mp3f]
        subprocess.check_call(args)
        print 'Converted ' + finalfile + ' into ' + mp3f

        #gets duration
        #ffprobe -show_entries format=duration -sexagesimal mp3/00_colophon.mp3
        #from http://superuser.com/questions/650291/how-to-get-video-duration-in-seconds
        #with thanks to http://trac.ffmpeg.org/wiki/FFprobeTips

        args = ['ffprobe', '-of', 'default=noprint_wrappers=1:nokey=1' , '-show_entries', 'format=duration', '-sexagesimal', mp3f]
        d = subprocess.check_output(args)
        durations.append(d.rstrip()) #removes new lines (\n)

        print '////////////////////////////////'
        print 'Deleting original wav files ' + wf+ ' and ' + finalfile
        os.remove(wf)
        os.remove(finalfile)
        print 'Deleted files ' + wf + ' and ' + finalfile
        continue
    else:
        continue

#removes empty wav folder
print '////////////////////////////////'
print 'Deleting empty "wav" folder'
os.rmdir('wav')

#print the values stored in durations into txt file
with open('durations.txt', 'w') as outfile:
    subprocess.call(["echo", str(durations)], stdout=outfile)
