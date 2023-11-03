import os
# from aiohttp import Fingerprint
import cv2
import random
import numpy as np


class Matcher:
    # constructor of the class and initializes everything that we need
    def __init__(self, template, probe):
        self.template = template
        self.probe = probe

    # matcher function where it matches the fingerprints by the given sample
    def get_sift_flann_match_score(self):
        """
         fast library for approx best match KNN
        Flann Based Matcher performs a fast local approximate nearest neighbors (FLANN) calculation between two
        sets of feature vectors. The result is two NumPy arrays. The first is a list of indexes of the matches,
        while the second contains the values of match distances.
        :return: match_score as a percentage (float)
        """
        sift = cv2.SIFT_create()  # creating an SIFT object\
        template_keypoints, template_des = sift.detectAndCompute(self.template, None)
        probe_keypoints, prob_des = sift.detectAndCompute(self.probe, None)
        matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 10}, {}).knnMatch(prob_des, template_des, k=2)

        # No idea what is going on here
        match_points = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        # The number of key points won't be necessarily same for both template and probe image
        # Comparing the minimum number of key points, the min of the two
        if len(probe_keypoints) <= len(template_keypoints):
            total_keypoints = len(probe_keypoints)
        else:
            total_keypoints = len(template_keypoints)

        # calculating the match score as percentage
        match_score = len(match_points) / total_keypoints * 100
        return match_score
