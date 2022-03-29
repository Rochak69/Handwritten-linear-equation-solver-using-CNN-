import cv2 
import numpy as np 



class getIMAGEPOSITION():
    
    def __init__(self,image_path):

        self.path = image_path
        self.image = cv2.imread(self.path)
        self.chars_bb = []
        self.chars_bb_new = []
        self.chars_bb_new2 = []
        self.bounding_box = []

 # overlapping bb bata eauta matra dinxa        
    def get_unique(self):
        unique_list=[]
        for y in self.chars_bb_new2:
            if y not in unique_list:
                unique_list.append(y)
        return unique_list 
            
    def get_bounding_box(self):
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3,3), 0)
        edged = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 11, 4)
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            cnt = cnt.reshape((cnt.shape[0],cnt.shape[2]))
            left_tc = np.amin(cnt, axis=0)
            right_bc = np.amax(cnt, axis=0)
            min_x = left_tc[0]
            max_x = right_bc[0]
            min_y = left_tc[1]
            max_y = right_bc[1]
            self.chars_bb.append([min_x,min_y,max_x,max_y])

        #################################################
        self.chars_bb_new = self.chars_bb.copy()
        for i in range(len(self.chars_bb)-1):
            cnt_i = self.chars_bb[i]
            i=0
            for j in range(i+1,len(self.chars_bb)):
                cnt_j = self.chars_bb[j]
                cent_i = cnt_i[0]+(cnt_i[2] - cnt_i[0])/2
                cent_j = cnt_j[0]+(cnt_j[2] - cnt_j[0])/2
                if cnt_j == cnt_i:
                    pass
                elif abs(cent_i - cent_j) <= 20:
                    min_x = min(cnt_j[0],cnt_i[0])
                    min_y = min(cnt_j[1],cnt_i[1])
                    max_x = max(cnt_j[2],cnt_i[2])
                    max_y = max(cnt_j[3],cnt_i[3])
                    vals_new = [min_x,min_y,max_x,max_y]
                    self.chars_bb_new.append(vals_new)
                    if i == 0:
                        self.chars_bb_new.remove(cnt_i)
                        i=i+1

        ################################################
        self.chars_bb_new2 = self.chars_bb_new.copy()
        for i in range(len(self.chars_bb_new)-1):
            cnt_i = self.chars_bb_new[i]
            for j in range(i+1,len(self.chars_bb_new)):
                cnt_j = self.chars_bb_new[j]
                cent_i = cnt_i[0]+(cnt_i[2] - cnt_i[0])/2
                cent_j = cnt_j[0]+(cnt_j[2] - cnt_j[0])/2
                area_i = (cnt_i[2] - cnt_i[0])*(cnt_i[3] - cnt_i[1])
                area_j = (cnt_j[2] - cnt_j[0])*(cnt_j[3] - cnt_j[1])
                if cnt_j == cnt_i:
                    pass
                elif (abs(cent_i - cent_j) <= 20):
                    if area_i > area_j:
                        if cnt_j in self.chars_bb_new2:
                            self.chars_bb_new2.remove(cnt_j)
                    elif area_i < area_j:
                        if cnt_i in self.chars_bb_new2:
                            self.chars_bb_new2.remove(cnt_i)
                            
                                            
        self.bounding_box = self.get_unique()        
        self.bounding_box.sort()
        return self.bounding_box 


if __name__ == "__main__":
    path = 'level3.jpg'
    bb_ext = getIMAGEPOSITION(path)
    bb = bb_ext.get_bounding_box()
    symbols = bb_ext.get_position()
    print(symbols)