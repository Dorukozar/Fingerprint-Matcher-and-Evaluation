import os
from aiohttp import Fingerprint
import cv2
from matplotlib import pyplot as plt
from Matcher import *
from random import *
from Authentication import *
from Identification import *
from sklearn import metrics
from Plotter import *


class PerformanceEvaluation:
    def __init__(self, data_path, probe_path, template_path):
        self.data_path = os.path.join(os.getcwd(), data_path)
        self.probe_path = probe_path
        self.template_path = template_path
        self.all_genuine_scores = []
        self.all_imposter_scores = []
        self.plt = Plotter()
        self.identification_objects = []

    def automated_authentication(self, num_of_probe_img=500) -> None:
        """
        :param num_of_probe_img: number of probe images that the user wants to run through
        MAX: max number of images that can be run through is 1629

        objective: runs through all the altered images and try to match them to the database that is created
        process: Creates an authentication object and runs through the probe folders to match those images
        with the images that are in the database
        input: dataset path
        output: gen and imp scores
        """
        break_point = 0
        probe_folder_path = os.path.join(self.data_path, self.probe_path)
        probe_folder_names = os.listdir(probe_folder_path)
        if '.DS_Store' in probe_folder_names:
            probe_folder_names.remove('.DS_Store')
        boolean = True
        while boolean:
            for name in probe_folder_names:
                probe_folder_img_path = os.path.join(self.data_path, self.probe_path, name)
                probe_img_list = os.listdir(probe_folder_img_path)
                for image in probe_img_list:
                    A = Authentication(image, "Dataset", "Probe")
                    A.create_random_authentication_database()
                    A.create_match_dict()
                    A.get_prediction()
                    break_point += 1
                    self.all_imposter_scores.extend(A.impostor_scores)
                    self.all_genuine_scores.extend(A.genuine_scores)

                    if break_point == num_of_probe_img:  # 500 img
                        if len(self.all_genuine_scores) == 0:
                            print("Running automated_authentication again because number of genuine scores is 0")
                            break_point = 0
                        if break_point == num_of_probe_img:
                            print(self.all_genuine_scores)
                            print(self.all_imposter_scores)
                            return

    def automated_identification(self, num_of_folders=1, num_of_probe_img=25) -> None:
        """
        :param num_of_folders: between 1-3 this is the folders that you want to run through either
        1, 2 or 3 (Altered-Easy, Altered-Hard, Altered-Medium)
        :param num_of_probe_img: number of probe images that the user wants to run through

        objective: Runs through all the altered images and try to match those altered images with the
        images that are in the folder and try to identify the people
        process:
        input: None
        output: Changes the lists self.all_genuine_scores and self.all_imposter_scores
        """
        real_folder_path = os.path.join(self.data_path, self.template_path)
        probe_folder_path = os.path.join(self.data_path, self.probe_path)
        probe_folders = os.listdir(probe_folder_path)
        if '.DS_Store' in probe_folders:
            probe_folders.remove('.DS_Store')

        for probe_folder in probe_folders[:num_of_folders]:  # every
            images_path = os.path.join(probe_folder_path, probe_folder)
            images = os.listdir(images_path)
            for image in images[:num_of_probe_img]:  # 25
                probe_image_full_path = os.path.join(probe_folder_path, probe_folder, image)
                # following identification method will do ....
                id_object = Identification(probe_image_full_path, probe_folder_path, real_folder_path)
                # id_object.get_prediction()  # interactive visualization
                id_object.compute_match_dictionary()
                id_object.compute_genuine_and_imposter_scores()
                self.all_genuine_scores.extend(id_object.genuine_score)
                self.all_imposter_scores.extend(id_object.imposter_score)
                self.identification_objects.append(id_object)

        print(f"all_genuine_scores {self.all_genuine_scores}")
        print(f"all_imposter_scores {self.all_imposter_scores}")

    def rank_accuracy(self, k=1) -> None:
        labels = []
        scores = []
        for id_object in self.identification_objects:
            labels.append(id_object.probe_image_name)
            scores.append(list(id_object.match_dict.values()))

        #
        print('len(labels):', len(labels))
        #
        print('len(scores):', len(scores))

        number = metrics.top_k_accuracy_score(labels, scores, k=k, normalize=False)
        fraction = metrics.top_k_accuracy_score(labels, scores, k=k)
        print(f"number: {number}, fraction: {fraction}")

    def plot_roc_curve(self, biometric_function) -> None:
        print("ROC")
        self.plt.plot_roc(self.all_genuine_scores, self.all_imposter_scores, biometric_function)

    def plot_det_curve(self, biometric_function) -> None:
        print("DET")
        self.plt.plot_det(self.all_genuine_scores, self.all_imposter_scores, biometric_function)


# Plotting problem is that when you run for 50 img in identification it adds a bit of slope
# but when running for 5 images there is no slope. ASK WHY????
if __name__ == '__main__':
    # p = PerformanceEvaluation("Dataset", "Probe", "Real")
    # print("Running authentication")
    # p.automated_authentication(num_of_probe_img=500)
    # p.plot_roc_curve("Authentication")
    # p.plot_det_curve("Authentication")
    # # print(p.all_genuine_scores)
    # # print(p.all_imposter_scores)

    obj = PerformanceEvaluation("Dataset", "Probe", "Real")
    print("Running Identification")
    obj.automated_identification(num_of_probe_img=10)
    obj.plot_roc_curve("Identification")
    obj.plot_det_curve("Identification")
    # obj.rank_accuracy(1)
    # obj.rank_accuracy(2)
    # obj.rank_accuracy(3)
