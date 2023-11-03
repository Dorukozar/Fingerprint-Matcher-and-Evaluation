from Identification import *

print("Welcome")

# Altered-Medium_10__M_Left_little_finger_Zcut.BMP
# Altered-Medium_14__M_Right_index_finger_CR.BMP

while True:
    print("Please Select one of the choices below")
    print("Enter 1 for Identification")
    print("Enter 2 for Authentication")
    print("Enter 9 to Quit")
    choice = int(input("Please Enter Your Choice (1,2, or 9)\n"))
    if choice == 1:
        # print("ENROLL or UPDATE")
        print("Identification")
        choice2 = str(input("Please Provide an image sample that you want to compare\n"))
        obj1 = Identification(choice2)
        obj1.get_prediction()
        obj1.get_genuine_and_imposter_scores()
    # elif choice == 2:
    #     print("RECORD")
    #     obj2 = Record()
    #     obj2.record()
    # elif choice == 3:
    #     print("PLOT")
    #     obj3 = Plot()
    #     obj3.plot()

    elif choice == 9:
        exit()
        # break
    else:
        print("Incorrect input provided!!! Please try again\n")

