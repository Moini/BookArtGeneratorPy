# BookArtGeneratorPy
Python version of BookArtGenerator with improved support for transparency, smoothing and an additional proportionate preview picture. Requires Pillow and Python 2.7.

This script will create a folding pattern for you if you provide it with an image.

Folding the pattern will turn a dull book into real art.

The program file for 'BookArtGenerator' is bookartgenerator.py. 

To run, it requires Python 2.7 and the PILLOW python module.  

I can only debug the program on Linux, so if you have difficulties on Windows, you will need to help with debugging.

NOTE: If you would like to use an even more improved, javascript-based online version, then go visit http://vektorrascheln.de/bookart.html

##How to use:
Make sure you have Python 2.7 and PILLOW installed.

Copy the script into a new directory on your computer.
Run the script once to automatically create the necessary subdirectories:

python bookartgenerator.py

(or python2 bookartgenerator.py, if python3 is your standard python)

Create a raster image file which fulfills the following requirements:

- With a not very detailed, dark object 
- Object may contain holes, or consist of several simple shapes, but there may be no gaps which go from top of the picture to the bottom
- Object in front of a bright background
- Object's width-to-height ratio must be within reasonable limits, you cannot open a book endlessly ;-)
- If there are holes or gaps in the object, make sure that there are no more than 5 holes in every orthogonal line. Less will turn out better.

Examples of a good choice: continuously written short words, single letters, simple silhouettes, all black on white...  
Examples of a bad choice: photo, colourful drawings with many details, words with more than 6 letters,...

Make sure you have the permission to reproduce the picture (for example, take a public domain picture from http://openclipart.org/ ).

Make sure you have the permissions to execute scripts in the script directory.   

Run the script again and answer its questions regarding your book. Be sure to have a ruler - and of course, the book - on hand. Put the picture file into the directory where it asks you to put it.

When the program has finished, to preview the result, look into the files the program tells you to look into.

One of them has the correct aspect ratio, but the width of the single lines varies due to resizing artifacts, while the other preview is distorted, but shows all lines crisp and clear. Every page is represented by an orthogonal line. The spaces in between are just to separate the lines more clearly for easier controlling.   
You will be able to control the aspect ratio of the final result by opening your book wider or pushing it more closed.  
Check if the details are all there and if the alternating page folding pattern creation has worked.  
To fold your pattern, follow the instructions in the *.txt file.

If you would like to change the precision of the text pattern to single digit, then open the script file and change line 60 ("SINGLE_PRECISION = False") to 
SINGLE_PRECISION = True
Read the comment in the lines above that line in the script to know what that means exactly.

If you make a beautiful object of art, please don't hesitate to send me a picture!

Please note the licence (AGPLv3) in the separate file and at the top of the program script.
