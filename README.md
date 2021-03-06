# ChipDigits
ChipDigits is a simple python script which performs handwriting recognition. There are two modes : 
* Recognition Mode
* Training Mode

## Modes

### Recognition Mode
In recognition mode you can simply draw a digit between 0 and 9 and the label at the top of the drawing zone will change to print which number have been recognized. This is visible on the illustration picture.

Here is a picture of the recognition mode :

![alt text](http://image.noelshack.com/fichiers/2017/11/1489593058-img2.png "Recognition Mode Picture")

### Training Mode
Since everybody writes in a different manner, you might want to train ChipDigit to your own writing style. To do so, you can access the Training Mode. In training mode, a small text box on the left of the screen is asking you to write a precise digit. Write it, and it's automatically stored. To prevent you from being bored and wrtiting the number exactly the same way, the number you have to write are chosen randomly.

Here is a picture of the training mode :

![alt text](http://image.noelshack.com/fichiers/2017/11/1489593058-img3.png "Training Mode Picture")

## Instructions

### How to install ChipDigit on PocketChip
To install ChipDigit you simply need to install a few dependencies :

```bash
sudo apt-get install python-tk git python-numpy
pip install --user scikit-learn
```

*Please be aware that installing scikit-learn on your PocketChip might take a **long** time.*

Then you need to download the necessary files (by typing the following, files will be downloaded in your home directory).

```bash
cd ~
git clone https://github.com/N0ciple/chipdigit.git
```

To lauch ChipDigit simply type :
```
python ~/chipdigit/main.py
```


### How to train ChipDigit with your writing
By default, ChipDigit already comes with a few images in order to be able to recognize writing. However you might want to train ChipDigit on your own writing. To do so, in the bash console type :
```bash
cd chipdigit
cd train
rm img*
rm counter
```
Then lauch ChipDigits which will automatically startup to training mode. Enters a few sample of your writing (typically arround 30 to 50 images are fine). Then click on the **Recon** to let ChipDigit build the new classification model and access recognition mode. (Depending on the number of sample pictures you have, building the model could take up to a few tens of seconds).


#### *Acknowledgement*
*The part of the code dealing with the canevas zone where you can write you digits have been taken from **PaintT**, available on GitHub [here](https://github.com/ChuntaoLu/PainT)*

