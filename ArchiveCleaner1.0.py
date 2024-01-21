import tkinter as tk
import cv2
import os, glob
import numpy as np
from shutil import copy2
import shutil, sys
from PIL import ImageTk, Image

#This sorts through one or more folders of images, finds any files that match, and lets you decide 
#a) which filename to keep, b) whether to move the file with a new name, or c) whether to keep any at all.
#This is useful if you're moving downloads over from your phone or an old computer for example.
#This is version 1.0, I know there's an easy way to make it more efficent but it was giving me an error so I did it this way for now.
#I might try and add a fancier gui next too.


#Add your folder paths below:

class archiver:
    def __init__(self, root):

        self.destinationfolder = "" #This is the folder where you send the images with the filenames that you want to keep.

        self.folder=""  #This is the first folder you're looking at images from.  

        #self.folder2=""
        #self.folder3=""
        #self.folder4="" #These are optional, you can add more or less.  These are all folders that it's searching from.
        #self.folder5=""

        self.duplicates="" #This is the folder you send duplicate images to for deletion.  This can be the trash folder, but you can also make a new one.

        self.filetypes=["*.jpg","*.jpeg","*.png", "*.webp"] #You can add avif and so on if you deal with other file types a lot.
        self.imagelist=[]

    def shortener(self,string):  #This function gets the short version of a filename.
        index=string.rfind('/')+1
        string=string[index:]
        return string 

    def prefixgetter(self,string):  #This function just gets the path.
        index=string.rfind('/')+1
        string=string[:index]
        return string 

    def iter(self,list):
        self.imagelist.clear()  #This is something I want to fix later, it should be able to run the glob thing once before any of these methods and
                                #just work off a list.  And it should be able to check all the folders with a loop.  It wasn't letting me, but
                                #it's probably not that hard.
        for ext in self.filetypes:
            self.imagelist.extend(glob.glob(os.path.join(self.folder, ext)))  #This checks the first folder.

        #for ext in self.filetypes:
        #    self.imagelist.extend(glob.glob(os.path.join(self.folder2, ext)))   #These are all optional, use one for each folder you want to check.
        #for ext in self.filetypes:
        #    self.imagelist.extend(glob.glob(os.path.join(self.folder3, ext)))
        #for ext in self.filetypes:
        #    self.imagelist.extend(glob.glob(os.path.join(self.folder4, ext)))

        print(len(self.imagelist))
        if len(self.imagelist)>1:
            self.x=(len(self.imagelist)-1)
            self.y=0
            self.everymatch=[self.imagelist[self.y]]
            self.dupindex=[self.y]
            while self.x>0: #All matches with first image in the list.
                if open(self.imagelist[self.y],"rb").read() == open(self.imagelist[self.x],"rb").read():  #This loop checks every image against the first image.
                    self.matchedfile=self.shortener(self.imagelist[self.x])
                    self.foldersrc=self.prefixgetter(self.imagelist[self.x])
                    self.src="{}{}".format(self.foldersrc, self.matchedfile)
                    self.dest="{}{}".format(self.duplicates, self.matchedfile)
                    self.everymatch.append(self.src)                            #All matches are added to a list.
                    self.dupindex.append(self.x) 
                    self.x=self.x-1
                    print(self.x)
                else:
                    self.x=self.x-1
                    print(self.x)
            app.duplicateChooser(self.everymatch)  #This opens a tkinter window with the list of matches, the first image, and three buttons.
        elif len(self.imagelist)==1:
            self.dupindex=[0]
            app.duplicateChooser(self.imagelist)  #This is just for the last image.


    def duplicateChooser(self, list):   #This creates the chooser GUI.
        self.root=root
        self.window1 = tk.Toplevel()
        self.window1.title("Duplicate Chooser")
        self.window1.configure(background="silver")
        self.window1.geometry("1150x700")                #You can change the size of it here, I might make it more responsive to the window content.
        self.window1.grid_columnconfigure((0, 1,2), weight=1)
        self.rownum=1
        self.radionum=0
        self.rad=tk.IntVar()
        self.thisimage = self.imagelist[0] 
        self.image = Image.open(self.thisimage)
        self.max_width = 500
        self.pixels_x, self.pixels_y = tuple([int(self.max_width/self.image.size[0] * x)  for x in self.image.size])
        self.img = ImageTk.PhotoImage(self.image.resize((self.pixels_x, self.pixels_y))) 
        self.label = tk.Label(self.window1, image = self.img)
        self.label.grid(row=0, column=1, padx=5, rowspan=15)
        for radioitem in list:
            self.radio = tk.Radiobutton(self.window1, text="{}".format(radioitem), variable=self.rad, value=self.radionum, highlightbackground="silver",font='helvetica',borderwidth=0,bg="silver", fg="black")
            self.radio.grid(row=self.rownum, column=0)
            self.rownum=self.rownum+1
            self.radionum=self.radionum+1
        #Displaself.y self.imagelist[self.y] with tkinter and the filenames below.
        #Set it here so the "command" appends the selected radio button voter to the main address list.      
        self.renamebutton=tk.Button(self.window1, text="Rename", command= lambda: self.rename(list))
        self.renamebutton.grid(row=self.rownum, column=0)
        self.keepbutton=tk.Button(self.window1, text="Keep", command= lambda: self.keep(self.rad.get()))
        self.keepbutton.grid(row=self.rownum+1, column=0)
        self.deletebutton=tk.Button(self.window1, text="Delete",command= lambda: self.delete(list))
        self.deletebutton.grid(row=self.rownum+2, column=0)


    ##############Here are the functions for the buttons.
    def rename(self, list):   #This opens an input to rename and keep one of the files.
        self.name=""
        self.window2 = tk.Toplevel(self.window1)
        self.newName = tk.StringVar()
        self.entry = tk.Entry(self.window2, textvariable=self.newName)
        self.entry.pack()
        self.submitbutton = tk.Button(self.window2, text = 'Submit', command  = lambda: self.renamer(self.newName.get()))
        self.submitbutton.pack()
        self.window2.mainloop() 

    def delete(self,list):   #Moves all copies to the "duplicates" destination folder (for manual deletion)
        for item in list: 
            shutil.move(item, self.duplicates, copy_function=copy2)
               #This just removes each match as it goes but keeps the first image.
            print("Deleted")
        self.window1.destroy()
        if len(self.imagelist)>0:
            self.root.after(0, self.iter, self.imagelist)



    def keep(self,selection):  #This keeps the filename selected with the radio button.
        if len(self.imagelist)>1:
            self.filetokeep=self.everymatch[selection]
            try:
                shutil.move(self.filetokeep, self.destinationfolder, copy_function=copy2)
                self.everymatch.remove(self.everymatch[selection])
                self.dupindex.remove(self.dupindex[selection])
            except:
                ("Error!")
            self.thisindex=0
            if len(self.everymatch)>0:
                for item in self.everymatch:        
                    try:
                        shutil.move(item, self.duplicates, copy_function=copy2)
                        self.thisindex=self.thisindex+1
                           #This just removes each match as it goes but keeps the first image.
                    except:
                        ("Error!")
        elif len(self.imagelist)==1:
            self.filetokeep=self.imagelist[0]
            try:
                shutil.move(self.filetokeep, self.destinationfolder, copy_function=copy2)
                print("Done!!")
            except:
                ("Error!")
        self.window1.destroy()
        if len(self.imagelist)>0:
            self.root.after(0, self.iter, self.imagelist)
    

    def renamer(self, string):  #This is the input for the renamer function defined above.
        self.name=string
        self.newlocation=self.destinationfolder+self.name
        if len(self.imagelist)>1:
            os.rename(self.everymatch[0], self.newlocation)
            self.everymatch.remove(self.everymatch[0])
            self.thisindex=0
            if len(self.everymatch)>0:
                for item in self.everymatch:        
                    try:
                        shutil.move(item, self.duplicates, copy_function=copy2)
                        self.thisindex=self.thisindex+1                     
                    except:
                        ("Error!")            
            else:
                pass
        elif len(self.imagelist)==1:
            try:
                os.rename(self.imagelist[0], self.newlocation)
            except:
                ("Error!")                   
        self.window2.destroy()
        self.window1.destroy()
        if len(self.imagelist)>0:
            self.root.after(0, self.iter, self.imagelist)

######################################################
#Below this line is the actual code that runs the program.

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = archiver(root)
    root.after(0, app.iter, app.imagelist)
    root.mainloop()
