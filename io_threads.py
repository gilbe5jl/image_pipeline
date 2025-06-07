from PIL import Image
import threading
# import queue
import os
import io
from multiprocessing import Queue


def load_images_threaded(image_paths:list, processing_queue:Queue, done_event: threading.Event)-> None:
    """
    @param image_paths: List of paths to image files
    @param processing_queue: Queue for sending image data to worker processes
    @param done_event: Event to signal when loading is complete
    @return: None
    This function loads images from the specified paths in a separate thread.
    It reads each image file, converts it to bytes, and puts the name and bytes into the processing queue.
    It handles exceptions during loading and signals when all images have been loaded.
    It uses a threading.Event to signal when the loading is complete.
    """
    def worker():
        for path in image_paths: # Iterate over the list of image paths
            try:
                with open(path, 'rb') as f: # Open the image file in binary mode for reading 'rb' reads bytes
                    img_bytes = f.read() # f.read() returns the entire content of the file as bytes
                name = os.path.basename(path) # Get the image name from the path
                processing_queue.put((name, img_bytes)) # Put image name and bytes into the queue
                print(f"Loaded: {name}")
            except Exception as e:
                print(f"Error loading {path}: {e}")
        done_event.set() # Signal that loading is done

    thread = threading.Thread(target=worker) # Create a thread to run the worker function by creating a Thread object
    thread.start() # Start the thread
    thread.join() # Wait for the thread to finish

def save_images_threaded(output_queue, output_dir, done_event):
    def worker():
        while True:
            item = output_queue.get()
            if item is None:
                break
            name, img_bytes = item
            try:
                img = Image.open(io.BytesIO(img_bytes)) # Load image from bytes
                output_path = os.path.join(output_dir, name) 
                img.save(output_path)
                print(f"Saved: {name}")
            except Exception as e:
                print(f"Error saving {name}: {e}")
        done_event.set()

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()