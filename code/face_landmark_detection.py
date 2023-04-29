import sys
import os
import dlib
import glob
import numpy as np
from skimage import io
import cv2
from imutils import face_utils

class NoFaceFound(Exception):
   """Raised when there is no face found"""
   pass

def calculate_margin_help(img1,img2):
    size1 = img1.shape
    size2 = img2.shape
    diff0 = abs(size1[0]-size2[0])//2
    diff1 = abs(size1[1]-size2[1])//2
    avg0 = (size1[0]+size2[0])//2
    avg1 = (size1[1]+size2[1])//2

    return [size1,size2,diff0,diff1,avg0,avg1]

def crop_image(img1,img2):
    [size1,size2,diff0,diff1,avg0,avg1] = calculate_margin_help(img1,img2)

    if(size1[0] == size2[0] and size1[1] == size2[1]):
        return [img1,img2]

    elif(size1[0] <= size2[0] and size1[1] <= size2[1]):
        scale0 = size1[0]/size2[0]
        scale1 = size1[1]/size2[1]
        if(scale0 > scale1):
            res = cv2.resize(img2,None,fx=scale0,fy=scale0,interpolation=cv2.INTER_AREA)
        else:
            res = cv2.resize(img2,None,fx=scale1,fy=scale1,interpolation=cv2.INTER_AREA)
        return crop_image_help(img1,res)

    elif(size1[0] >= size2[0] and size1[1] >= size2[1]):
        scale0 = size2[0]/size1[0]
        scale1 = size2[1]/size1[1]
        if(scale0 > scale1):
            res = cv2.resize(img1,None,fx=scale0,fy=scale0,interpolation=cv2.INTER_AREA)
        else:
            res = cv2.resize(img1,None,fx=scale1,fy=scale1,interpolation=cv2.INTER_AREA)
        return crop_image_help(res,img2)

    elif(size1[0] >= size2[0] and size1[1] <= size2[1]):
        return [img1[diff0:avg0,:],img2[:,-diff1:avg1]]

    else:
        return [img1[:,diff1:avg1],img2[-diff0:avg0,:]]

def crop_image_help(img1,img2):
    [size1,size2,diff0,diff1,avg0,avg1] = calculate_margin_help(img1,img2)

    if(size1[0] == size2[0] and size1[1] == size2[1]):
        return [img1,img2]

    elif(size1[0] <= size2[0] and size1[1] <= size2[1]):
        return [img1,img2[-diff0:avg0,-diff1:avg1]]

    elif(size1[0] >= size2[0] and size1[1] >= size2[1]):
        return [img1[diff0:avg0,diff1:avg1],img2]

    elif(size1[0] >= size2[0] and size1[1] <= size2[1]):
        return [img1[diff0:avg0,:],img2[:,-diff1:avg1]]

    else:
        return [img1[:,diff1:avg1],img2[diff0:avg0,:]]


def get_average_points(points_list_1, points_list_2):
    assert len(points_list_1) == len(points_list_2)
    result = []

    for i in range(len(points_list_1)):
        x_ave = (points_list_1[i][0] + points_list_1[i][1]) / 2.0
        y_ave = (points_list_1[i][1] + points_list_1[i][1]) / 2.0
        result.append( (x_ave, y_ave) )

    return result


def generate_face_correspondences(images):
    # Detect the points of face.
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('code/utils/shape_predictor_68_face_landmarks.dat')
    corresp = np.zeros((68,2))

    # Assuming all images 1024x1024
    #imgList = crop_image(theImage1,theImage2)

    corr_points = []
    transition_average_points = []

    for image_num in range(images.shape[0]):
        img = images[image_num]

        size = (img.shape[0],img.shape[1])

        currList = []
        corr_points.append(currList)

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.

        dets = detector(img, 1)

        try:
            if len(dets) == 0:
                raise NoFaceFound
        except NoFaceFound:
            print("Sorry, but I couldn't find a face in the image.")

        for k, rect in enumerate(dets):

            # Get the landmarks/parts for the face in rect.
            shape = predictor(img, rect)
            # corresp = face_utils.shape_to_np(shape)

            for i in range(0, 68):
                x = shape.part(i).x
                y = shape.part(i).y
                currList.append((x, y))
                # cv2.circle(img, (x, y), 2, (0, 255, 0), 2)

        # For the second image and above, calculate the average points with the previous image
        if image_num > 0:
            print('Generating transition between {} and {}.'.format(image_num - 1, image_num))
            transition_average_points.append(get_average_points(corr_points[image_num - 1], corr_points[image_num]))


    assert len(corr_points) == images.shape[0]
    assert len(transition_average_points) == images.shape[0] - 1

    return [size, corr_points, transition_average_points]
