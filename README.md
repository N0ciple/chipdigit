# ChipDigits
ChipDigits is a simple python script which performs handwritting recognition. There are two modes : 
* Recognition Mode
* Training Mode

## Modes

### Recognition Mode
In recognition mode you can simply draw a digit between 0 and 9 and the label at the top of the drawing zone will change to print which number have been recognized. This is visible on the illustration picture.

Here is a picture of the recognition mode :

![alt text](http://image.noelshack.com/fichiers/2017/11/1489593058-img2.png "Recognition Mode Picture")

### Training Mode
Since everybody writes in a different manner, you might want to train ChipDigit to your own writting style. To do so, you can access the Training Mode. In training mode, a small text box on the left of the screen is asking you to write a precise digit. Write it, and it's automatically stored. To prevent you from being bored and wrtiting the number exactly the same way, the number you have to write are chosen randomly.

Here is a picture of the training mode :

![alt text](http://image.noelshack.com/fichiers/2017/11/1489593058-img3.png "Training Mode Picture")

## Instructions

### How to train ChipDigit with your writting
By default, ChipDigit already comes with a few images in order to be able to recognize writting. However you might want to train ChipDigit on your own writting. To do so, in the bash console type :
```bash
cd chipdigit
cd train
rm img*
rm counter
```
Then lauch ChipDigits which will automatically startup to training mode. Enters a few sample of your writting (typically arround 30 to 50 images are fine). Then click on the **Recon** to let ChipDigit build the new classification model and access recognition mode. (Depending on the number of sample pictures you have, building the model could take up to a few tens of seconds).


#### *Acknowledgement*
*The part of the code dealing with the canevas zone where you can write you digits have been taken from **PaintT**, available on GitHub [here](https://github.com/ChuntaoLu/PainT)*

