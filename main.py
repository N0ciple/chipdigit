
from Tkinter import *

from time import time
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from random import randint
import os.path
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.resizable(width=False, height=False)
        self.root.geometry('{}x{}'.format(480, 272))


        self.Frame1 = Frame(self.root,borderwidth=2,relief=GROOVE)
        self.Frame1.pack(fill="both",side=LEFT)

        self.trainFrame = Frame(self.Frame1, borderwidth=2, relief=GROOVE)
        self.trainNum = Label(self.trainFrame)

        self.myLab = Label(self.Frame1, text="Recognition Mode")
        self.myLab.pack(padx=10, pady=10)

        self.bouton2 = Button(self.Frame1, text="reset", command=self.reset_canevas)
        self.bouton2.pack()

        self.bouton3 = Button(self.Frame1, text="Train", command=self.train_mode)
        self.bouton3.pack()

        self.bouton=Button(self.Frame1, text="Quit", command=self.close_window)
        self.bouton.pack()

        self.isEmpty = True
        self.isTrain = False
        self.number = 0
        self.counter=0

        self.l = LabelFrame(self.root, text="drawZone",labelanchor="n",cursor="tcross", padx=2, pady=2)
        self.Frame2 = Frame(self.l,borderwidth=2,width=360)
        self.Frame2.pack(fill="y")
        self.l.pack(fill="y",anchor="se")

        self.image1 = Image.new("RGB", (240, 240), white)
        self.draw = ImageDraw.Draw(self.image1)

        self.set_counter()
        self.c = Canvas(self.l, bg='white', width=240, height=240)
        self.c.pack()
        self.IsPainting = False
        self.setup()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 5
        self.color = 'black'
        self.active_button = True
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def close_window(self):
        self.root.destroy()

    def reset_canevas(self):
        self.c.delete("all")
        self.image1 = Image.new("RGB", (240, 240), white)
        self.draw = ImageDraw.Draw(self.image1)
        self.isEmpty = True


    def activate_button(self, some_button):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button



    def set_counter(self):
        if os.path.isfile('train/counter'):
            with open('train/counter', 'r') as myfile:
                data = myfile.read().replace('\n', '')
                self.counter = int(data)
        else :
            self.counter = 0




    def save_image(self):

        if not self.isEmpty and self.isTrain :
            f = open('train/counter','w')
            self.counter+=1
            f.write(str(self.counter))
            self.image1 = self.image1.filter(ImageFilter.GaussianBlur(2))
            self.image1 = self.autocrop(self.image1)
            self.image1 = self.image1.resize((imSize, imSize), Image.ANTIALIAS)
            self.image1.save('train/img'+str(self.counter)+"-"+str(self.number)+'.jpg')
            self.number = randint(0,9)
            self.trainNum.config(text="write:\n" + str(self.number))
        elif not self.isEmpty :
            self.image1 = self.image1.filter(ImageFilter.GaussianBlur(2))
            self.image1 = self.autocrop(self.image1)
            self.image1 = self.image1.resize((imSize, imSize), Image.ANTIALIAS)
            self.image1.save('digit.jpg')


    def train_mode(self):
        self.isTrain = True
        self.trainFrame.pack()
        self.number = randint(0,9)
        self.l.config(text="Draw Zone")
        self.trainNum.config(text="write:\n"+str(self.number))
        self.trainNum.pack()
        self.bouton3.config(text="Recon")
        self.bouton3.config(command=self.recon_mode)
        self.myLab.config(text='Training\nMode')


    def recon_mode(self):
        self.trainNum.pack_forget()
        self.trainFrame.pack_forget()
        self.isTrain = False
        global classif
        classif = train_classif()
        self.myLab.config(text='Recognition\nMode')
        self.bouton3.config(text='Train')
        self.bouton3.config(command=self.train_mode)


    def autocrop(self,MyImg):
        image_data = np.asarray(MyImg)
        image_data_bw = image_data[:,:,1]
        non_empty_columns = np.where(image_data_bw.min(axis=0) < 255)[0]
        non_empty_rows = np.where(image_data_bw.min(axis=1) < 255)[0]
        cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

        image_data_new = image_data[cropBox[0]:cropBox[1] + 1, cropBox[2]:cropBox[3] + 1, :]

        img = Image.fromarray(image_data_new)

        return img

    def paint(self, event):
        self.isEmpty = False
        self.IsPainting = True
        self.line_width = 5
        paint_color = 'black'
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.draw.line(  (self.old_x, self.old_y, event.x, event.y,), (0,0,0) ,25 )


        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None
        self.IsPainting = False


def train_classif():
    with open('train/counter', 'r') as myfile:
        data = myfile.read().replace('\n', '')
    counter = int(data)
    data_train = np.zeros((counter-2,imSize*imSize))
    data_target = np.zeros((counter-2,1))
    dirContent = os.popen('find train -type f -print').read()
    dirContent = dirContent[:-1].split('\n')



    for i in range(counter-1):
        line = dirContent[i]
        if '.jpg' in line :
            imgTempo = Image.open(dirContent[i])
            data_train[i-1,:] = np.array(imgTempo)[:,:,1].reshape(1,imSize*imSize)
            data_target[i-1,0] = int(line.split('.')[0][-1:])

    #clf = svm.SVC(gamma=0.001)
    clf = RandomForestClassifier(n_estimators=50)
    clf.fit(data_train, data_target.ravel())

    return clf


def predict_img(myClf):

    imag = Image.open('digit.jpg')
    imag2 = np.array(imag)[:,:,1].reshape(1,imSize*imSize)
    #img = Image.fromarray(imag2.reshape(32,32))
    pred = myClf.predict(imag2)
    ge.l.config(text='recognized : ' + str(int(pred[0])))




if __name__ == '__main__':
    imSize = 32
    white = (255,255,255)
    ge = Paint()
    isTicking = False
    try :
        classif = train_classif()
    except :
        ge.train_mode()
    while True :

        ge.root.update()

        if not ge.IsPainting  and not isTicking :
            t1 = time()
            isTicking = True

        if ge.IsPainting :
            isTicking = False

        if not ge.IsPainting and isTicking :
            if time() - t1 > 0.7 :
                ge.save_image()
                isTicking = False
                if not ge.isTrain and not ge.isEmpty:
                    try:
                        predict_img(classif)
                    except :
                        ge.train_mode()
                ge.reset_canevas()

#####END OF FILE
