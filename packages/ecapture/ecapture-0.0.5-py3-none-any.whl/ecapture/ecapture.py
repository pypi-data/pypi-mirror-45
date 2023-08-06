from cv2 import *
def capture(camera_index,name_of_window,save_name):
    cam = VideoCapture(camera_index)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors
        if name_of_window != False:
            namedWindow("cam-test")
            imshow("cam-test",img)
            waitKey(0)
            destroyWindow("cam-test")
        if save_name != False:
            imwrite(save_name,img) #save image
    
    
    
