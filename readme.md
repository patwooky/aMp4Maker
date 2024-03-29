# a_MP4_Maker v02_03
### Written by Patrick Woo patrickwoo@yahoo.com
### Date: 20191025

## Description
This tool converts image sequence(s) into corresponding MP4 movie file(s), 
and transcodes movie files (mov, avi, flv, etc) into MP4 files.

---
## Usage:
There are a few ways to use this tool.
- from the command-line: `python aMp4Maker arg1 arg2 arg3` where each arg should be a full path of a movie file or a single image from a sequence of images. Please make sure to follow the naming convention for image sequences stated below.

- Drop a single image belonging to a sequence, a movie file, for single seq / single file operation.

- Drop multiple movie files or images belonging to different sequences for multiple specific conversions.

- Drop an entire folder onto the this script 
and MP4 file(s) will be created for each unique sequence of images and each movie file in the folder.

Name of image sequence should follow this convention:

    <base_name>.####.ext

----
## Change log:
### v002_03 (20191025)
-------
- added ./utils to house ffmpeg.exe that can be used independently if ffmpeg.exe is not available in the local machine

### v002_02 (20191023)
-------
- bug fixed: a mov file is interpreted as an image and invoked the message `does not have frame numbers in the expected format: <filename.mov>, skipping basename`.
    A movie file was interpreted as an image when it has more than a 1 file with the same basename (eg, mymovie.mov, mymovie.mp4, mymovie.avi),
    yet does not stick to the filename.###.ext convention.
    I removed the check that required the basename to only have one file present, before it can be processed, else it being treated like an image seq

### v002_01 (20191014)
---
- user can now supply a single file in an image sequence, and tool should be able to detect the sequence and create an mp4 movie
- if user supplies a single movie file, it should run ffmpg to re-encode the movie file into mp4
- if user supplies a folder, it will go through the entire folder converting each unique img seq into mp4, and each movie file into mp4

### v001_01
---
initial code
- user can only supply a folder as source
- can only handle image sequences, cannot convert/transcode movie files.

----
## Configuring the Tool

### Setting up Dependencies

### FFmpeg
[![FFmpeg Logo](https://tigr.net/wp-content/uploads/2016/12/ffmpeg.logo_-150x150.png)](https://ffmpeg.org/)

aMp4Maker requires the free utility FFmpeg (https://ffmpeg.org/) to be present in accessible storage.

Specifically, the full path to `ffmpeg.exe` is stored in the variable `path_ffmpg` in the `config variables` section of the code.

### DJV Imaging
[![DJV Imaging Logo](http://djv.sourceforge.net/images/djv-logo-large.png)](http://djv.sourceforge.net/)

aMp4Maker requires the free viewing/reviewing utility DJV Imaging (http://djv.sourceforge.net/) to be present in accessible storage.

Specifically, the full path to `djv_view.exe` is stiored in the variable `path_djv` in the `config variables` section of the code.

### Setting Up to Run from a Batch File
aMp4Maker can run off the command-line, but the printed messages will be lost when the console window closes before the user can examine the output. 

A better way is to call it from a batch file that has a pause function at the end that waits for a key-press event before the console window goes away.

With the batch file, user can still drag and drop files and folders onto the batch file, and these will still be able to get passed on to the Python tool as arguments.

### Using and Customising the Batch File
The batch file needs to be placed in the same directory as the Python tool.

In the batch file there is a line of code that says:

    R:\Pipeline\App_VHQ\Python27x64\python.exe  %~dp0aMp4Maker.py %*

Change the full python path to your python executable to point to `my\python\dir\python.exe`. 

`%~dp0aMp4Maker.py` passes the full path of `aMp4Maker.py` to Python.

`%*` passes along all the arguments to aMp4Maker.

Once these are all set-up to reflect correct locations on your local machine, you should be able to drop single/multiple files and folders onto the batch file and a console window will now open while while the script is running, and will pause at the end of the script for you to inspect the printed log before closing.
