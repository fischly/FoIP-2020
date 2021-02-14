# Cropper

Cropper allows to crop images of a given directory in a fast way, storing the cropped images into the given output directory.

## Installation

Download cropper.py and cropping.py and store them inside the same directory - or just clone this repository.

## Usage

```
python cropping.py <input-directory> <output-directory>
```

One can switch between the next and previous image with the keys `n` and `b` respectively.
Pressing down the left mouse button starts the cropping area selection. Hold down the button and drag it to the desired position.
After that, a prompt will ask to give a text describing the selected object (annotation). For every box that is made, an annotation MUST be also made.

One can crop and save all images pressing the `s` key. Only images where an actual selection was made are cropped and stored.
A csv file is also made in the output directory with the annotation data. The application can be shut down pressing the `q` key.

```
usage: cropping.py [-h] input-directory output-directory

Allows to crop and annotate images of a given directory in a fast way, storing the cropped
images into the given output directory.

positional arguments:
  input-directory   the directory the images should be read from
  output-directory  the directory the cropped images should be stored at

optional arguments:
  -h, --help        show this help message and exit
  -a, --annotate    starts asking for an annotation after each image
```
