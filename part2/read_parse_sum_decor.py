import perf
import haversine
cpu_freq = perf.get_cpu_freq()
print('CPU Freq', cpu_freq)

import traceback
import inspect

def print_cpu_tick(func):
    def wrapper(*args, **kwargs):
        start = perf.get_cpu_tick()
        f = func(*args, **kwargs)
        end = perf.get_cpu_tick()


        func_stack = [i.name + '() > ' for i in traceback.extract_stack() if i.name not in ('wrapper', '<module>')]
        # print(func_stack)
        # func_stack = ''.join(map(str, func_stack))
        print('\t' * int(len(func_stack)-1) + ''.join(map(str, func_stack)) +
              func.__code__.co_name + str(args) + ' took', end - start, 'cycles;', round((end - start)/ cpu_freq * 1000,5) ,'ms')
        return f
    return wrapper

@print_cpu_tick
def main():
    @print_cpu_tick
    def read():
        with open('json_points', encoding='utf-8') as f:
            data = f.read()
            return data

    d = read()

    @print_cpu_tick
    def parse(data):
        import json, myjson
        return myjson.loads(data)

    json_content = parse(d)

    @print_cpu_tick
    def sum(json_content):

        @print_cpu_tick
        def hd(x0,y0,x1,y1):
            return haversine.haversine_distance(x0, y0, x1, y1)

        total_sum = 0
        for p in json_content['pairs']:
            total_sum += hd(p['x0'], p['y0'], p['x1'], p['y1'])
        total_avg = total_sum / len(json_content['pairs'])
        return total_avg, len(json_content['pairs'])

    result = sum(json_content)
    print('Ave haversine dist', result[0], 'for', result[1],'points')

if __name__ == '__main__':
    main()