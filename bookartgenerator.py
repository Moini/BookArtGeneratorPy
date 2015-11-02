'''This program requires Python 2.7 and the Pillow module for Python (convert)

     Licence
     ================
    <Book Art Creator Python Port: Creates patterns from raster images for folding book pages to get book sculptures >
    Copyright (C) 2015  Maren Hachmann

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can reach the author at marenhachmann at-sign yahoo.com.

How to use:
Make sure you have Python 2.7 installed. Also make sure you have the Python module Pillow installed. 
Put a raster image file (jpg or png) of the picture you want on your book into the directory 'MyPictures', 
which the program will create for you when it is run for the first time. 
Make sure you have the permissions to execute scripts in that directory. 
On the command line, go into the directory where the script is and enter

python bookartgenerator.py

Follow the instructions the program gives you. 
Answer the questions regarding your book. 
Be sure to have a ruler on hand. 
To preview the result, look at the file named *-sheets.png. 
To fold your pattern, follow the instructions in *-pattern.txt.

KNOWN PROBLEMS: 
- Images with artifacts (like JPG images, or images created by converting from lossy formats) 
  can cause small unfoldable lines. The program will issue a warning if the picture contains 
  very short lines. It is the responsibility of the user to check if this warning is justified 
  or if the short line is intentional.
- iteritems is no longer available in Python3

If you make a beautiful object of art, please don't hesitate to send me a picture!'''

#This program is written for Python2.7

from PIL import Image as Pimage
import os

# Choose True, if you want single precision in pattern output, e.g. 2.1 or 5.8.
# This setting does not affect the preview, so expect your result to 
# look less detailed than the preview image.
# Also, know that rounding does not always work as expected, due to
# floating point math inaccuracies, see 
# https://docs.python.org/2/tutorial/floatingpoint.html#tut-fp-issues
# for more info.
# Choose False for default, double digit precision, e.g. 2.24 or 5.77.
SINGLE_PRECISION = False

class Book(object):
    """Represents the book the user wants to use. 
    num_pages= number of pages, 
    first= first page which should be folded, 
    last= last page which should be folded, 
    height= height of book as float""" 
    
    def __init__(self):
        parameters = self.get_parameters()
        self.num_sheets = (parameters["last_page"] - parameters["first_page"]) // 2
        self.first = parameters["first_page"]
        self.height = parameters["book_height"]
        self.user_pic = parameters["user_picture"]
        self.file_name = parameters["file_name"]

    def get_parameters(self):
        """Retrieves information about the book from the user"""
        
        parameters = {
                      "first_page" : None,
                      "last_page" : None,
                      "book_height" : None,
                      "user_picture" : None,
                      "file_name" : None,
                     }
        
        while not parameters["first_page"]:
            try:
                temp = int(raw_input("First page of your book: ").strip())
                if temp < 0:
                    print("Please enter a number bigger than zero!!!")
                else:
                    parameters["first_page"] = temp
            except ValueError:
                print("I need a number here. Please try again!")
        
        while not parameters["last_page"]:        
            try:
                temp = int(raw_input("Last page of your book: ").strip())
                if temp <= parameters["first_page"] + 1:
                    print("This would be a very, very small book! Please enter a useful value!")
                else:
                    parameters["last_page"] = temp
            except ValueError:
                print("This must be a whole number, and it must be bigger than the first page.")
        
        while not parameters["book_height"]:
            try:
                temp = float(raw_input("Height of your book (you can use a dot as decimal separator): ").strip())
                temp = round(temp, 2)
                if temp <= 0:
                    print("Oh, really? Please enter a valid measurement!")
                else:
                    parameters["book_height"] = temp
            except ValueError:
                print("Please enter a valid measurement, like 10 or 15.1 or 20.25")
        
        while not parameters["user_picture"]:
            filename = raw_input("Your picture: \n => must be in the directory \"MyPictures\" \n => must be a png or jpg image \n => the picture object must be dark, the background bright \n => the ratio width to height may not be too big if you want it to look good (your picture cannot be very wide) \n => the dark parts must all be connected, there may be holes, but it better not be more than 2 or 3 in any vertical slice)\nName of your picture file: ").strip()
            if filename != "":
                try:
                    parameters["user_picture"] = MyImage(Pimage.open("MyPictures/" + filename))
                    parameters["file_name"] = filename
                except IOError as e:
                    print "Cannot open image file. Please make sure that you entered the name correctly, that it is in the correct location and that it is a valid image file, like png or jpg. (I/O error({0}): {1}".format(e.errno, e.strerror) + ")"
            else:
                print("Please enter a file name here!")

        return parameters
      
    def process_picture(self):
        """uses MyImage class for making the pattern"""
        self.user_pic.make_pattern(self.first, self.num_sheets, self.height, self.file_name)
      
    def __str__(self):
        return "Your Book:\n  Sheets to fold: {sheets} \n  Starting at page number: {pagenum}\n  Height of book: {height}\n  Image file: {filename} ({imgwidth}x{imgheight}px)".format(sheets= self.num_sheets, pagenum = self.first, height = self.height, filename = self.file_name, imgwidth = self.user_pic.size[0], imgheight = self.user_pic.size[1])                                                                                                                                                                                

class MyImage(object):
    """provides a wrapper for the PIL Image class, direct inheritance impossible"""
    
    def __init__(self,img):
        self._img = img
        
    def __getattr__(self,key):
        if key == '_img':
            raise AttributeError()
        return getattr(self._img, key)
      
    def make_pattern(self, first, num_sheets, height, file_name):
        """Calls other functions to make pattern, check pattern, and create preview and pattern text file"""
        
        #prepare for text output and new filenames
        filebase, ext = os.path.splitext(file_name)
        self.file_base = filebase
        
        #resize that copy with the dimensions for the book, destroys aspect ratio
        self.temp = self.resize((num_sheets, int(height * 100)))#Pimage.BICUBIC
        
        #turn transparent areas to white, for all those who don't understand transparency
        if self.temp.mode == "RGBA":
            self.temp.load() # required for png.split()
            self.whitebg = Pimage.new("RGB", self.temp.size, (255, 255, 255))
            self.whitebg.paste(self.temp, mask=self.temp.split()[3]) # 3 is the alpha channel
            
        #convert to greyscale
        self.temp = self.temp.convert("L")

        

        
        #turn it into black and white
        self.temp = self.temp.point(lambda x: 0 if x < 128 else 255, '1')
        
        #Uncomment following line to open a preview picture (on Linux only)
        #self.temp.show()
        
        self.raw_pattern = self.create_raw_pattern()
        self.check_raw_pattern()
        self.smoothe_raw_pattern()
        
        self.final_pattern = self.create_final_pattern()
        
        self.create_pattern_text(first)
        
        self.create_previews()
        

    def create_raw_pattern(self):
        """Creates dictionary with lists of tuples: { x1:[(start, end), (start, end)], 
                                                      x2:[(start, end), (start, end), (start, end)],
                                                      ... }"""
        pattern = dict()
        imagewidth, imageheight = self.temp.size
        
        #loop through width/columns
        for x in range(0, imagewidth):
            #reset for beginning of a column
            white = 255
            black = 0
            y = 0
            
            colorAbove = None
            
            #loop through height
            while y < imageheight:
                currentColor = self.temp.getpixel((x,y))

                while currentColor == black and y < imageheight:
                    #if a dark region begins, or if the column is dark at the top, set a start marker
                    if colorAbove == white or colorAbove == None:
                        start = y
                    #if we reached the end of the column set an end marker
                    if y == imageheight-1:
                        end = y+1 # add one to comprise full dark area
                        pattern.setdefault(x, []).append((start,end))
                    
                    #increment and prepare for next iteration
                    y += 1
                    colorAbove = currentColor
                    if y < imageheight:    
                        currentColor = self.temp.getpixel((x,y))
                    
                while currentColor == white and y < imageheight:
                    #at the border from black to white set an end marker
                    if colorAbove == black:
                        end = y-1 # subtract one to comprise full dark area
                        pattern.setdefault(x, []).append((start,end))
                    
                    #increment and prepare for next iteration
                    y += 1
                    colorAbove = currentColor
                    if y < imageheight:
                        currentColor = self.temp.getpixel((x,y))
                        
        return(pattern)
        
    def check_raw_pattern(self):   
        """Checks the raw pattern dictionary for vertical gaps, closes the program if gaps are found"""
        try:
              column = min(self.raw_pattern)
              endcolumn = max(self.raw_pattern)
        except ValueError:
            print("Ooops - you gave me a picture which is only white (or has too little contrast)!")
            quit()
        
        #check if the picture is empty
        while column < endcolumn:
            column += 1
            #there is no value in the pattern dictionary if the line is all white. White areas at both sides are allowed.
            if column not in self.raw_pattern: 
                print("Sorry, but your picture has vertical gaps (like space between letters, for example) in it, this won't look good!\nPlease use another picture!")
                quit()
        
        #check for too many bands per column
        for column, bands in self.raw_pattern.iteritems():
            if len(bands) > 5:
                print("Your picture has an awful lot of detail! This results in more than 5 alternating folds in some area(s). Please reduce the details in your picture and call this program again.")
                quit()
        
        #check for very short bands, which may be caused by artifacts
        warning_issued = False
        for column, bands in self.raw_pattern.iteritems():
            for band in bands:
                if band[1] - band[0] < BANDTHRESHOLD and warning_issued == False:
                    warning_issued = True
                    print("\nWARNING: The distance between the top and bottom fold for some sheet(s) in your pattern is very short!\nPlease check the *-sheets.jpg file thoroughly for correctness. You can resolve this problem by using a picture without artifacts, or by sheer luck when entering different values for page numbers. It may also be that the short folds are intentional, then just ignore this warning. In the preview, if they appear there, these folds are marked RED.)\n") 
                    #Debug print:
                    #(x: " + str(column) + ", y: " + str(band[1]) + ", size: " + str(self.temp.size) + ")"
    
    def smoothe_raw_pattern(self):
        """Tries to remove small gaps in dark lines, usually caused by artifacts. Experimental!"""
        
        first_sheet = min(self.raw_pattern)
        last_sheet = max(self.raw_pattern)
        
        for column in range(first_sheet, last_sheet):
            bandslist = self.raw_pattern[column]
            
            #only try smoothing if there is more than one band
            if len(bandslist) > 1:
                new_bandslist = [bandslist.pop(0)]
                while len(bandslist) > 0:
                    next_band = bandslist.pop(0)
                    #check if start of next band and end of current band are very close
                    if next_band[0] - new_bandslist[-1][1] < BANDTHRESHOLD:
                        #if so, make them one single band
                        new_bandslist[-1] = (new_bandslist[-1][0], next_band[1])
                    else:
                        #else add the band to the list
                        new_bandslist.append(next_band)
                #replace the original bandslist
                self.raw_pattern[column] = new_bandslist
       
    def create_final_pattern(self):
        """Creates the folding pattern which allows for alternate folding if there are several bands of dark in a line"""

        final_pattern = {}
        
        #for each column in the picture
        for column in range(0, self.temp.size[0]): 
            bands_list = self.raw_pattern.get(column, [])
            #if i is in pattern, count tuples, else count empty list
            num_bands = len(bands_list)
            
            if num_bands == 1:
                final_pattern[column] = bands_list[0]

            elif num_bands != 0:
                final_pattern[column] = bands_list[column % num_bands] #magical modulo, select one of the bands for alternate folding

        #check again if there are gaps, this time probably caused by jpg artifacts in the orgininal picture
        column = min(final_pattern)
        endcolumn = max(final_pattern)
        while column < endcolumn:
            column += 1
            #there is no value in the pattern dictionary if the line is all white. White areas at both sides are allowed.
            if column not in self.raw_pattern: 
                print("Sorry, but your pattern has vertical gaps in it, this is probably caused by artifacts in your picture.\nPlease clean up your picture, or use another one.")
                quit()


        return final_pattern
    
    def create_pattern_text(self, first):
        """Creates a pattern text file for printing"""
        textfile_path = os.path.join(os.path.relpath("MyPatterns"), self.file_base + "_pattern.txt")
        try:
            textfile = open(textfile_path, 'w')
        except IOError as e:
            print "Cannot create pattern text file. Please make sure that the directory 'MyPatterns' exists and that you have permission to write into it. (I/O error({0}): {1}".format(e.errno, e.strerror) + ")"
            
    
        pattern_string = """Book Folding Art Pattern for the Picture \"{filename}\"
==============================================================================

Instructions:

These measurements describe where you will have to fold the pages of your book.
All measurements are given in cm/inch, whichever you chose at the beginning.
The first number indicates the page number, the second tells you where
(measured from the top of the book) you have to fold the upper corner down,
the third tells you where you will have to fold the lower corner up.

  Page     Top Fold     Bottom Fold
==========================================\n\n""".format(filename = self.file_base)

        for column in range(0, self.temp.size[0]):
            # add first page to get the correct page number, double for sheets instead of pages
            pagenum = column * 2 + first
            if column in self.final_pattern:
                # make the number a float with double precision, like 10.15 
                upper_corner = self.final_pattern[column][0]/100.0 
                lower_corner = self.final_pattern[column][1]/100.0
                
                if SINGLE_PRECISION == True:
                    upper_corner = ('%.1f' % round(upper_corner, 1)).rjust(7)
                    lower_corner = ('%.1f' % round(lower_corner, 1)).rjust(7)
                else:
                    upper_corner = ('%.2f' % upper_corner).rjust(6)
                    lower_corner = ('%.2f' % lower_corner).rjust(6)

                pattern_string += "{pagenum}     {upper}        {lower}\n".format(pagenum = str(pagenum).rjust(6), upper = upper_corner, lower = lower_corner)
            else:
                pattern_string += "{pagenum}  No folds, or fold back completely.\n".format(pagenum = str(pagenum).rjust(6))
          
            if pagenum % 10 == 0:
                pattern_string += "------------------------------------------\n"    

    
        pattern_string += """\n\n\nThis pattern was created using the program BookArtGenerator (Python Port).
The program is licenced under the GPLv3.

------------  HAVE FUN FOLDING :-)  ------------ !\n\n""" 
        
        textfile.write(pattern_string)
        textfile.close()
        
        print("Your folding pattern was saved to: " + textfile_path)
      
    def create_previews(self):
        """Saves a preview, uncomment parts to save different kinds of preview"""
        
        #Uncomment the following 4 lines to save a black-and-white copy with correct dimensions for contrast checking
        #bw_preview = self.temp.resize(self.size, Pimage.BICUBIC)
        #filepath = os.path.join(os.path.relpath("MyPatterns"), self.file_base + "_bw.jpg")
        #bw_preview.save(filepath, "JPEG")
        #print("A black-and-white preview was saved as: " + filepath)
        
        #save a copy which shows the individual sheets for checking if alternating folds worked out and detail is enough
        sheet_preview = Pimage.new("RGB", (self.temp.size[0]*3, self.temp.size[1]), color=(255, 255, 255))
        
        black = (0, 0, 0)
        red = (255, 0, 0)
        #create a preview with wrong proportions
        for column, black_area in self.final_pattern.iteritems():
            for y in range(black_area[0], black_area[1]):
                if black_area[1] - black_area[0] >= BANDTHRESHOLD:
                    sheet_preview.putpixel((column*3, y), black)
                else:
                    sheet_preview.putpixel((column*3, y), red)

        sheet_preview.show()

        #Save a disproportionate version of the preview:
        filepath = os.path.join(os.path.relpath("MyPatterns"), self.file_base + "_sheets_disprop.png")
        sheet_preview.save(filepath, "PNG")
        print("A disproportionate preview showing a line for each sheet was saved as: " + filepath)
        
        #resize the preview to correct proportions, preview is at least as big as original image
        width_2_height_orig = self.size[0] / float(self.size[1])
        
        w = sheet_preview.size[0]
        h = int(sheet_preview.size[0] / width_2_height_orig)
        
        min_width = self.size[0]
        min_height = self.size[1]
        
        if w < min_width:
            w = min_width
            h = int(w / width_2_height_orig)
            
        sheet_preview = sheet_preview.resize((w, h))
        filepath = os.path.join(os.path.relpath("MyPatterns"), self.file_base + "_sheets.png")
        sheet_preview.save(filepath, "PNG")
        print("A preview showing a line for each sheet was saved as: " + filepath)

def welcome():
    print("""\nWelcome to your BookArtGenerator (improved Python version)!
---------------------------------\n\n
    BookArtGenerator  Copyright (C) 2015  Maren Hachmann
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions, please look into the script file for details.\n\n""")

# Run the program!
welcome()

# Make sure that the folder structure we need exists
FOLDERS = (("MyPatterns", os.path.relpath("MyPatterns")),("MyPictures", os.path.relpath("MyPictures")))

#the shortest band (in pixels or 10ths of mm/inch) which is allowed to be folded without warning, problem most likely caused by jpg artifacts.
BANDTHRESHOLD = 10 

created_folder = False

for foldername, folder in FOLDERS:
    if not os.path.exists(folder):
        os.makedirs(folder)
        created_folder = True
        print("Created folder '{0}' in current directory!".format(foldername))

if created_folder == True:
    print("Please start the program again and put a picture into the folder 'MyPictures'.")
    quit()

myArtBook = Book()
print myArtBook
myArtBook.process_picture()
