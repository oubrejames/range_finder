import cv2
import numpy as np

def ROI(im): 
    """GET ROI, CROP TO NEW IMAGE
    """
    # Select ROI
    r = cv2.selectROI(im, showCrosshair = False)

    # Crop image
    imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    cv2.waitKey(0)
    return imCrop


def get_color(cropped_im): 
    """TAKE OUT JUST FLAG FROM ITS COLOR
    """
    img_hsv = cv2.cvtColor(cropped_im , cv2.COLOR_BGR2HSV)
    low_white = np.array([0, 0, 69])
    high_white = np.array([255, 60, 255])
    mask = cv2.inRange(img_hsv, low_white, high_white)
    # Merge the mask and crop the red regions
    color_crop = cv2.bitwise_and(cropped_im , cropped_im , mask=mask)
    return color_crop

def get_edges(color_crop): 
    """GET EDGES, AND Y GRADIENT OF EDGES"""
    edges = cv2.Canny(color_crop, 100, 200)
    sobely = cv2.Sobel(edges,cv2.CV_64F,0,1,ksize=1)
    return sobely



def find_length(iyy): 
    """GET SIDE LENGTH OF FLAG IN PIXELS"""
    n_row = iyy.shape[0]
    n_col = iyy.shape[1]
    print("size = ", iyy.shape)
    esc = 1
    esc2 = 1
    for i in range(0, n_row):
        for j in range(0, n_col):
            if iyy[i, j] > 0:
                top_x = j
                top_y = i
                esc = 0
                break
        if esc == 0:
            break


    for i in reversed(range(0, n_row)):
        for j in reversed(range(0, n_col)):
            if iyy[i, j] > 0:
                print("oop")
                bot_x = j
                bot_y = i
                esc2 = 0
                break
        if esc2 == 0:
            break
    return top_y, top_x, bot_y, bot_x


def focal(known_d, known_l, b_y, t_y): 
    """Calculate the focal length"""
    print("Calculating focal length")
    P = b_y - t_y
    focalLength = (P * known_d) / known_l
    print(focalLength)

    return #focalLength


def dist_to_flag(focalLength, known_length, b_y, t_y): #Contributers: James Oubre
    P2 = b_y - t_y
    distance_to_flag = known_length * focalLength / P2
    return distance_to_flag

def display_result(image, distance): #Contributers: James Oubre
    cv2.putText(image, "%.2f yd" % (distance),
                (image.shape[1] - 300, image.shape[0] - 20), cv2.FONT_HERSHEY_DUPLEX ,
                2.0, (255, 255, 0), 3)
    cv2.imshow("ROI selector", image)

def main(): #Contributers: James Oubre
    # Read image
    """
    ######### ALL JUST TO GET INITIAL FOCAL LENGTH. ONCE OBTAINED, FOCAL LENGTH SAVED AND USED AS A CONSTANT###########
    ctrl_im = cv2.imread("2ftwhite.jpg")
    ctrl_im = cv2.resize(ctrl_im, (720, 960))  # Resize image

    ctrl_ROI = ROI(ctrl_im)
    cv2.imshow("ctrl_ROI", ctrl_ROI)

    ctrl_color_crop = get_color(ctrl_ROI)
    cv2.imshow("ctrl_color_crop", ctrl_color_crop)

    ctrl_sobel = get_edges(ctrl_color_crop)
    cv2.imshow("ctrl_sobel", ctrl_sobel)

    t_y, t_x, b_y, b_x = find_length(ctrl_sobel)
    cv2.rectangle(ctrl_ROI , (t_x, t_y), (b_x, b_y), (255, 69, 69), 2)
    cv2.imshow("rectangle1", ctrl_ROI)

    focal_l = focal(24, 14, b_y, t_y)
    """
    ################### MAIN ONCE FOCAL OBTAINED ###########################

    focal_l = 755 #CALCULATED FOCAL LENGTH

    ### TEST IMAGES BELOW ###
    #im = cv2.imread("IMG_2180.jpg")  #PICTURE FROM 5 yds away
    #im = cv2.imread("IMG_2189.jpg")  #PICTURE FROM 5 yds away
    #im = cv2.imread("IMG_2196.jpg")  #PICTURE FROM 6 yds away'
    #im = cv2.imread("IMG_2203.jpg")  #PICTURE FROM 7 yds away
    #im = cv2.imread("IMG_2188.jpg")  #PICTURE FROM 12 yds away
    #im = cv2.imread("IMG_2202.jpg")  #PICTURE FROM 14 yds away
    #im = cv2.imread("IMG_2199.jpg")  #PICTURE FROM 15 yd away
    im = cv2.imread("IMG_2195.jpg")   #PICTURE FROM 15 yd away
    #im = cv2.imread("IMG_2194.jpg")  #PICTURE FROM 27 yd away
    #im = cv2.imread("IMG_2187.jpg")  #PICTURE FROM 27 yds away
    #im = cv2.imread("IMG_2198.jpg")  #PICTURE FROM 35 yd away
    #im = cv2.imread("IMG_2193.jpg")  #PICTURE FROM 44 yd away
    #im = cv2.imread("IMG_2177.jpg")  #PICTURE FROM 61 yds away
    #im = cv2.imread("IMG_2183.jpg")  #PICTURE FROM 77 yds away
    #im = cv2.imread("IMG_2201.jpg")  #PICTURE FROM 83 yds away
    #im = cv2.imread("IMG_2191.jpg")  #PICTURE FROM 109 yds away
    #im = cv2.imread("IMG_2197.jpg")  #PICTURE FROM 113 yds away
    #im = cv2.imread("IMG_2186.jpg")  #PICTURE FROM 132 yds away

    im = cv2.resize(im, (720, 960))  # Resize image to iPhone size
    new_ROI = ROI(im) #select flag ROI


    color_crop = get_color(new_ROI) #Crop out just the flag

    sobel = get_edges(color_crop) #Get contours of flag

    t2_y, t2_x, b2_y, b2_x = find_length(sobel) #Find the top and bottom pixels to obtain flag pixel length

    distance_to_flag = dist_to_flag(focal_l, 14, b2_y, t2_y) #Calculate distance to the flag

    #Convert distance from inches to yards.
    actual_distance = distance_to_flag/36

    # noticed that the output was off by a linearly increasing amount as the distance grew.
    # The calculation below accounts for the error and improves results (linear regression)
    actual_distance_yds = actual_distance + actual_distance*0.15+0.6175

    #Show the rectangle of the top and bottom pixels
    cv2.rectangle(new_ROI, (t2_x, t2_y), (b2_x, b2_y), (255, 69, 69), 1)
    cv2.circle(new_ROI, (t2_x, t2_y), 2,(69, 200, 69))
    cv2.circle(new_ROI, (b2_x, b2_y), 2, (69, 200, 69))

    #Display results
    print(round(actual_distance_yds, 2), 'yds')  #print distance in terminal
    display_result(im, actual_distance_yds) #display results on original image
    cv2.waitKey(0)

if __name__ == '__main__' :
    main()
