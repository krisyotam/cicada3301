# Hit or Miss

I should be clear from the start that I'm not batting in the dark here. I have fairly extensive experience in image and text processing, though my cryptography knowledge may be lacking. I'm relying pretty heavily on my technical knowledge to ensure that when I swing, I'll at least make contact. 

### Alphabet Creation

I knew that I would need a full transcription of the pages before any decrypting could be attempted. To that end, I began work automating the task that I had attempted manually: transcribing the text. Though the text was not a character set I recognized, it did appear to have a consistent font and character size. Ideal conditions for a [hit or miss filter]()! I started work immediately, painstakingly cropping each character out of whichever page they could be found. After a couple curious looks and shushed questions from my fellow D&D mates, I finally had all 32 characters of this mysterious language isolated.

Knowing that the imperfect borders produced by my cropping could introduce errors in later processes, I quickly wrote a [script](https://github.com/ralphatobe/cicada-3301/blob/master/process_images.py) to load each image, binarize it, crop away any padding surrounding the character, and repad the image consistenly with 5 pixels in each direction. After running the first bit of code for this project, I was ready to move on to the first real challenge to tackle!

### Initial Hit or Miss

I had the pages, I had the characters, it was time to start the identification! I began by searching strictly for exact matches between my alphabet and each page. As expected, small differences (possibly caused by JPEG artifacts affecting the binarization process) resulted in many missed characters. With this simple method proven inadequate, I moved on to the next easiest process: erosion with a 3x3 kernel and searching with the eroded image. Unfortunately, this method resulted in too many false positives. As expected, a hit or miss filter would be necessary to get reasonable results. After some quick implementation with OpenCV, I got the following results.

 Binarized Image | Exact Match  
:---------------:|:-----------:
![binarized image](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_original.png "Binarized Image") | ![exact match](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_exact.png "Exact Match") | 

Eroded Kernel | Hit or Miss 
:-------------:|:-----------:
![dilate](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_dilate.png "Dilated Image") | ![hit or miss](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_hom.png "Hit or Miss")

Comparing the hit or miss image to the original reveals three new problems: scale variance, kerning, and subcharacter overlap.

### Scale Variance

 Binarized Image | Hit or Miss
:---------------:|:----:
![binarized image](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/start_char.png "Binarized Image") | ![hits](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/missing_start.png "Hits")

Though hit or miss filters are great for identifying slight changes in a consistent font, they cannot deal with significant changes in font size. As a result, none of the large characters at the start of each section are captured. I could collect a second set of cropped characters at the appropriate scale, but such an effort would likely amount to more work than manually typing out the first character for each page. Alternately I could determine the scale difference between the normal and large characters, rescale the collected characters, and run the hit or miss filter on the resulting image to find the larger characters. For the time being, we'll be forging onward accepting that our transcriptions will have that slight error.

### Kerning

 Binarized Image | Hit or Miss
:---------------:|:----:
![binarized image](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/chars.png "Binarized Image") | ![hits](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/missing_chars.png "Hits")

If you look closely at the middle of the hit page, you'll notice that two characters are missing completely! Upon closer inspection, you'll see that these two characters are much closer to each other than the majority of the characters in the page (the typography term for this being kerning). A small bit of experience with hit or miss filters will inform you that the filter needs whitespace surrounding each character to make a proper identification. Without that precondition met, we'll have to find a workaround.

The solution I came up with seems fairly straightforward. Instead of using the typical dilation operations on the filter kernels, I chose to erode the image itself, artificially widening the spaces between different characters. Two different kernels are used for the erosion, to provide more rounded separation (square kernels caused persistent false negatives for the 'D' character). The new hit images are shown below.

 Binarized Image | Modified Hit or Miss
:---------------:|:----:
![binarized image](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_original.png "0_Binarized Image") | ![hits](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_hits.png "0_Hits")

### Subcharacter Overlap

 Binarized Image | Hit or Miss
:---------------:|:----:
![binarized image](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/normal_char.png "Binarized Image") | ![hits](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/highlight_char.png "Hits")

Great! We've found every true positive, but why are there two intensities in the hit image? Unforunately, the brighter characters indicate false positives occurring due to complete subcharacter overlap. Examining the character set reveals three characters that perfectly contain a different character from our alphabet.

 Character | ![Y](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/Y.png "Y") | ![4 dots](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/dots_4.png "4 Dots") | ![13 dots](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/dots_13.png "13 Dots")
:-:|:-:|:-:|:-:
Subcharacter | ![U](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/U.png "U") | ![1 dot](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/dots_1.png "1 Dot") | ![1 dot](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/dots_1.png "1 Dot")

Well, this is a bit of an issue... there's really no easy way to alter the filter that will remove these false positives. Looks like a job for postprocessing!

At this point in the code, we've collected labelled lists of hit pixels for each character. Connected collections of hit pixels are consolidated by the recursive function find_blob in [process_images.py](https://github.com/ralphatobe/cicada-3301/blob/master/process_images.py), giving us a list of centroid-character pairs. Using these labelled centroids, user-defined character prioritization, and the size of the supercharacter, we can easily identify false positives by checking if they overlap with the higher priority character. This process is executed by prioritize_chars in [process_images.py](https://github.com/ralphatobe/cicada-3301/blob/master/process_images.py) and it leaves only true positives!

 Binarized Image | Prioritized Hit or Miss
:---------------:|:----------------:
![binarized image](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_original.png "0_Binarized Image") | ![hits](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_prioritized.png "0_Hits")

[return home](index.md)
