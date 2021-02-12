# Cropper

Cropper allows to crop images of a given directory in a fast way, storing the cropped images into the given output directory.

## Installation

Download cropper.py and cropping.py and store them inside the same directory - or just clone this repository.

## Usage

```bash
python cropping.py <input-directory> <output-directory>
```

One can switch between the next and previous image with the keys `n` and `b` respectively.
Pressing down the left mouse button starts the cropping area selection. Hold down the button and drag it to the desired position.

One can crop and save all images pressing the `s` key. Only images where an actual selection was made are cropped and stored.
The application can be shut down pressing the `q` key.

```bash
usage: cropping.py [-h] input-directory output-directory

Allows to crop images of a given directory in a fast way, storing the cropped
images into the given output directory.

positional arguments:
  input-directory   the directory the images should be read from
  output-directory  the directory the cropped images should be stored at

optional arguments:
  -h, --help        show this help message and exit
```