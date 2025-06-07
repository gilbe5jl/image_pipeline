# image_pipeline
Image Processing Pipeline with Threaded I/O and Multiprocessed Filters

1.	Controller starts:
	•	A thread pool for loading images
	•	A process pool for filtering
	•	A thread pool for saving output
2.	Queues connect:
	•	Threaded loaders → put into processing_queue
	•	Workers → get from processing_queue, apply filter, put into output_queue
	•	Threaded savers → get from output_queue and write to disk
3.	Graceful shutdown after all tasks are done


image_pipeline/
├── controller.py        # entry point and controller
├── workers.py           # multiprocessing logic
├── io_threads.py        # I/O threading for load/save
├── images/              # input images
└── output/              # processed output

1.	Loads images from a folder using threads (I/O-bound task)
2.	Sends the images to worker processes that apply filters like grayscale or blur (CPU-bound)
3.	Saves the processed images using threads again
4.	Uses a master controller process to orchestrate it all

⸻

🧱 Tools & Libraries
	•	Python 3
	•	multiprocessing
	•	threading
	•	queue
	•	Pillow for image processing

# Concurrent Image Filter Pipeline

This project loads images from disk using threads, processes them using a multiprocessing filter engine, and writes them out using threads again.

It demonstrates:
- Threaded I/O for non-blocking file operations
- Multiprocessing for CPU-bound image filtering
- Queue-based communication between threads/processes
- Clean shutdown coordination

## To Run:
1. Place .jpg or .png files in the `images/` folder.
2. Run `python run_pipeline.py`.
3. Processed images appear in the `output/` folder.

You can change the filter (e.g. grayscale, blur) in `run_pipeline.py`.