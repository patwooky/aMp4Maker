##!R:\Pipeline\App_VHQ\Python27x64\pythonw.exe
# coding:utf-8
import os, sys
import subprocess
from pprint import pprint as pp

banner = '''
a_MP4_Maker v02_01
Written by Patrick Woo patrickwoo@yahoo.com
date: 20191014

This tool converts image sequence(s) into corresponding MP4 movie file(s), 
and transcodes movie files (mov, avi, flv, etc) into MP4 files.

Usage:
    Drop a single image belonging to a sequence, a movie file, for single seq / single file operation.
    
    Drop multiple movie files or images belonging to different sequences for multiple specific conversions.

    Drop an entire folder onto the this script 
    and MP4 file(s) will be created for each unique sequence of images and each movie file in the folder.

    Name of image sequence should follow this convention:
        <base_name>.####.ext

'''

changelog = '''

-- change log --
v002_01
-------
- user can now supply a single file in an image sequence, and tool should be able to detect the sequence and create an mp4 movie
- if user supplies a single movie file, it should run ffmpg to re-encode the movie file into mp4
- if user supplies a folder, it will go through the entire folder converting each unique img seq into mp4, and each movie file into mp4

v001_01
-------
initial code
- user can only supply a folder as source

'''

print(banner)
# print(changelog)

# first argv is the python file path
if len(sys.argv) < 2:
    print ('Error: This tool needs a path to an image sequence, or a single image belonging to a sequence.\nTerminating.')
    sys.exit(1)

print('{} args passed in '.format(len(sys.argv)-1))
# pp(sys.argv[1:])

# -- config variables
path_djv = r'R:\Pipeline\App_VHQ\djv_win64\bin\djv_view.exe'
# path_ffmpg = r'H:\patrick\Dropbox\proj\2019\vhq\vhq_pipeline\dos_shell\ffmpeg_bin\ffmpeg.exe'
path_ffmpg = r'R:\Pipeline\_bin\ffmpeg.exe'
imgFormatsDict = ['jpg', 'jpeg', 'png', 'tif', 'exr', 'iff', 'psd', 'tga', 'bmp', 'gif', 'dpx']
movFormatsDict = ['avi', 'asf', 'mp4', 'mpg', 'mpeg', 'mov', 'm4v', 'mkv', 'flv', 'f4v', 'ogg', 
                    'ogv', 'qt', 'rm', 'rmvb', 'webm', 'wmv', '3gp', '3g2']
framerate = 24

foundDjv = False
foundFfmp = False
if (os.path.exists(path_djv)):
    print('djv exists at {}'.format(path_djv))
    foundDjv = True
else:
    print('DJV not found at {}. Movie files will not play using DJV.')

if (os.path.exists(path_ffmpg)):
    print('ffmpeg exists at {}'.format(path_ffmpg))
    foundFfmp = True
else:
    print('The ffmpeg dependency does not exist. Terminating.')
    print('ffmpeg not found: {}'.format(path_ffmpg))
    sys.exit(1)


for this_seq in sys.argv[1:]:
    print ('this seq is {}'.format(this_seq))
    if not os.path.exists(this_seq):
        print ('\nError: does not exist: {}\nSkipping to next item.\n'.format(this_seq))
        continue

    # inFileType - 'm' for movie, 'i' for image. 
    # image mode will result in img seq (multiple images) to mp4 conversion
    # movie mode will result in a single movie to mp4 conversion
    inFileType = '' 

    # if a file is passed in, this would be the basename, if not it will be an empty string
    # only in image seq mode will specificBasename be populated
    specificBasename = '' 

    if not os.path.isdir(this_seq):    
        print('\n\nNot a directory: {}'.format(this_seq))
        # print('This tool currently only supports directory as an input argument. Please only use directories for now.\n\n')
        # continue # skips to the next iteration in the for loop
        
        # determine if this_seq is an image or movie
        thisExt = os.path.splitext(this_seq)[1] # will give '.ext'
        thisExt = thisExt[1:] # taking away the '.' to get 'ext'
        if thisExt.lower() in imgFormatsDict:
            specificBasename = os.path.splitext(os.path.split(this_seq)[1])[0] # will include frame number '.####' at this point
            specificBasename = specificBasename.rsplit('.')[0] # strip away any frame numbers, take the first component of split
            print('\n\nIs a {} image: {}'.format(thisExt, this_seq))
            print('image basename is {}'.format(specificBasename))
            this_path = os.path.abspath(os.path.realpath(os.path.split(this_seq)[0]))
        elif thisExt.lower() in movFormatsDict:
            specificBasename = os.path.splitext(os.path.split(this_seq)[1])[0]
            print('{} is a {} movie.'.format(this_seq, thisExt))
            print('move basename is {}'.format(specificBasename))
            this_path = os.path.split(os.path.abspath(os.path.realpath(this_seq)))[0]
        # continue # skips to the next iteration in the for loop
    else:
        # this_seq is a directory
        this_path = this_seq

    print ('this_path is {}'.format(this_path))
    flist = os.listdir(this_path)
    # print('{} files in {} are'.format(len(flist), this_path))
    # pp(flist)
    # reminder, os.path.splitext will split 'abc.jpg' into ['abc', '.jpg'] watch the '.'
    # filter the file lists to only include recognised image extensions
    flistFiltered = [x.replace('\\','/') for x in flist if os.path.splitext(x)[1][1:].lower() in imgFormatsDict+movFormatsDict]
    # print('{} files after filter'.format(len(flistFiltered)))
    # pp(flistFiltered)
    
    # right now our filenames are without path
    # later we can use os.path.realpath() to get the full path
    
    baseNamesList = [os.path.splitext(x)[0].rsplit('.')[0] for x in flistFiltered]
    # print('baseNamesList is')
    # pp(baseNamesList)
    baseNamesList = list(set(baseNamesList))
    print ('unique base names found: {}, {}'.format(len(baseNamesList), baseNamesList))
    for basename in baseNamesList:
        # check if a specific file/seq to process is passed in, and if this basename is that sequence
        if specificBasename and specificBasename != basename:
            # there is a spacific basename to look for in the directory of files, and this is not that target file / seq
            print('Looking for {} and this is not it. Continuing to the next item.'.format(specificBasename))
            continue

        print('\n\n--== processing {} ==--'.format(basename))
        fseq = [x for x in flistFiltered if basename in x]
        # an fseq item should now be 'basename.1001.exr'
        fseq.sort()
        # print ('fseq is')
        # pp(fseq)
        # ascertain if the file is an image or a movie
        if len(fseq)==1 and os.path.splitext(fseq[0])[1][1:] in movFormatsDict:
            # this basename is a movie file
            inFileType = 'm'
            # no specific name it means that all files can be converted
            # make movie ffmpeg file command
            formattedFilename = fseq[0]
            formattedFilenameFull = os.path.join(this_path, formattedFilename)
            # formattedFilenameFull = 
            print('formattedFilenameFull is {}'.format(formattedFilenameFull))
            
            # usually for movie file conversion we will export to the same directory
            # and name the output file exactly the same as the input with the output extension changed to .mp4
            mp4OutPath = '{}.mp4'.format(os.path.join(this_path,basename))
            # %ffmp% -i "%~f1" -vf "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2" -hide_banner %outputmp4%
            ffmpgCmd = '{} -i {} -vf "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2" -hide_banner {}'.format(path_ffmpg, formattedFilenameFull, mp4OutPath)
        else:
            # this baseneame is an image sequence
            inFileType = 'i'
            try:
                # ascertain the number padding in frame numbers
                numPadding = sum([len(os.path.splitext(x)[0].rsplit('.')[1]) for x in fseq])/len(fseq) # average across paddings in all frames
            except:
                print('Does not have frame numbers in expected format: {}\nSkipping basename.'.format(fseq[0]))
                continue
            # print('numpadding is {}'.format(numPadding))

            # get the min and max frame numbers
            # print([fseq[0], fseq[-1]])
            minMaxFramesList = [int(os.path.splitext(x)[0].rsplit('.')[1]) for x in [fseq[0], fseq[-1]]]
            # print('minMaxFramesList is {}'.format(minMaxFramesList))
            
            # take the first file's extension and use it to define the sequence's extension
            # again this will give us '.ext'
            imgExt = os.path.splitext(fseq[0])[1]
            imgExt = imgExt[1:]
            # formattedFilename will be something like: 'basename.%04d.png'
            formattedFilename = '{}.%0{}d.{}'.format(basename, numPadding, imgExt)
            # print(formattedFilename)
            # print('this_path is {}'.format( this_path ))
            # fseqFull = [os.path.join(this_path, x).replace('\\', '/') for x in fseq if os.path.exists(os.path.join(this_path, x))]
            # pp(fseqFull)
            formattedFilenameFull = os.path.join(this_path, formattedFilename)
            # print ('formattedFilenameFull is {}'.format(formattedFilenameFull))

            # output image to put in a path that is 1 level up from the img seq
            # we usually put movie files one level up from the hundreds of images
            mp4OutPath = '{}.mp4'.format(os.path.join(os.path.split(this_path)[0],basename))
            # print('mp4OutPath is {}'.format(mp4OutPath))

            # build ffmpeg command
            # -vf "pad= " will deal with width & height pixels, adding 1 to pixel count if original width/height cannot be divided by 2            
            ffmpgCmd = '{} -start_number {} -framerate {} -i {} -vf "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2" -hide_banner {}'.format(\
                        path_ffmpg, minMaxFramesList[0], framerate, formattedFilenameFull, mp4OutPath)
        print('ffmpgCmd is:\n{}'.format(ffmpgCmd))
        print('running ffmpeg now')
        
        # calling with os.system()
        os.system(ffmpgCmd)
        
        # calling with subprocess
        # try:
        #     subprocess.call([ffmpgCmd])
        # except OSError:
        #     print ('ERROR: ffmpeg raised errors!')
        print('\n--== Finished processing {} ==--'.format(basename))
    # end for basename in baseNamesList
# end for this_seq
print('end of items to convert')


# playback section after conversion

try:
    # if the creation fails, mp4OutPath will be undefined

    # specify the path to movie
    # foundDjv=False
    if foundDjv:
        # this will use djv to open the movie
        subprocess.call([path_djv, mp4OutPath])
    else:
        # using the shell to launch the default player, like passing a command to dos prompt in shell
        # the following will play the movie using the OS default player assigned to handle the file type
        os.system(mp4OutPath)
except:
    pass