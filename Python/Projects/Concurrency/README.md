
- [asyncio](#asyncio)
- [Reference](#reference)

This project is to demonstrate how Python works for concurrency. The version of Python is expected to be 3.7 or above.

![overview](overview.png)

Python has a memory management feature called __the GIL__, or __Global Interpreter Lock__.


1. why async and when
2. async and await (asyncio)
3. multi-threaded parallelism
4. thread safety
5. multi-process parallelism
6. execution pools
7. extending async patterns
8. async web frameworks
9. parallelism in C (with Cython)


- Do more at once
  - asyncio
  - threads
- Do things faster
  - multiprocessing
  - C / Cython
- Do both easier
  - trio
  - unsync


## asyncio
Cooperative Concurrency or Parallelism



> Asynchrony,  in computer programming, refers to the occurrence of events independent of the main program flow and ways to deal with such events.
> These may be "outside" events such as the arrival of signals, or actions instigated by a program that take place concurrently with program execution, without the program blocking to wait for results.


- thread
- process
- asyncio


## Reference
- Async Techniques and Examples in Python: https://training.talkpython.fm/courses/details/async-in-python-with-threading-and-multiprocessing
- Power and Head Problems Led to Multiple Cores and Prevent Further Improvements in Speed: https://www.slideshare.net/Funk98/end-of-moores-law-or-a-change-to-something-else
- Sample Code: https://github.com/talkpython/async-techniques-python-course
