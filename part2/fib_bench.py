from read_parse_sum_decor import print_cpu_tick

x = 10

@print_cpu_tick
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

fib(5)

