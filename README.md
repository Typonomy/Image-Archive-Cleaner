# Image Archive Cleaner

This sorts through one or more folders of images, finds any files that match, and lets you decide 
a) which filename to keep, b) whether to move the file with a new name, or c) whether to keep any at all.
This is useful if you're moving downloads over from your phone or an old computer for example.
This is version 1.0, I know there's an easy way to make it more efficent but it was giving me an error so I did it this way for now.

In order to use it, go into the file and manually add the folders you want to search.  Choose or create two additional folders, one for the images you want to keep and one for the duplicates to go to. 

Requires installation of tkinter.  I see that I imported OpenCV but I don't know why, it's probably not necessary but I just saw it right now so I'll fix it later.

I might try and add a fancier gui in the next version that has normal inputs for the folders.


1.2 - Fixed an error in the delete function that would throw an error if multiple files to be deleted had the same name.  It works now.  The keep function should be having the same problem, albeit less often, but it hasn't told me yet because it has an exception, so if it happens it's just moving along.  I'll test that later.
