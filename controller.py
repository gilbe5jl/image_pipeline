import os
import time
import multiprocessing as mp
import threading
import queue
from io_threads import load_images_threaded, save_images_threaded
from workers import image_worker_process

# Queues for communication
processing_queue = mp.Queue()
output_queue = mp.Queue()

# Directory setup
INPUT_DIR = 'images'
OUTPUT_DIR = 'output'
FILTER = 'grayscale'  # Or 'blur'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def start_worker_processes(num_processes):
    processes = []
    for _ in range(num_processes):
        p = mp.Process(target=image_worker_process, args=(processing_queue, output_queue, FILTER))
        p.start()
        processes.append(p)
    return processes

def main():
    '''
    step 1:
        Creates a thread for loading images from the input dir '/images'
        start the thread after passing in args 
    step 2:
        get the number of CPU cores 
        we then pass that number into the function `start_worker_processes`
        which creates worker processes that will process the images
    step 3:
        Creates a thread for saving processed images to the output dir '/output'
        start the thread after passing in args
    step 4:
        Creates a thread for saving images to the output dir '/output'
    
    '''
    # Step 1: Start I/O loader threads
    image_paths = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.lower().endswith(('jpg', 'png', 'jpeg'))]
    load_done_event = threading.Event()
    load_thread = threading.Thread(target=load_images_threaded, args=(image_paths, processing_queue, load_done_event))
    load_thread.start()

    # Step 2: Start worker processes
    num_cores = mp.cpu_count()
    workers = start_worker_processes(num_cores)

    # Step 3: Start I/O saver threads
    save_done_event = threading.Event()
    save_thread = threading.Thread(target=save_images_threaded, args=(output_queue, OUTPUT_DIR, save_done_event))
    save_thread.start()

    # Step 4: Wait for image loading to finish
    load_thread.join()
    print("Image loading complete. Sending stop signals to workers...")

    # Signal end of processing
    for _ in workers:
        processing_queue.put(None)

    # Step 5: Wait for all workers to finish
    for p in workers:
        p.join()
    print("All worker processes complete.")

    # Step 6: Signal save thread to finish
    output_queue.put(None)
    save_thread.join()
    print("All images saved. Pipeline complete.")

if __name__ == '__main__':
    import multiprocessing as mp
    # Set the start method for multiprocessing, which is necessary for Windows or other OS
    # This ensures that the multiprocessing module uses the 'spawn' method, the 'spawn' is used because its safer for starting new processes in a cross-platform way.
    mp.set_start_method('spawn', force=True)  #`force=True` to override if already set, this is for compatibility with Windows mainly
    from controller import main  # Import everything else after setting the start method
    main() # This ensures that the multiprocessing start method is set before any processes are created.