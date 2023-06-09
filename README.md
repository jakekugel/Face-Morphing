Face Morphing
===================

This is a tool to build a face morph video between multiple face images.  This project began as a clone of the
open source project [Face-Morphing](https://github.com/Azmarie/Face-Morphing).

* Input: A directory containing images of faces.
* Output: A video showing the fluid transformation from one face to the other.

Installation
-------------
1.  Install Python from [here](https://www.python.org/).

2.  Install CMake from [here](https://cmake.org/download/).

3.  Install ffmpeg from [here](https://ffmpeg.org/download.html).

4.  Install the tool:

    `python setup.py install`

Key Features
-------------
The following features were part of the origin [Face-Morphing](https://github.com/Azmarie/Face-Morphing) project that this app was based on.

1. Optionally detect and auto-align faces in the images.
2. Use the dlib open-source tool to identify the facial landmarks used as correspondence points.
3. Use Delaunay triangulation to construct the triangular mesh for the correspondence points.
4. Interpolate the positions of the correspondence points between two images, warp the images, and use cross-dissolve to construct each intermediate frame.

The following features are new additions that were added for the class project.

1. Packaged into a user-friendly command-line app.
2. Added an option to read all images in a directory and create a face morph video with mutiple images.
3. Added an option for B-spline interpolation for calculation of correspondence point positions for warp.
4. Added an option to create a bounce effect in the transition between each image pair.

Example Usage
-------------
#### Create a standard face morph between two specific images, and save results as 'output.mp4'
`face-morphing --image1 images/aligned_images/jennie.png --image2 images/aligned_images/rih.png --output output.mp4 --hide_lines`

#### Create a face morph with a directory containing multiple images.
`face-morphing --image_dir images/jake --output output.mp4 --duration 2 --hide_lines`

#### Create a face morph that utilizes B-spline interpolation of correspondence points.
`face-morphing --image_dir images/jake --output output.mp4 --b_spline --duration 2 --hide_lines`

#### Create a face morph that adds a bounce effect in the transition between images.ints.
`face-morphing --image_dir images/jake --output output.mp4 --bounce --duration 2 --hide_lines`

Parameter Help
--------------
**--image1 <filename>**

The first image to use in the face morph.  If the --image1 parameter is used, the --image2 parameter is also required.

**--image2 <filename>**

The second image to use in the face morph.  If the --image2 parameter is used, the --image1 parameter is also required.

**--image_dir <directory name>**

The directory containing images to use in a face morph.  All images in the directory are used.  This is an alternative to
--image1 and --image2.

**--output <filename>**

The file name of the generated face morph video.

**--duration**

Optional, the number of seconds for each transition.  Default is 5.

**--b_spline**

Optional, if provided a B-spline interpolation is used to calculate the position of the correspondence points.

**--hide_lines**

Optional, if provided, the triangulation lines are not shown.

**--bounce**

Optional, if provided, a bouncing effect is applied to each transition.


References and Resources
------------------------
[1] Wang, Azmarie.  "Face Morphing–A Step-by-Step Tutorial with Code".  Medium.com.  https://azmariewang.medium.com/face-morphing-a-step-by-step-tutorial-with-code-75a663cdc666  (accessed 2/1/2023).

[2] Wang, Azmarie.  https://github.com/Azmarie/Face-Morphing. (accessed 2/1/2023).

[3] Adams, Peter.  "Faces of Open Source".  https://www.facesofopensource.com/ (accessed 2/1/2023).

[4] The SciPy community. "scipy.interpolate.BSpline".  https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BSpline.html (accessed 2/1/2023)/

