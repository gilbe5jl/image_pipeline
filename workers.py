from PIL import Image, ImageFilter
import io
import sys
from multiprocessing import Queue

def apply_filter(image_data, filter_type:str):
    '''
    io.BytesIO is a class in Python's io module that provides an in-memory file-like object for working with binary data. 
    It's useful when you need to treat a sequence of bytes as if it were a file, without actually writing to disk.

    '''
    img = Image.open(io.BytesIO(image_data))

    if filter_type == 'grayscale':
        img = img.convert('L')  # Convert to grayscale
    elif filter_type == 'blur':
        img = img.filter(ImageFilter.BLUR)

    output = io.BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()

def image_worker_process(input_queue:Queue, output_queue:Queue, filter_type:str)->None:
    """
    @param input_queue: Queue for receiving image data and names
    @param output_queue: Queue for sending processed image data
    @param filter_type: Type of filter to apply ('grayscale' or 'blur')
    @return: None
    This function continuously processes images from the input queue,
    applies the specified filter, and puts the processed images into the output queue.
    It runs until it receives a None item in the input queue, which signals it to stop.
    It handles exceptions during processing and logs errors to stderr.
    """
    while True:
        item = input_queue.get()
        if item is None:
            break
        name, image_data = item
        try:
            processed = apply_filter(image_data, filter_type)
            output_queue.put((name, processed))
            print(f"Processed: {name}")
        except Exception as e:
            print(f"Error processing {name}: {e}", file=sys.stderr)