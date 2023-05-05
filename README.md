Face Morphing
===================

This is a tool to build a face morph video between multiple face images.  This project began as a clone of the
open source project [Face-Morphing](https://github.com/Azmarie/Face-Morphing).

Input: A directory containing images of faces.
Output: A video showing the fluid transformation from one face to the other.

Installation
-------------
1.  Install Python from [here](https://www.python.org/).

2.  Install CMake from [here](https://cmake.org/download/).

3.  Install ffmpeg from [here](https://ffmpeg.org/download.html).

4.  Install the tool in develop mode:

    `python setup.py develop`

Usage
-------------

#### Creating a face morph with a directory containing images.

face-morphing --image_dir images/jake --output output.mp4 --b_spline --duration 2 --hide_lines

Key Features
-------------
1. Detect and **auto align faces** in images (Optional for face morphing)
2. Generate **corresponding features points** between the two images using Dlib's Facial Landmark Detection
3. Calculate the **triangular mesh** with Delaunay Triangulation for each intermediate shape
4. Warp the two input images towards the intermediate shape, perform **cross-dissolve** and obtain intermediate images each frame
5. Packaged into a user-friendly command-line interface.
6. Optionally use B-spline interpolation for calculation of correspondence point positions for warp.

Citations
-------------

Adivces on working with facial landmarks with dlib and opencv https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
