import numpy as np
from matplotlib import pyplot as plt


class Plotter:

    def __init__(self):
        self.thresholds = np.linspace(0, 1, 11)
        self.TAR = []  # True Acceptance rate ROC
        self.FAR = []  # False Acceptance rate ROC
        self.FRR = []  # False rejection rate DET

    def plot_roc(self, gen_scores, imp_scores, biometric_function, roc_line_width=2):
        """
        ROC: Receiver Operating Curve
        :param gen_scores: genuine scores list
        :param imp_scores: imposter scores list
        :param biometric_function: Identification or Authentication
        :param roc_line_width: ROC curve's line width (default = 4)
        :return: None
        """
        self.compute_TAR(gen_scores)

        self.compute_FAR(imp_scores)

        # These couple of lines sets the x-axis and y-axis  labels, plots what we need to plot and shows it.
        # It also sets the title of the graph and the limits of the graph and returns the plot
        plt.plot(self.FAR, self.TAR, '--o', linewidth=roc_line_width)
        plt.title(f"{biometric_function} ROC Curve")
        plt.ylabel("True Acceptance Rate")
        plt.xlabel("False Acceptance Rate")
        plt.legend(["ROC"], loc="lower right")
        plt.xlim([-0.1, 1.1])
        plt.ylim([-0.1, 1.1])
        plt.grid(True)
        plt.show()
        self.FAR.clear()

    def plot_det(self, gen_scores, imp_scores, biometric_function, det_line_width=2, eer_color="red",
                 eer_marker_type="o", eer_marker_size=10):
        """
        DET: Decision Error Tradeoff
        :param gen_scores: genuine scores list
        :param imp_scores: imposter scores list
        :param biometric_function: Identification or Authentication
        :param eer_color: EER point's color
        :param eer_marker_type: EER point's marker type
        :param eer_marker_size: eer point's marker size (how big the point is)
        :param det_line_width: DET curve's line width (default = 4)
        :return: None
        """

        self.compute_FRR(gen_scores)

        self.compute_FAR(imp_scores)

        eer, eer_percentage = self.compute_EER()

        # plot DET curves
        plt.plot(self.FAR, self.FRR, '--o', color="green", linewidth=det_line_width)
        plt.plot([0, 1], [0, 1], "--b")
        plt.plot([eer], [eer], color=eer_color, marker=eer_marker_type, markersize=eer_marker_size)

        # for i, j in zip(self.FAR, self.FRR):
        #     plt.text(i, j, '({}, {})'.format(i, j))

        # for i, j, k in zip(self.FAR, self.FRR, self.thresholds):
        #     # plt.annotate('(%s, %s, %s)' % (i, j, k), xy=(i, j, k), textcoords='offset points', xytext=(0, 10), ha='center')
        #     plt.annotate('(%s, %s, %s)' % (i, j, k), (i, j, k), textcoords='offset points', xytext=(0, 10),
        #                  ha='center')

        plt.title(f"{biometric_function} DET Curve")
        plt.ylabel("False Rejection Rate")
        plt.xlabel("False Acceptance Rate")
        plt.legend(["DET", "X=Y", f"EER = {eer_percentage} %"], loc="center right")
        plt.xlim([-0.1, 1.1])
        plt.ylim([-0.1, 1.1])
        plt.grid(True)
        plt.show()
        self.FAR.clear()

    def compute_EER(self):
        """
        computes EER
        :return: EER as float and eer_percentage as float but rounds it to the nearest 10th and multiplies by 100
        """
        FAR_numpy = np.array(self.FAR)
        FRR_numpy = np.array(self.FRR)
        eer_index_list = abs(FAR_numpy - FRR_numpy)
        eer_index = np.argmin(eer_index_list)
        eer = np.mean(np.array([FAR_numpy[eer_index], FRR_numpy[eer_index]]))
        print(f"Equal error rate: {eer}")
        eer = np.around(eer, 4)
        eer_percentage = eer * 100
        print(f"Eer_index -> {eer_index}, eer -> {eer}, eer percentage -> {eer_percentage} %")
        return eer, eer_percentage

    def compute_FAR(self, imp_scores):
        """
        In this for loop it goes through the thresholds and the imp_scores list that is passed in the parameter
        then checks if the imposter score is greater than or equal to threshold, then it increments the counter for imposter scores
        and at the end of the second for loop it sets the counter 0 so that it will correctly count for each threshold
        So these for loops are essential for fpr
        :param imp_scores: imposter scores
        :return: None but edits self.FAR
        """
        for j in self.thresholds:
            count_imposter = 0
            for val in imp_scores:
                if val >= j:
                    count_imposter += 1
            res = count_imposter / len(imp_scores)
            self.FAR.append(res)

    def compute_TAR(self, gen_scores):
        """
        In this for loop it goes through the thresholds and the gen_scores list that is passed in the parameter
        then checks if the genuine score is greater than or equal to threshold, then it increments the counter for
        genuine scores and at the end of the second for loop it sets the counter 0 so that it will correctly count
        for each threshold So these for loops are essential for tpr
        :param gen_scores: genuine scores
        :return: None but edits self.TAR
        """
        for i in self.thresholds:
            count_genuine = 0
            for value in gen_scores:
                if value >= i:
                    count_genuine += 1
            result = count_genuine / len(gen_scores)
            self.TAR.append(result)

    def compute_FRR(self, gen_scores):
        """
        In this for loop it goes through the thresholds and the gen_scores list that is passed in the parameter
        then checks if the genuine score is less than or equal to threshold, then it increments the counter for genuine scores
        and at the end of the second for loop it sets the counter 0 so that it will correctly count for each threshold
        So these for loops are essential for FRR
        :param gen_scores: genuine scores
        :return: None but edits self.TAR
        """
        for i in self.thresholds:
            count_genuine = 0
            for value in gen_scores:
                if value < i:
                    count_genuine += 1
            result = count_genuine / len(gen_scores)
            self.FRR.append(result)
