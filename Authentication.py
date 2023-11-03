import os
from aiohttp import Fingerprint
import cv2
from matplotlib import pyplot as plt
from Matcher import *
from random import *


# Authentication class will serve as an authenticator for one person
class Authentication:
    def __init__(self, probe_img, data_path, folder, threshold=0.6):
        self.probe_img = probe_img  # Probe_image_description
        self.genuine_scores = []    # genuine score list
        self.impostor_scores = []   # Imposter score list
        self.authentication_database = []   # random authentication data_base
        self.data_path = data_path      # "Dataset"
        self.folder = folder            # "Probe"
        self.match_dictionary = {}      # dictionary that stores the matches as values and corresponding images that matched as keys
        self.threshold = threshold      # Threshold value that you want to compare when deciding genuine or imposter

    def create_random_authentication_database(self) -> None:
        """
        objective: Creates a random list of images from real folder so that we can have a sort of
        database for authentication
        process: Randomly picks 5 images from the Real folder and appends it to
        self.authentication_database list
        input: None
        output: changes the self.authentication_database list
        """
        real_img_path = os.path.join(self.data_path, "Real")
        real_img_file_names = os.listdir(real_img_path)
        for i in range(0, 5):
            random_idx_for_real_img = randint(0, len(real_img_file_names) - 1)
            random_real_img = real_img_file_names[random_idx_for_real_img]
            self.authentication_database.append(random_real_img)

    def create_match_dict(self) -> None:
        """
        objective: Creates a dictionary where the key is the image name and the value is the match score
        process: computing the match score with every image in the database that the user formed when they
        call the function create_random_authentication_database
        input: None
        output: changes the self.match_dictionary
        """
        probe_img_info_list = self.probe_img.split("_")
        probe_img_folder = probe_img_info_list[0]
        database_path = os.path.join(self.data_path, 'Real')
        probe_path = os.path.join(self.data_path, self.folder, probe_img_folder, self.probe_img)
        real_image_descriptions = os.listdir(database_path)
        probe_image = cv2.imread(probe_path)
        for image_description in self.authentication_database:
            authentication_database_image_path = os.path.join(database_path, image_description)
            real_image = cv2.imread(authentication_database_image_path)
            M = Matcher(real_image, probe_image)
            match_score = M.get_sift_flann_match_score()
            print_description = image_description
            self.match_dictionary[print_description] = match_score
            sorted_match_dict = sorted(self.match_dictionary.items(), key=lambda x: x[1])

    def get_prediction(self) -> int:
        """
        objective: to return whether a correct or incorrect match
        process: gets the score of the image and if the match score is greater than the self.threshold
        then we append it to the self.genuine_scores, otherwise we append it to self.impostor_scores
        input: None
        output: a dictionary with the filename and corresponding match scores
        """
        sorted_match_dict = sorted(self.match_dictionary.items(), key=lambda x: x[1])
        if sorted_match_dict[-1][1] / 100 > self.threshold:
            print('Access Granted')
            self.genuine_scores.append(sorted_match_dict[-1][1] / 100)
            return 1
        else:
            self.impostor_scores.append(sorted_match_dict[-1][1] / 100)
            # print('Access Denied')
            return 0
