## Concurrency Comparison for Image I/O: Multithreading vs Multiprocessing

**Date:** 2025-10-22  
**Category:** Experiment

### 🔍 Insights
- Multi-threading: single process, many threads, Multi-processing: many process, many threads, Thread Pooling: single process with managable threads
- I/O bound - CPU bound - I/O bound repetitive tasks
- Downloading/API calls/File reading - ML/Image processing/heavy math - server requests

### 🧪 Task Definition
Limit TensorFlow’s internal threads to ensure isolated execution, use 15 workers to read, decode, and standardize a local image in parallel. Measure total execution time, CPU, and GPU usage to evaluate performance for both Multithreading and Multiprocessing

### 📎Code Results
- GitHub Link: [d03'01_multithreading_img.ipynb](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d03'01_multithreading_img.ipynb)
~~~python
MULTITHREADING RESULTS:
Time taken: 0.157 sec
CPU usage start → end: 11.0% → 8.0%
GPU usage (end):
  GPU-0: 0.0% load, 0.0% mem
Processed 15 images successfully.

MULTIPROCESSING RESULTS: ERROR!
~~~

### 🐞 Issues Faced
- 🔄 TensorFlow operations crash or hang under multiprocessing on Windows due to missing context and incompatible process creation. 
- 🧠 Windows uses spawn instead of fork to create new processes, which starts a fresh interpreter rather than copying the parent state. TensorFlow relies on special internal objects. These objects can't be re-instantiated automatically in the child process, causing failures when multiprocessing tries to access them. 

### ✅ Fixes Applied
- Used controlled multiprocessing by limiting TensorFlow to 1 thread per process, enabling 15 parallel processes without conflict — successfully bypassed Windows spawn limitations.
- GitHub Link: [d03'02_multiprocessing_img.ipynb](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d03'02_multiprocessing_img.ipynb)

### 🔁 Updated Observations
- In both threading and synthetic multiprocessing, workers read the same image and create separate in-memory copies. Threads can share TensorFlow tensors, but processes can't—so each worker builds its own tensor to ensure safe, isolated execution.
~~~python
MULTITHREADING RESULTS:
Time taken: 0.157 sec
CPU usage start → end: 11.0% → 8.0%
GPU usage (end):
Processed 15 images successfully.

MULTIPROCESSING RESULTS:
Time taken: 0.170 sec
CPU usage start → end: 9.3% → 17.0%
GPU usage (end):
  GPU-0: 0.0% load, 0.0% mem
~~~

### 🏷️ Conclusion
- We simulated multiprocessing by using multithreading with shared memory, restricting TensorFlow to one internal thread per worker. This setup mimicked process-level isolation while maintaining thread-level efficiency — effectively treating threads as fake processes.


