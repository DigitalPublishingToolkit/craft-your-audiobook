# Craft your audiobook
Semi-automated process to create an audiobook (in m4b format) from markdown files. For further info and a bit of context, check: http://www.publishinglab.nl/blog/2016/07/12/craft-your-own-audiobook/ ‎

For this process, you'll need:
<ul>
  <li>one or more text files in <a href="https://daringfireball.net/projects/markdown/syntax">markdown</a> format (each chapter should have its own file, they should all be located inside directory 'md')</li>
  <li>a cover image (jpg or png)</li>
  <li>a YAML file containing chapter names (simply edit toc.yaml)</li>
  <li><a href="https://www.python.org/downloads/">python (and modules listed below)</a>
    <ul>
      <li>sys</li>
      <li>os</li>
      <li>shutil</li>
      <li>subprocess</li>
      <li>yaml</li>
      <li>datetime</li>
    </ul>
  </li>
  <li><a href="http://pandoc.org/installing.html">pandoc</a></li>
  <li><a href="http://www.speech.cs.cmu.edu/flite/doc/flite_4.html">flite</a></li>
  <li>sox (available as package or you can compile)</li>
  <li><a href="https://ffmpeg.org/download.html">ffmpeg</a></li>
  <li>ffprobe (installed with ffmpeg)</li>
  <li><a href="https://gpac.wp.mines-telecom.fr/downloads/">MP4Box</a></li>
  <li><a href="https://code.google.com/archive/p/mp4v2/">m4chaps</a></li>
</ul>

After installing all required software and downloading these files, make sure you have your content in markdown format (inside directory 'md') and run, <strong>in this order</strong>:
<ul>
  <li>create-chapters.py</li>
  <li>get-durations.py</li>
  <li>pack-chapters.py</li>
</ul>

To run these files, open your Terminal, navigate to the directory where the scripts are located and type

python create-chapters.py

Wait until the script is completely processed and then type the next one. It might take a while. Text-to-speech operations (which occur in the first script) and audio manipulation/concatenation (which occur in the third script) can take <strong>a few minutes</strong> to be completed.
