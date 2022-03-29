
from os import error
import numpy as np
import re
import cv2
import glob
from bb import getIMAGEPOSITION
from validate import Predict
import tensorflow as tf
import itertools


# import os
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
# physical_devices = tf.config.list_physical_devices("GPU")
# tf.config.experimental.set_memory_growth(physical_devices[0], True)

numeric = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
characters = ['X', 'Y', 'Z']
symbols = ['-', '+']
pc = Predict()


def get_equtaion_list(path_list):

    main_list = []
    for image_path in path_list:
        char_list = []
        final_crop = cv2.imread(image_path)
        bbgetter = getIMAGEPOSITION(image_path)
        bbs = bbgetter.get_bounding_box()

        for i, c in enumerate(bbs):
            (x, y, w, h) = (c[0], c[1], c[2], c[3])
            roi = final_crop[y:h, x:w]
            height, width = roi.shape[0], roi.shape[1]
            # print(height,width)
            if width > 15:
                ##################################################################
                if height > width:

                    blank_image = np.zeros((height, height, 3), np.uint8)
                    blank_image[:, 0:height] = (255, 255, 255)  # (B, G, R)
                    x_start = int(((height-width)/2))
                    blank_image[0:int(height), x_start:x_start + width] = roi
                else:

                    blank_image = np.zeros((width, width, 3), np.uint8)
                    blank_image[:, 0:width] = (255, 255, 255)  # (B, G, R)
                    x_start = int(((width-height)/2))
                    blank_image[x_start:x_start + height, 0:int(width)] = roi
                #################################################################

                kernel = np.ones((3, 3), np.uint8)
                dilation = cv2.erode(blank_image, kernel, iterations=1)
                blank_image = cv2.resize(dilation, (45, 45))
                blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)

                #################################################################
                result = pc.get_class(blank_image)
                char_list.append(str(result))
                ###########################################################
            else:
                char_list.append('.')
        main_list.append(char_list)

    return main_list


def convert_equation_list_to_string(main_list):

    equation_list = []
    for charset in main_list:
        equation = ''
        for i, char in enumerate(charset):

            if i == 0 and (char in characters) and (char not in symbols):
                equation = equation+'1'+str(char)

            elif i > 0 and (char in characters) and (char not in symbols) and (charset[i-1] not in numeric):
                equation = equation+'1'+str(char)
            elif char == "=":
                if charset[i+1] == "-":
                    equation = equation+str('+')

                else:
                    equation = equation+str('-')

            elif (charset[i] in symbols) and (charset[i-1] == '='):
                pass

            else:
                equation = equation+str(char)
        equation_list.append(equation)

    return equation_list



# def get_coeff(all_equations):
#     '''
#     Inputs all the equation list and find coefficient of 
#     each Varialbe. And doesnot depends on order of equation 
#     for example : 1x+1y-6 , -5y+2x+10
#     returns -> [[1,1,-6],[2,-5,10]]
#     '''
#     coeff_list = []

#     if len(all_equations) == 2:
#         def CoefficientIntercept(equation):
#             coef_x = re.findall('-?[0-9.]*[Xx]', equation)[0][:-1]
#             coef_y = re.findall('-?[0-9.]*[Yy]', equation)[0][:-1]
#             intercept = re.sub(
#                 "[+-]?\d+[XxYy]|[+-]?\d+\.\d+[XxYy]", "", equation)

#             return [float(coef_x), float(coef_y), float(intercept)]

#         for equation in all_equations:
#             coeff_list.append(CoefficientIntercept(equation))

#         return coeff_list

#     if len(all_equations) == 3:
#         def CoefficientIntercept(equation):
#             coef_x = re.findall('-?[0-9.]*[Xx]', equation)[0][:-1]
#             coef_y = re.findall('-?[0-9.]*[Yy]', equation)[0][:-1]
#             coef_z = re.findall('-?[0-9.]*[Zz]', equation)[0][:-1]
#             intercept = re.sub(
#                 "[+-]?\d+[XxYyZz]|[+-]?\d+\.\d+[XxYyZz]", "", equation)

#             return [float(coef_x), float(coef_y), float(coef_z), float(intercept)]

#         for equation in all_equations:
#             coeff_list.append(CoefficientIntercept(equation))

#         return coeff_list


def get_coeff(all_equations):
    '''
    Inputs all the equation list and find coefficient of 
    each Varialbe. And doesnot depends on order of equation 
    for example : 1x+1y-6 , -5y+2x+10
    returns -> [[1,1,-6],[2,-5,10]]
    '''
    coeff_list =  [] 
    
    if len(all_equations) == 2:
        for equation in all_equations:

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:
                coef_x = re.findall('-?[0-9.]*[Xx]', equation)[0][:-1]
            except:
                coef_x = 0.0
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:

                coef_y = re.findall('-?[0-9.]*[Yy]', equation)[0][:-1]
            except:
                coef_y = 0.0
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            intercept = re.sub("[+-]?\d+[XxYy]|[+-]?\d+\.\d+[XxYy]","", equation)    

            coeff_list.append([float(coef_x), float(coef_y), float(intercept)])

    
    if len(all_equations) == 3:
        for equation in all_equations:
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:
                coef_x = re.findall('-?[0-9.]*[Xx]', equation)[0][:-1]
            except:
                coef_x = 0.0
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:

                coef_y = re.findall('-?[0-9.]*[Yy]', equation)[0][:-1]
            except:
                coef_y = 0.0
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:
                coef_z = re.findall('-?[0-9.]*[Zz]', equation)[0][:-1]
            except:
                coef_z = 0.0
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            intercept = re.sub("[+-]?\d+[XxYyZz]|[+-]?\d+\.\d+[XxYyZz]","", equation)    

            coeff_list.append([float(coef_x), float(coef_y), float(coef_z), float(intercept)])


        
    return coeff_list


def solve(equation_list):

    equation_type = len(equation_list)

    if equation_type == 2:
        A = np.array([
            equation_list[0][:-1],
            equation_list[1][:-1] ]
        )
        B = np.array([
            equation_list[0][-1:],
            equation_list[1][-1:] ]
        )
    elif equation_type == 3:
        A = np.array([
            equation_list[0][:-1],
            equation_list[1][:-1],
            equation_list[2][:-1] ]
        )
        B = np.array([
            equation_list[0][-1:],
            equation_list[1][-1:],
            equation_list[2][-1:] ]
        )

    # x_ls = np.linalg.inv(A.transpose() * np.mat(A)) * A.transpose() * B
    x_ls = np.linalg.solve(A, B)
    return np.ndarray.tolist(x_ls)


def get_response():

    path_list = glob.glob('img/*.png')
    eq_list = get_equtaion_list(path_list)

    eq_str = convert_equation_list_to_string(eq_list)
    print(eq_str)
    coeff = get_coeff(eq_str)
    # print(coeff)
    # response = {}
    try:
        num_of_var = len(coeff)
        if num_of_var == 2:
            result = solve(coeff)
            # print(result)
            # convert 2D list to 1D
            result = list(itertools.chain(*result))
            X, Y = result[0], result[1]
            response = {
                "Success": True,
                'Soln_X': X*-1,
                "Soln_Y": Y*-1,
                "Eqn_1": eq_str[0] + '=0',
                "Eqn_2": eq_str[1] + '=0',

            }
            # print(f" X = {X} and Y = {Y}")

        elif num_of_var == 3:
            result = solve(coeff)
            # convert 2D list to 1D
            result = list(itertools.chain(*result))
            X, Y, Z = result[0], result[1], result[2]
            response = {
                "Success": True,
                'Soln_X': X*-1,
                "Soln_Y": Y*-1,
                "Soln_Z": Z*-1,
                "Eqn_1": eq_str[0] + '=0',
                "Eqn_2": eq_str[1] + '=0',
                "Eqn_3": eq_str[2] + '=0',

            }
            # print(f" X = {X} and Y = {Y} and Z = {Z}")

    except np.linalg.LinAlgError:
        response = {
            "Success": False,
            "Error": "THE LINES ARE PARALLEL"
        }
        print("THE LINES ARE PARALLEL")

    finally:
        return response
