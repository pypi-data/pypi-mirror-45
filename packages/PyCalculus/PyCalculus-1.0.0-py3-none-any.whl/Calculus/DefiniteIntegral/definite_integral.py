from threading import Thread
from time import sleep

"""
 * 
 *  Coded by Rickiarty @ GitHub 
 * 
"""

def eval_single_partition(math_func, from_x, to_x):
    if from_x > to_x:
        t = from_x
        from_x = to_x
        to_x = t
    dx = to_x - from_x
    from_y = math_func(from_x)
    to_y = math_func(to_x)
    aver_y = (from_y + to_y) / 2.0
    return aver_y * dx

def eval_single_partition_concurrently(mutex, sum_obj, math_func, from_x, to_x):
    while True:
        if mutex:
            sleep(1) # 0.001 second(s) 
            continue
        else:
            mutex = True
            sum_obj[0] += eval_single_partition(math_func, from_x, to_x)
            mutex = False
            break
    return

def summarize_multiple_partitions(math_func, from_x, to_x, div_num):
    coef = 1
    sum = 0.0
    if from_x > to_x:
        t = from_x
        from_x = to_x
        to_x = t
        coef = -1
    dx = (float(to_x) - float(from_x)) / div_num
    for i in range(div_num):
        sum += eval_single_partition(math_func, float(from_x) + i*dx, float(from_x) + ((i+1)*dx))
    return coef * sum

def summarize_multiple_partitions_concurrently(math_func, from_x, to_x, div_num):
    threads = []
    coef = 1
    sum_obj = [0.0]
    if from_x > to_x:
        t = from_x
        from_x = to_x
        to_x = t
        coef = -1
    dx = (float(to_x) - float(from_x)) / div_num

    mutex = False
    thread = None
    for i in range(div_num):
        thread = Thread(target=eval_single_partition_concurrently, args=(mutex, sum_obj, math_func, float(from_x) + i*dx, float(from_x) + ((i+1)*dx)))
        threads.append(thread) # Append the thread to the list for management. 
        thread.start() # Start the thread. 
    
    # Wait for all sub-threads to end. 
    for th in threads:
        th.join()
    
    return coef * sum_obj[0]
