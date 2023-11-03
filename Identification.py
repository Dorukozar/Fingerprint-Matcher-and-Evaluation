from matplotlib import pyplot as plt
import os
import cv2
from matplotlib import pyplot as plt
from Matcher import *
from random import *


# In Identification.py you have to implement an identification system via fingerprints. For example, when a sample
# fingerprint is provided,
# it needs to search the entire dataset and try to figure out who that person is by comparing fingerprints.
# You have to have an object-oriented design
# Because we have 3 different folders that are Easy, Medium, and Hard, I highly recommend having at least 1
# parameter for the identify that is either going to be "Probe-Easy", "Probe-Medium", or "Probe-Hard"
# So if you want to run through all eas, medium and hard; you have to call the identify method 3 times
# I went ahead and did the constructor for you. For the constructor, this is actually all you need but you can add
# more variables if you like.
# After you downloaded the actual data set from the link that is provided in the readme file, you can uncomment the
# actual data-set path but
# WARNING: the actual and test data-sets are taking too long to run. I highly recommend making a breakpoint in the code
# Use the code from the previous homework that you implemented to plot ROC and DET curves and also computing the EER.


class Identification:
    def __init__(self, probe_image_path, probe_folders_path, template_path, threshold=0.5):
        self.probe_image_path = probe_image_path  # probe image full path
        self.probe_image_name = self.image_name_extractor(
            probe_image_path)  # clears the full path and stores just the image name
        self.probe_folders_path = probe_folders_path  # "Probe"
        self.template_path = template_path  # "Real"
        self.probe_image = cv2.imread(probe_image_path)  # read probe image (it is an array)
        self.match_dict = {}  # it will keep print_description and match_score
        self.genuine_score = []  # Genuine score list
        self.imposter_score = []  # Imposter score list
        self.threshold = threshold  # threshold value

    def compute_match_dictionary(self) -> None:
        """
        objective: computing the match score with every image in the template database
        input:
        output: a dictionary with the filename and corresponding match scores
        """
        template_image_descriptions = os.listdir(self.template_path)
        for image_description in template_image_descriptions:
            path = os.path.join(self.template_path, image_description)
            real_image = cv2.imread(path)
            M = Matcher(real_image, self.probe_image)
            match_score = M.get_sift_flann_match_score()
            print_description = image_description
            extracted_probe_image = self.image_name_extractor(self.probe_image_path)
            self.match_dict[(print_description, extracted_probe_image)] = match_score

    def image_name_extractor(self, probe_image_name) -> str:
        """
        :param probe_image_name: this parameter is fullpath of the probe_image
        :return: function returns just the image name, so it extracts the full path
        """
        base_name = os.path.basename(probe_image_name)
        name_list = base_name.split("_")
        name_list.pop(0)
        last_element_list = name_list[len(name_list) - 1].split(".")
        last_element_list.pop(0)
        name_list.pop(len(name_list) - 1)
        result = "_".join(name_list)
        result += "." + last_element_list[0]
        return result

    def get_prediction(self) -> str:
        """
        objective: to return whether a correct or incorrect match
        process: get the description of the file with the highest match score
        if the description matched with that of the probe file then its a correct match
        input: a dictionary computed via compute_match_dictionary
        output: a dictionary with the filename and corresponding match scores
        """
        self.compute_match_dictionary()
        # sort the dictionary and get the best matching image
        sorted_match_dict = sorted(self.match_dict.items(), key=lambda x: x[1])
        if self.is_equal(sorted_match_dict[-1][0][0], self.probe_image_name):
            return "correct"
        else:
            return "incorrect"

    def is_equal(self, real_img, probe_img) -> bool:
        """
        objective: Helper function to check if the image names are the same
        process: splits the names by underscore and if the ID, gender, hand, and fingers the same then
        it is the same person
        input: template image and probe image
        :param real_img: real image description (name)
        :param probe_img: probe image description (name)
        :return: boolean
        """
        real_img_info_list = real_img.split("_")
        probe_img_info_list = probe_img.split("_")
        real_img_ID = real_img_info_list[0]
        real_img_gender = real_img_info_list[2]
        real_img_hand = real_img_info_list[3]
        real_img_finger = real_img_info_list[4]
        probe_img_ID = probe_img_info_list[1]
        probe_img_gender = probe_img_info_list[3]
        probe_img_hand = probe_img_info_list[4]
        probe_img_finger = probe_img_info_list[5]
        if real_img_ID == probe_img_ID and real_img_gender == probe_img_gender and real_img_hand == probe_img_hand and real_img_finger == probe_img_finger:
            return True
        else:
            return False

    def compute_genuine_and_imposter_scores(self) -> None:  # Look at this func and decide whether you want to add threshold into part
        """
        objective: Decides an attempt is either genuine or imposter
        process: uses is_equal function to check if the images are equal and then if it is appends
        it to the self.genuine_score list, otherwise appends it to self.imposter_score
        input: None
        output: changes the self.genuine_score and self.imposter_score lists
        """
        sorted_match_dict = sorted(self.match_dict.items(), key=lambda x: x[1])
        for desc, score in sorted_match_dict:
            score = score / 100
            if self.is_equal(desc[0], self.probe_image_path):
                if score > self.threshold:  # it means genuine this line increased the security of the Identification system
                    self.genuine_score.append(score)
                else:  # this means impostor
                    self.imposter_score.append(score)
            else:  # this means impostor
                self.imposter_score.append(score)
