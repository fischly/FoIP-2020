import argparse
import os

from cropper import Cropper

if __name__ == "__main__":
    # use argparse to parse the command line inputs: input directory and output directory
    parser = argparse.ArgumentParser(description='Allows to crop images of a given directory in a fast way, storing the cropped images into the given output directory.')
    parser.add_argument('in_dir', metavar='input-directory', type=str, nargs=1, help='the directory the images should be read from')
    parser.add_argument('out_dir', metavar='output-directory', type=str, nargs=1, help='the directory the cropped images should be stored at')

    args = parser.parse_args()

    # use abspath at first, so different way of writing directories on different plattforms get handled by the os.path module first 
    input_dir = os.path.abspath(args.in_dir[0])
    output_dir = os.path.abspath(args.out_dir[0])

    # check if the directories exist
    if not os.path.exists(input_dir):
        print('given input directory does not exist. ({})\naborting.'.format(input_dir))
        exit(1)
    if not os.path.exists(output_dir):
        print('given output directory does not exist. ({})\naborting.'.format(output_dir))
        exit(1)


    # instantiate a new Cropper object and giving the read directories to the ctor
    c = Cropper(input_dir, output_dir)
    # running the Cropper application
    c.run()


