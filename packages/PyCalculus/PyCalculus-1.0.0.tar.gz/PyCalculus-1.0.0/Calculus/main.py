import sys
from DefiniteIntegral.definite_integral import summarize_multiple_partitions, summarize_multiple_partitions_concurrently
import time

"""
 * 
 *  Coded by Rickiarty @ GitHub 
 * 
"""

def example_math_func1(x):
    x = float(x)
    y = 3 * (x**2)
    return float(y)

from_x = float(sys.argv[1])
to_x = float(sys.argv[2])
div_num = int(sys.argv[3])

print('', end='\n')

start = time.time()
print('single thread computing ...')
# single thread
sum1 = summarize_multiple_partitions(example_math_func1, from_x, to_x, div_num)
end = time.time()
print(str(sum1) + ' [single thread]')
print('the time cost: ' + str(end - start) + ' second(s)')

print('', end='\n')

start = time.time()
print('multiple threads computing ...')
# multiple threads
sum2 = summarize_multiple_partitions_concurrently(example_math_func1, from_x, to_x, div_num)
end = time.time()
print(str(sum2) + ' [multiple threads]')
print('the time cost: ' + str(end - start) + ' second(s)')

print('', end='\n')
