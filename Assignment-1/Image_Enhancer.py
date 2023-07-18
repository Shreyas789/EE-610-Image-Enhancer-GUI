import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as font
import cv2
import warnings
from functools import partial
warnings.filterwarnings('ignore')
from tkinter import filedialog

"""
Global Variables in the code:
image: current image or the variation which is displayed
image_array: stack of images and variations created after browsing
action_array: stack of strings having names of operations till now
"""

def select_img():     
    """
    Function to get an image from PC
    """
    global image, image_array, action_array
    path = filedialog.askopenfilename(title='open', filetypes = (("PNG Files", "*.png*"), ("JPG Files", "*.jpg*")))
    #gets the path of the file from pc
    if path != ():
        image = cv2.imread(path) #image is a numpy ndarray now
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert to RGB
        PIL_image = Image.fromarray(image.astype('uint8'), 'RGB') #converted to PIL
        Tk_image = ImageTk.PhotoImage(PIL_image) #converted to ImageTk for compatibility with GUI framework
        panel.configure(image = Tk_image, bd = 10) #place image in the panel
        panel.image = Tk_image #place image in the panel
        action_array = ["Browse"] #save info of last action in stack for display
        last["text"] = "Browse" #will be displayed
        image_array = [] #stack for storing images and variations
        image_array.append(image) #store image in stack


def undo(): 
    global image ,image_array, action_array
    if len(image_array) > 1: #execute only if some action has been done
        image_array.pop() #returns (pops) last element of the stack
        image = image_array[-1] #new last element after popping
        action_array.pop() #pops last element of action stack
        last['text'] = action_array[-1] #new last action
        PIL_image = Image.fromarray(image.astype('uint8'), 'RGB') #converted to PIL
        Tk_image = ImageTk.PhotoImage(PIL_image) #converted to ImageTk
        panel.configure(image = Tk_image)  #configure previous (now current) image
        panel.image = Tk_image        #image placed on the panel 

def undo_all():
    global image ,image_array, action_array
    if len(image_array) > 1:  #execute only if some action has been done
        image = image_array[0] #original image
        image_array = [image] #singleton list of original image
        action_array = [action_array[0]] #singleton list of 'Browse' action 
        last['text'] = action_array[0] #display 'Browse'
        PIL_image = Image.fromarray(image.astype('uint8'), 'RGB') #converted to PIL
        Tk_image = ImageTk.PhotoImage(PIL_image) #converted to ImageTk
        panel.configure(image = Tk_image) #configure original image
        panel.image = Tk_image #original image placed on panel


def enter_gamma():
    """
    Function when called opens a new window asking the user 
    to input the gamma value for Gamma Correction.
    Calls the function gamma_correct for actual execution
    """
    frame = tk.Tk()  #new tkinter window
    frame.title("Enter Gamma Value") #title of the frame
    frame.geometry('300x80') #dimensions
    global gamma_entry #variable to hold the input gamma value
    gamma_entry = tk.Text(frame, width = 10, height = 2, relief = 'solid', font = ('Comic Sans', 20)) #area for the user to type
    gamma_entry.place(relx = 0, rely = 0)   #positioning relative to borders
    enter_btn=tk.Button(frame, text = 'Apply', command = partial(gamma_correct, frame),
                        height = 1, font = ('Arial', 12, "bold"), relief = 'raised')  #button which user will press after typing    
    enter_btn.place(relx = 0.65, rely = 0.6) #positioning relative to borders
    frame.mainloop() # Window loops and waits for events

def gamma_correct(frame, c = 1):
    """
    Function to execute gamma correction using the value input by user in enter_gamma
    """
    global image, image_array, action_array 
    gamma = float(gamma_entry.get(1.0, "end-1c")) #get the gamma value from the previous function user input
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #convert to HSV
    value = hsv[:,:,2] #grab the V channel
    corrected = c*((value/255)**gamma) #formula for gamma correction
    hsv[:,:,2] = corrected*255 #scale it to [0,255]
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB) #convert back to RGB for display
    rgb_PIL = Image.fromarray(image.astype('uint8'), 'RGB') #convert to PIL
    rgb_PIL = ImageTk.PhotoImage(rgb_PIL) #convert to PhotoImage for compatibility
    panel.configure(image = rgb_PIL) #configure new image
    panel.image = rgb_PIL #place image in panel
    image_array.append(image) #store new image onto stack
    last["text"] = "G.C: Gamma = " + str(gamma) #display operation name
    action_array.append("G.C: Gamma = " + str(gamma)) #store action info onto stack
    frame.destroy() #close the new frame


def log_xform():
    """
    Function to carry out Logarithmic Transformation on the Image
    """
    global image, image_array, action_array
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #convert to HSV
    value = hsv[:,:,2] #grab V channel
    corrected = np.log10(1 + value/255)/np.log10(2) #formula for Log transform
    hsv[:,:,2] = corrected*255 #scaling to [0,255]
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB) #convert back to RGB for display
    rgb_PIL = Image.fromarray(image.astype('uint8'), 'RGB') #convert to PIL
    rgb_PIL = ImageTk.PhotoImage(rgb_PIL) #convert to PhotoImage
    panel.configure(image = rgb_PIL) #configure new image
    panel.image = rgb_PIL #show image on panel
    image_array.append(image)  #store new image onto stack
    last["text"] = "Log transform" #display operation name
    action_array.append("Log transform") #store action info onto stack


## Extra Operation Implemented

def threshold_img(frame4):
    """
    Function to implement binary thresholding of the image, with cutoff input by user
    """
    global image, image_array, action_array  
    cutoff = float(cutoff_entry.get(1.0, "end-1c")) #get the cutoff value from user input
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #convert to HSV
    value = hsv[:,:,2] #grab the value channel
    value_1d = value.reshape(-1) #flatten the array to 1D
    value_th = np.array(list(map(lambda r: int(r>=cutoff), value_1d))) #apply binary threshold to each element of array
    hsv[:,:,2] = (value_th*255).reshape(value.shape) #convert back to 2D
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB) #convert back to RGB
    rgb_PIL = Image.fromarray(image.astype('uint8'), 'RGB') #convert to PIL
    rgb_PIL = ImageTk.PhotoImage(rgb_PIL) #convert to PhotoImage
    panel.configure(image = rgb_PIL) #configure thresholded image
    panel.image = rgb_PIL #place image on panel
    image_array.append(image) #place image on stack
    last["text"] = "Thresholding" #display the action
    action_array.append("Thresholding") #store the action
    frame4.destroy() #close the extra window
    
def enter_cutoff():
    """
    Function when called opens a new window asking the user 
    to input the cutoff value for Thresholding.
    Calls the function threshold for actual execution
    """
    frame4 = tk.Tk()  #new tkinter window
    frame4.title("Enter Cutoff Value") #title of the frame
    frame4.geometry('300x80') #dimensions
    global cutoff_entry #variable to hold the input cutoffgamma value
    cutoff_entry = tk.Text(frame4, width = 10, height = 2, relief = 'solid', font = ('Comic Sans', 20)) #area for the user to type
    cutoff_entry.place(relx = 0, rely = 0)   #positioning relative to borders
    enter_btn=tk.Button(frame4, text = 'Apply', command = partial(threshold_img, frame4),
                        height = 1, font = ('Arial', 12, "bold"), relief = 'raised')  #button which user will press after typing    
    enter_btn.place(relx = 0.65, rely = 0.6) #positioning relative to borders
    frame4.mainloop()  # Window loops and waits for events


#https://stackoverflow.com/questions/57033158/how-to-save-images-with-the-save-button-on-the-tkinter-in-python
def save_as():
    """
    Function to save the modified image in any location in the device
    """
    global image
    path = filedialog.asksaveasfile(defaultextension=".png") #gets the path to location
    if path is None:  #if not chosen any path
        return
    PIL_image = Image.fromarray(image.astype('uint8'), 'RGB') #convert to PIL image
    PIL_image.save(path.name) #save the image


def eq_hist():
    """
    Function which carries out histogram equalization
    """
    global image ,image_array, action_array 
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #convert to HSV
    value = hsv[:,:,2] #grab V channel
    value_list = value.reshape(-1) #flatten to 1D
    pdf = np.histogram(value_list, bins = 256)[0]/len(value_list) #get the pdf of the pixel values
    equalized = []  #list to store values of s for each r in [0,255]
    for i in range(0,256):  #values which 'r' takes (original pixel values)
        s = 255*sum(pdf[0:i])   #formula for histogram equalization. s: new pixel values
        equalized.append(s)   #store this value in the list
    equalized = np.array(equalized) #convert to a numoy array for applying function
    value_list_eq = np.array(list(map(lambda r: int(equalized[r]),value_list.astype('uint8')))) #will hold s value for each pixel
    value_eq = value_list_eq.reshape(value.shape) #convert back to 2d
    hsv[:,:,2] = value_eq #replace values in V channel
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB) #convert back to RGB for display
    rgb_PIL = Image.fromarray(image.astype('uint8'), 'RGB') #convert to PIL
    rgb_PIL = ImageTk.PhotoImage(rgb_PIL) #convert to PhotoImage
    panel.configure(image = rgb_PIL) #configure new image
    panel.image = rgb_PIL #place on the panel
    image_array.append(image) #store onto the stack
    last["text"] = "Histogram Eql" #Display action
    action_array.append("Histogram Eql") #store action onto stack
    
def blur_img(frame2):
    """
    Function for applying blurring through box filter of size input by user
    """
    global image, image_array, action_array
    ksize = int(ksize_entry.get(1.0, "end-1c"))  #get ksize value from user input from other function
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #convert to HSV
    value = hsv[:,:,2] #grab V
    if ksize%2 == 0: #if by mistake user puts even number, convert it to odd
        ksize = ksize - 1
    pw = int((ksize-1)/2) #padding width 
    value = np.pad(value, pw, mode = 'constant')  #zero padding of width pw
    value_blur = value.copy() #same sized array
    kernel = np.array([[1]*ksize]*ksize)/(ksize**2)  #box kernel of size ksize
    for x in range(pw,len(value)-pw):  #convolving the kernel with the image
        for y in range(pw,len(value[0])-pw):
            value_blur[x][y] = sum((value[x-pw:x+pw+1,y-pw:y+pw+1]*kernel).reshape(-1)) #element wise multiplication
    hsv[:,:,2] = value_blur[pw:-pw, pw:-pw]
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB) #convert back to RGB for display
    rgb_PIL = Image.fromarray(image.astype('uint8'), 'RGB') #convert to PIL
    rgb_PIL = ImageTk.PhotoImage(rgb_PIL) #convert to PhotoImage
    panel.configure(image = rgb_PIL) #configure new image
    panel.image = rgb_PIL #place on the panel
    image_array.append(image)  #store onto the stack
    last["text"] = "Blur: " + str(ksize) + "x" + str(ksize) #Display action
    action_array.append("Blur: " + str(ksize) + "x" + str(ksize)) #store action onto stack
    frame2.destroy() #close extra window
            

def enter_blur_value():
    """
    Creates a window and takes user input for the kernel size to control the extent of blurring
    """
    frame2 = tk.Tk() #new window
    frame2.title("Enter Kernel Size") #title
    frame2.geometry('300x80') #dimensions
    global ksize_entry  #variable to hold input ksize
    ksize_entry = tk.Text(frame2, width = 10, height = 2, relief = 'solid', font = ('Comic Sans', 20)) #place to write input, for user
    ksize_entry.place(relx = 0, rely = 0) #positioning relative to borders
    blur_btn = tk.Button(frame2, text = 'Apply', command = partial(blur_img,frame2),
                        height = 1, font = ('Arial', 12, "bold"), relief = 'raised') #user will press this button after typing
    blur_btn.place(relx = 0.65, rely = 0.6) #positioning relative to borders
    frame2.mainloop() # Window loops and waits for events

    
    
def sharpen_img(frame3):
    """
    Function for unsharp masking with user inpout c
    """
    #similar code to blur_img with some variations
    global image, image_array, action_array
    c = float(c_entry.get(1.0, "end-1c"))  #get c value from user input from other function
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #convert to hsv
    value = hsv[:,:,2] #grab V
    pw = 4 #we are using only 9x9 filter now
    value_pad = np.pad(value, pw, mode = 'constant')  #zero padding of width pw
    value_blur = value_pad.copy() #same shaped array
    kernel = np.array([[1]*9]*9)/81 #box filter of size 9
    for x in range(pw,len(value_pad)-pw):  #convolution
        for y in range(pw,len(value_pad[0])-pw):
            value_blur[x][y] = sum((value_pad[x-pw:x+pw+1,y-pw:y+pw+1]*kernel).reshape(-1)) #new values computed
    mask = value - value_blur[pw:-pw, pw:-pw]   #creating the mask by subtracting blurred from original
    hsv[:,:,2] = (value + c * mask)  #adding mask to original with weight c
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)  #convert to hsv
    rgb_PIL = Image.fromarray(image.astype('uint8'), 'RGB') #convert to PIL
    rgb_PIL = ImageTk.PhotoImage(rgb_PIL) #convert to PhotoImage 
    panel.configure(image = rgb_PIL) #configure new image
    panel.image = rgb_PIL #place new image on panel
    image_array.append(image) #store image onto stack
    last["text"] = "Sharpen: c = " + str(c)  #display action
    action_array.append("Sharpen: c = " + str(c)) #store action onto stack 
    frame3.destroy() #close extra window 
    

def enter_sharpen_value():
    """
    Creates a window and takes user input for the mask weight c 
    to control the extent of sharpening in Unsharp Masking
    """
    frame3 = tk.Tk() #new window
    frame3.title("Enter c value") #title
    frame3.geometry('300x80') #dimensions
    global c_entry #variable to hold input c
    c_entry = tk.Text(frame3, width = 10, height = 2, relief = 'solid', font = ('Comic Sans', 20))
    c_entry.place(relx = 0, rely = 0) #positioning relative to borders
    blur_btn = tk.Button(frame3, text = 'Apply', command = partial(sharpen_img,frame3),
                        height = 1, font = ('Arial', 12, "bold"), relief = 'raised')
    blur_btn.place(relx = 0.65, rely = 0.6) #positioning relative to borders
    frame3.mainloop() # Window loops and waits for events


# https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
# https://stackoverflow.com/questions/10133856/how-to-add-an-image-in-tkinter

h = 1000
w = 1000

root = tk.Tk()  #Main GUI Window
root.title('Image Enhancer') #its title
root.geometry("{}x{}".format(w,h))  #its dimensions

panel = tk.Label(root, background = 'white', relief = 'raised') #panel to display the image. Parent: root
panel.pack(side = 'right', anchor = tk.NW) #anchored to top right

my_font = font.Font(family='Helvetica', size=18, weight='bold')
buttonFrame = tk.Frame(root, width = 100) #creating a frame to hold all the buttons in one place. Parent: root
buttonFrame.pack(side = 'left', anchor = tk.NE) #achored to top left corner

#defining buttons for every operation with commands having respective function calls. Parent: buttonFrame
#when button is pressed the function under command will be called
browseB = tk.Button(buttonFrame, text = "Browse", command = select_img, 
                    height = 2, width = 20, font = my_font, bg = 'cyan')
saveB = tk.Button(buttonFrame, text = "Save As", command = save_as, 
                  height = 2, width = 20, font = my_font, bg = 'cyan')
undoB = tk.Button(buttonFrame, text = "Undo", command = undo, 
                  height = 2, width = 20, font = my_font, bg = 'lightpink')
undo_allB = tk.Button(buttonFrame, text = "Undo All", command = undo_all, 
                      height = 2, width = 20, font = my_font, bg = 'lightpink')
eq_histB = tk.Button(buttonFrame, text = "Equalize Histogram", command = eq_hist, 
                     height = 2, width = 20, font = my_font, bg = 'lightgreen')
gamma_correctB = tk.Button(buttonFrame, text = "Gamma Correction", command = enter_gamma, 
                           height = 2, width = 20, font = my_font, bg = 'lightgreen')
log_xformB = tk.Button(buttonFrame, text = "Log Transform", command = log_xform, 
                       height = 2, width = 20, font = my_font, bg = 'lightgreen')
last_label = tk.Label(buttonFrame, text = "Last Action:", height = 2, width = 20, font = my_font, bg = 'yellow')
last = tk.Label(buttonFrame, text = "No Action", height = 2, width = 20, font = my_font,  bg = 'yellow', fg = 'red')
#label to display last action

blur = tk.Button(root, text = "Browse", command = select_img, 
                 height = 2, width = 20, font = my_font)
sharpen = tk.Button(root, text = "Browse", command = select_img, 
                    height = 2, width = 20, font = my_font)
blur_button = tk.Button(buttonFrame, text = "Blur", command = enter_blur_value, bg = 'orange' ,
                        height = 2, width = 20, font = my_font)
sharpen_button = tk.Button(buttonFrame, text = "Sharpen", command = enter_sharpen_value, bg = 'orange',
                           height = 2, width = 20, font = my_font)
threshold_button = tk.Button(buttonFrame, text = "Threshold", command = enter_cutoff, bg = 'orange',
                           height = 2, width = 20, font = my_font)

#Some additional instructions displayed through a label and text. Parent: buttonFrame
info_text = "Click the Browse button to select an image from your system, apply the necessary transformations and then save the image using the Save As button."
info = tk.Label(buttonFrame, text = info_text, font = ('Helvetica', 15), height = 15, padx = 5, wraplength = 200)
info.pack(side = 'bottom', fill = 'both') #at the bottom of buttonFrame

#placing all the buttons in the buttonFrame frame
browseB.pack()
saveB.pack()
undoB.pack()
undo_allB.pack()
eq_histB.pack()
gamma_correctB.pack()
log_xformB.pack()
blur_button.pack()
sharpen_button.pack()
threshold_button.pack()
last_label.pack()
last.pack()

root.mainloop() # Window loops and waits for events