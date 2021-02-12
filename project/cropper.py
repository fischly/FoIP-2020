
import cv2
import math
import numpy as np
import os

class Cropper:
    def __init__(self, input_directory, output_directory):
        # set the properties of the Cropper class given the argumnents of the constructor
        self.input_directory = input_directory
        self.output_directory = output_directory

        self.current_image_index = 0

        # get all paths of image files in the given directory
        self.image_paths = self.get_all_image_files(self.input_directory)

        # stores the cropping area for each of our images
        self.cropping_areas = [{'from': None, 'to': None} for _ in self.image_paths]

        # load the first image
        self.load_next_image()

        # a variable to help rendering the current rectangle that should be cropped to
        self.is_mouse_down = False


    def run(self):
        """Runs the Cropper application, creating it's own window and starting the application loop."""
        # initialize the window 
        cv2.namedWindow("cropper")
        # register function that gets called on mouse events
        cv2.setMouseCallback("cropper", self.on_mouse_event)
        
        # used to store the key that was pressed after each key stroke
        pressed_key = 0

        # main application loop. loops until the user presses 'q'
        while pressed_key is not ord('q'):
            # first, draw the image onto the canvas 
            self.render_preview()

            # wait indefinitely for a key press and store the pressed key into 
            pressed_key = cv2.waitKey(0) & 0xFF

            # go to the next image
            if (pressed_key is ord('n')):
                self.current_image_index += 1
                # loop over if we reach the last picture in the array
                if (self.current_image_index >= len(self.image_paths)):
                    self.current_image_index = 0
                self.load_next_image()
            # go to previous image
            if (pressed_key is ord('b')):
                self.current_image_index -= 1
                if (self.current_image_index < 0):
                    self.current_image_index = len(self.image_paths) - 1
                self.load_next_image()

            # if the s-key is pressed, all images that have been given a cropping area are cropped and stored on the disk
            if (pressed_key is ord('s')):
                self.crop_all_images()
                exit(0)

    def on_mouse_event(self, event, x, y, flags, params):
        """Handles all mouse events, like clicks and mouse moves."""
        if event == cv2.EVENT_LBUTTONDOWN:
            # print('on mouse down with x={0}, y={1}, flags={2}, params={3}, event={4}'.format(x,y,flags,params, event))
            self.cropping_areas[self.current_image_index]['from'] = (x, y)

            # print('set cropping area of image with id={}:'.format(self.current_image_index))
            # print(self.cropping_areas[self.current_image_index])

            self.is_mouse_down = True

        if event == cv2.EVENT_LBUTTONUP:
            # print('on mouse up with x={0}, y={1}, flags={2}, params={3}, event={4}'.format(x,y,flags,params, event))
            self.cropping_areas[self.current_image_index]['to'] = (x, y)

            # print('set cropping area of image with id={}:'.format(self.current_image_index))
            # print(self.cropping_areas[self.current_image_index])
        
            self.is_mouse_down = False
            # update the preview
            self.render_preview()
        
        # if we moved our mouse while the mouse was clicked, we are currently specifying a crop area
        # therefore we draw the area between the position where the mouse was pressed down and the current mouse position as a rectangle
        if event == cv2.EVENT_MOUSEMOVE and self.is_mouse_down == True:
            self.current_image = self.current_image_copy.copy()
            curr_crop_area = self.cropping_areas[self.current_image_index]

            cv2.rectangle(self.current_image, curr_crop_area['from'], (x, y), (255, 0, 0), 2)
            cv2.imshow("cropper", self.current_image)

    

    def get_all_image_files(self, directory):
        """Tries to find all image files in the given directory and returns the path to all found image files as an array."""
        # retrieve all files in the given directory
        files = os.listdir(directory)
        # # we now only have relative paths, but we want full paths, making working with them later on easier
        files = [os.path.join(directory, filename) for filename in files]
    
        # only take files that end with .jpg, .jpeg, .png or .gif
        accepted_endings = ['jpg', 'jpeg', 'png', 'gif']
        image_files = []
        
        # iterate over all files we got and over all accepted endings. if a file ends with an accepted ending we store it
        for file in files:
            for ending in accepted_endings:
                if file.endswith(ending):
                    image_files.append(file)
                    break
                    
        # return only the filtered image files
        return image_files
    
    def load_next_image(self):
        """Loads current (specified by self.current_image_index) image from the file system."""
        current_image_path = self.image_paths[self.current_image_index]
        print('current image: {}'.format(current_image_path))

        # store the loaded image in a variable and store a copy of the image as well
        # that way we can draw onto the image that gets rendered without having to reload the original image each frame
        self.current_image = cv2.imread(current_image_path)
        self.current_image_copy = self.current_image.copy()

        return self.current_image

    def render_preview(self):
        """Draws the current image onto the window, adding some features to visualize the specified crop area - if it was specified yet."""
        curr_crop_area = self.cropping_areas[self.current_image_index]
        # check if we already got a cropping area set for the current image
        if (curr_crop_area['from'] is not None and curr_crop_area['to'] is not None):
            # if a cropping area is set, render the cropping area
            self.current_image = self.current_image_copy.copy()
            self.current_image = self.draw_shadow_onto_image(self.current_image, curr_crop_area['from'], curr_crop_area['to'])
            # draw a rectangle visualizing the cropping area onto the current image
            cv2.rectangle(self.current_image, curr_crop_area['from'], curr_crop_area['to'], (255, 0, 0), 2)

        # finally draw the image
        cv2.imshow("cropper", self.current_image)

    def draw_shadow_onto_image(self, image, point1, point2):
        """Darkens the region out of the given rectangle. This is helpful to visualize the cropping area."""
        # create a overlay image to darken the original image
        overlay = np.ones(image.shape, dtype=np.uint8)
        # use cv2.addWeighted to combine the overlay and the original image
        overlayed = cv2.addWeighted(overlay, 0.25, image, 0.75, 1.0)

        # calculate the topLeft and bottomRight points
        # this is neccessary since the given first point can be "smaller" than the given second point
        # therefore indexing a rectangle of an image like: img[p1.y:p2.y, p1.x:p2.x] does only work in the 4th quadrant
        # to solve this, calculate the topmost/leftmost point and the bottommost/rightmost point of the given rectangle
        top_left = (min(point1[0], point2[0]), min(point1[1], point2[1]))
        bottom_right = (max(point1[0], point2[0]), max(point1[1], point2[1]))
        # restore the crop region to be non darkened again
        overlayed[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        return overlayed


    def crop_all_images(self):
        """Tries to crop all images and writes the results to the output directory that was given to the constructor."""
        print('Cropping images and store them to "{}"'.format(self.output_directory))

        # array to store output1 in
        output1 = [[] for _ in range(len(self.image_paths))]

        # iterate over all images
        for index, image_path in enumerate(self.image_paths):
            # retrieve the stored crop area for the current image
            curr_crop_area = self.cropping_areas[index]
            
            # if there was no complete crop area set for the current image, we skip it 
            if (curr_crop_area['to'] is None or curr_crop_area['from'] is None):
                print('Skipped image "{}" due to having no crop area specified.'.format(image_path))
                continue
            
            # load the image data (TODO: maybe load all images at the start? this would potentially mean a lot of RAM being used, when a directory with many images is selected)
            curr_image = cv2.imread(image_path)
            cropped_image = curr_image[curr_crop_area['from'][1]:curr_crop_area['to'][1], curr_crop_area['from'][0]:curr_crop_area['to'][0]]

            # parse the last part of the input file and calculate the output path
            output_file_name = os.path.basename(image_path)
            output_full_path = os.path.join(self.output_directory, output_file_name)

            # handle case where the file already exist. overwrite it or skip it?
            if (os.path.exists(output_full_path)):
                os.remove(output_full_path)

            print('Writing cropped image ({0}) to {1}'.format(image_path, output_full_path))
            
            # write the image to the file system
            cv2.imwrite(output_full_path, cropped_image)

            # ---- calculating output 1 ----
            # your output should be rows of a matrix, the row should be like this:
            # Output 1:
            # "object ID" | "image ID/name” | All pixels of the related object 
            output1[index] = [
                index,
                output_file_name,       # the base name of the image file
                cropped_image.shape,    # since we should flatten the image, we need to store the shape of the image as well, otherwhise it will be hard to retrieve the original image
                cropped_image.flatten() # we should store all pixels of the image here, so we need a 1-d representation -> flatten
            ]
        
        # just return the output1 for now, I don't know what we should further do with it
        return output1


