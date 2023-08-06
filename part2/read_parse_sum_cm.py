import json, time, myjson, json_parser
from perf import *
import haversine

profiler = Profiler()

with ProfileBlock('read', profiler):
    with open('json_points', encoding='utf-8') as f:
        d = f.read()


with ProfileBlock('parse', profiler):
    py_dict2 = myjson.loads(d)
    # py_dict2 = json_parser.loads(d)
    # py_dict2 = json.loads(d)


with ProfileBlock('hd_calc', profiler):
    total_sum = 0
    for p in py_dict2['pairs']:
        total_sum += haversine.haversine_distance(p['x0'], p['y0'], p['x1'], p['y1'])
    total_avg = total_sum / len(py_dict2['pairs'])

profiler.result()
exit()