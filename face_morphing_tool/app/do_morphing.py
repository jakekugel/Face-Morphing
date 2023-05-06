from __future__ import annotations

import os
import sys
import traceback
import cv2
import numpy as np
from pathlib import Path
from argparse import ArgumentParser, Namespace, BooleanOptionalAction
from face_morphing_tool.utils.face_landmark_detection import generate_face_correspondences
from face_morphing_tool.utils.delaunay_triangulation import make_delaunay
from face_morphing_tool.utils.face_morph import generate_morph_sequence


def face_morphing(image1, image2, image_dir, output, hide_lines, b_spline, bounce, duration=5, frame_rate=20):

	"""
	Entry point for the process

	Arguments:
		image1: path to the first image
		image2: path to the second image
		image_dir: path to directory containing images
		output: output video path
		hide_lines: hide the triangulation lines or not
		b_spline: whether to use b-spline interpolation instead of standard linear interpolation
		duration: duration of the generated video in seconds
		frame_rate: the frame rate in fps

	Returns:
		int -- POSIX complaint exit code (0 for success)

	"""

	try:
		if (image1 or image2) and image_dir:
			raise Exception('the --image_dir argument cannot be used with the --image1 and --image2 arguments.')

		# Read in images
		if image1:
			# Just two images given
			image_test = cv2.imread(image1)
			images = np.zeros((2, image_test.shape[0], image_test.shape[1], image_test.shape[2]), dtype=np.uint8)
			images[0] = cv2.imread(image1)
			images[1] = cv2.imread(image2)
		else:
			# Directory containing images given
			pics = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, file)) and file.lower().endswith('png')]
			images = np.zeros((len(pics), 1024, 1024, 3), dtype=np.uint8)
			for i in range(len(pics)):
				images[i] = cv2.imread(pics[i])

		if len(images) < 3 and b_spline:
			raise Exception('the --b_spline parameter requires at least 3 images.')

		[image_shape, corr_points, transition_average_points] = generate_face_correspondences(images)

		triangulations = make_delaunay(image_shape[1], image_shape[0], transition_average_points, images)

		generate_morph_sequence(duration, frame_rate, images, corr_points, triangulations, image_shape, output, hide_lines, b_spline, bounce)

		return 0
	except Exception as e:
		print('Error: ' + str(e))
		traceback.print_exception(e)
		return 1


def validate_args(args: Namespace):

	"""
	Validate the parsed argument

	Returns:
		bool -- true if valid, false if invalid
	"""

	valid = True

	if not Path(args.imag1).exists():

		valid = False

	if not Path(args.image2).exists():

		valid = False

	return valid


def main():
	parser = ArgumentParser(usage="face-morphing "
		"--image1 <path to the first image> "
		"--image2 <path to the second image> "
		"--output <path to the output video> "
		"--hide_lines <hide the trangulation lines or not> "
		"--duration <duration of the generated video in seconds> "
		"--frame_rate <fame rate of the generated video in fps> "
		"--image_dir <directory containing images for face morph> "
		"--b_spline <use b-spline interpolation> "
		"--bounce <add a bounce effect in each image transition>"
		,
		description="Do face-morphing based on two face images",
	)

	parser.add_argument("--image1", type=str, help="Path to the first image")
	parser.add_argument("--image2", type=str, help="Path to the second image")
	parser.add_argument("--output", type=str, help="Path to the output video", required=True)
	parser.add_argument("--duration", type=int, default=5, help="duration of the generated video in seconds")
	parser.add_argument("--frame_rate", type=int, default=20, help="frame rate of the generated video in fps")
	parser.add_argument("--hide_lines", action=BooleanOptionalAction, help="Hide the triangulation lines" )
	parser.add_argument("--image_dir", required=False, help="Directory containing images.")
	parser.add_argument("--b_spline", action=BooleanOptionalAction, help="If provided, a b-spline is used to interpolate the position of the correspondence points.")
	parser.add_argument("--bounce", action=BooleanOptionalAction, help="If provided, a bouncing effect is applied in each transition.")

	args = parser.parse_args()
	print(args)

	return face_morphing(**vars(args))


if __name__ == "__main__":
    sys.exit(main())
    #Need to step output of the face-morphing-tool directory in order to use it
	# image1 = 'images/Shu/1.png'
	# image2 = 'images/Shu/2.png'
	# output_path = 'results/output2.mp4'
	# face_morphing(image1, image2,output_path)
