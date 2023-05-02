from face_landmark_detection import generate_face_correspondences
from delaunay_triangulation import make_delaunay
from face_morph import generate_morph_sequence

import subprocess
import argparse
import shutil
import os
import cv2
import numpy as np
import utils.misc

def doMorphing(images, duration, frame_rate, output, show_lines, b_spline):

	[image_shape, corr_points, transition_average_points] = generate_face_correspondences(images)

	triangulations = make_delaunay(image_shape[1], image_shape[0], transition_average_points, images)

	generate_morph_sequence(duration, frame_rate, images, corr_points, triangulations, image_shape, output, show_lines, b_spline)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--img1", required=False, help="The First Image")
	parser.add_argument("--img2", required=False, help="The Second Image")
	parser.add_argument("--duration", type=int, default=5, help="The duration")
	parser.add_argument("--frame", type=int, default=20, help="The frame Rate")
	parser.add_argument("--output", help="Output Video Path")

	# Added by Jake
	parser.add_argument("--hide_lines", action=argparse.BooleanOptionalAction, help="Hide the triangulation lines" )
	parser.add_argument("--image_dir", required=False, help="Directory containing images.")
	parser.add_argument("--b_spline", action=argparse.BooleanOptionalAction, help="If provided, a b-spline is used to interpolate the position of the correspondence points.")

	args = parser.parse_args()

	if (args.img1 or args.img2) and args.image_dir:
		print("Error:  the --image_dir argument cannot be used with the --img1 and --img2 arguments.")

	# Read in images
	if args.img1:
		# Just two images given
		images = np.zeros((2, image1.shape[0], image1.shape[1], image1.shape[2]), dtype=np.uint8)
		image[0] = cv2.imread(args.img1)
		image[1] = cv2.imread(args.img2)
	else:
		# Directory containing images given
		pics = [os.path.join(args.image_dir, file) for file in os.listdir(args.image_dir) if os.path.isfile(os.path.join(args.image_dir, file)) and file.lower().endswith('png')]
		images = np.zeros((len(pics), 1024, 1024, 3), dtype=np.uint8)
		for i in range(len(pics)):
			images[i] = cv2.imread(pics[i])

	print('Loaded {} images'.format(images.shape[0]))

	doMorphing(images, args.duration, args.frame, args.output, args.hide_lines, args.b_spline)
