import numpy as np
import cv2
import sys
import os
import math
from subprocess import Popen, PIPE
from PIL import Image
import utils.misc

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def apply_affine_transform(src, srcTri, dstTri, size) :

    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morph_triangle(img1, img2, img, t1, t2, t, alpha) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))

    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []

    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))

    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warpImage1 = apply_affine_transform(img1Rect, t1Rect, tRect, size)
    warpImage2 = apply_affine_transform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    try:
        img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask
    except ValueError as e:
        print('Error: ' + str(e))
        print('    img: {}'.format(str(utils.misc.array_info(img))))
        print('    mask: {}'.format(str(utils.misc.array_info(mask))))
        print('    imgRect: {}'.format(str(utils.misc.array_info(imgRect))))
        print('    r[0] = {}'.format(r[0]))
        print('    r[1] = {}'.format(r[1]))
        print('    r[2] = {}'.format(r[2]))
        print('    r[3] = {}'.format(r[3]))


def generate_morph_sequence(duration, frame_rate, images, points, triangulations, size, output, hide_lines):

    # Number of frames per transition
    num_frames = int(duration*frame_rate)

    p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-r', str(frame_rate),'-s',str(size[1])+'x'+str(size[0]), '-i', '-', '-c:v', 'libx264', '-crf', '25','-vf','scale=trunc(iw/2)*2:trunc(ih/2)*2','-pix_fmt','yuv420p', output], stdin=PIPE)

    for transition_num in range(len(triangulations)):
        for j in range(0, num_frames):

            # Convert Mat to float data type
            img1 = np.float32(images[transition_num])
            img2 = np.float32(images[transition_num + 1])

            # Read array of corresponding points
            interpolated_points = []
            alpha = j/(num_frames - 1)

            # Compute weighted average point coordinates
            for i in range(0, len(points[transition_num])):
                x = (1 - alpha) * points[transition_num][i][0] + alpha * points[transition_num + 1][i][0]
                y = (1 - alpha) * points[transition_num][i][1] + alpha * points[transition_num + 1][i][1]
                interpolated_points.append((x,y))

            # Allocate space for final output
            morphed_frame = np.zeros(img1.shape, dtype = img1.dtype)

            for i in range(len(triangulations[transition_num])):
                x = int(triangulations[transition_num][i][0])
                y = int(triangulations[transition_num][i][1])
                z = int(triangulations[transition_num][i][2])

                t1 = [points[transition_num][x], points[transition_num][y], points[transition_num][z]]
                t2 = [points[transition_num + 1][x], points[transition_num + 1][y], points[transition_num + 1][z]]
                t = [interpolated_points[x], interpolated_points[y], interpolated_points[z]]

                # Morph one triangle at a time.
                morph_triangle(img1, img2, morphed_frame, t1, t2, t, alpha)

                pt1 = (int(t[0][0]), int(t[0][1]))
                pt2 = (int(t[1][0]), int(t[1][1]))
                pt3 = (int(t[2][0]), int(t[2][1]))

                if not hide_lines:
                    cv2.line(morphed_frame, pt1, pt2, (255, 255, 255), 1, 8, 0)
                    cv2.line(morphed_frame, pt2, pt3, (255, 255, 255), 1, 8, 0)
                    cv2.line(morphed_frame, pt3, pt1, (255, 255, 255), 1, 8, 0)

            res = Image.fromarray(cv2.cvtColor(np.uint8(morphed_frame), cv2.COLOR_BGR2RGB))
            res.save(p.stdin,'JPEG')

    p.stdin.close()
    p.wait()