from __future__ import annotations

import sys
import cv2
from pathlib import Path
from argparse import ArgumentParser, Namespace
from face_morphing_tool.utils.face_landmark_detection import generate_face_correspondences
from face_morphing_tool.utils.delaunay_triangulation import make_delaunay
from face_morphing_tool.utils.face_morph import generate_morph_sequence


def face_morphing(image1, image2, output, hide_lines=True, duration=5, frame_rate=20):
    
	"""
	Entry point for the process

	Arguments:
		img1: path to the first image
		img2: path to the second image
		output: output video path
		hide_lines: hide the triangulation lines or not
		duration: duration of the generated video in seconds
		frame_rate: the frame rate in fps

	Returns:
		int -- POSIX complaint exit code (0 for success)
	
	"""
	
	try:
		image1 = cv2.imread(image1)
		image2 = cv2.imread(image2)

		[size, img1, img2, points1, points2, list3] = generate_face_correspondences(image1, image2)

		tri = make_delaunay(size[1], size[0], list3, img1, img2)

		generate_morph_sequence(duration, frame_rate, img1, img2, points1, points2, tri, size, output, hide_lines)
		return 0
	except Exception as e:
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
		"--output <path to the output video>"
		"--hide_lines <hide the trangulation lines or not>"
		"--duration <duration of the generated video in seconds> "
		"--frame_rate <fame rate of the generated video in fps>",
		description="Do face-morphing based on two face images",
	)

	parser.add_argument("--image1", type=str, help="Path to the first image", required=True)
	parser.add_argument("--image2", type=str, help="Path to the second image", required=True)
	parser.add_argument("--output", type=str, help="Path to the output video", required=True)
	parser.add_argument("--hide_lines",type=bool, default=True, help="Hide the triangulation lines")
	parser.add_argument("--duration", type=int, default=5, help="duration of the generated video in seconds")
	parser.add_argument("--frame_rate", type=int, default=20, help="frame rate of the generated video in fps")

	args = parser.parse_args()
	print(args)

	return face_morphing(**vars(args))


if __name__ == "__main__":
    #sys.exit(main())
    #Need to step output of the face-morphing-tool directory in order to use it
	image1 = 'images/Shu/1.png'
	image2 = 'images/Shu/2.png'
	output_path = 'results/output2.mp4'
	face_morphing(image1, image2,output_path)