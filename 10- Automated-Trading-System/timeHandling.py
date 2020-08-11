import time


def fibonachi(n):
    """Recursive function to print nth Fibonacci number"""
    if n <= 1:
        return n
    else:
        return fibonachi(n - 2) + fibonachi(n - 1)


StartTime = time.time()
EndTime = time.time() + 2*60
n_ = 0
while time.time() <= EndTime:
    print(fibonachi(n_))
    n_ += 1
    time.sleep(10)

