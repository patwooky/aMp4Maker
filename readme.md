# a_MP4_Maker v02_01
### Written by Patrick Woo patrickwoo@yahoo.com
### Date: 20191014

## Description
This tool converts image sequence(s) into corresponding MP4 movie file(s), 
and transcodes movie files (mov, avi, flv, etc) into MP4 files.

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
## change log:

### v002_01
---
- user can now supply a single file in an image sequence, and tool should be able to detect the sequence and create an mp4 movie
- if user supplies a single movie file, it should run ffmpg to re-encode the movie file into mp4
- if user supplies a folder, it will go through the entire folder converting each unique img seq into mp4, and each movie file into mp4

### v001_01
---

initial code
- user can only supply a folder as source
