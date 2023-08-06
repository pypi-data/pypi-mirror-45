from cv2 import *
def capture(camera_index,name_of_window,save_name):
    cam = VideoCapture(camera_index)   # 0 -> index of camera
    if cam is None or not cam.isOpened():
       print('Warning: unable to open image source: ', camera_index)
    s, img = cam.read()
    if s:    # frame captured without any errors
        if name_of_window != False:
            namedWindow(name_of_window)
            imshow(name_of_window,img)
            waitKey(0)
            destroyWindow(name_of_window)
        if save_name != False:
            imwrite(save_name,img) #save image
    
    
    
