# 100_000
# 0.09768033027648926
# 7.15291690826416

# 1_000_000
# 0.8824529647827148
# 73.65929889678955

import json, time, myjson
import perf
import haversine
cpu_freq = perf.get_cpu_freq()

read_start = perf.get_cpu_tick()
with open('json_points', encoding='utf-8') as f:
    d = f.read()
read_end = perf.get_cpu_tick()

parse_start = perf.get_cpu_tick()
# py_dict2 = myjson.load(d)
py_dict2 = json.loads(d)
parse_end = perf.get_cpu_tick()

sum_start = perf.get_cpu_tick()
total_sum = 0
for p in py_dict2['pairs']:
    total_sum += haversine.haversine_distance(p['x0'], p['y0'], p['x1'], p['y1'])
total_avg = total_sum / len(py_dict2['pairs'])
sum_end = perf.get_cpu_tick()

print('Avg Haversine distance', total_avg ,'of', len(py_dict2['pairs']), 'points')
read_time = (read_end - read_start) / cpu_freq * 1000
parse_time = (parse_end - parse_start) / cpu_freq * 1000
sum_time = (sum_end - sum_start) / cpu_freq * 1000
total_time = read_time + parse_time + sum_time
print('Read time', read_end - read_start, 'cycles;',round(read_time,2), 'ms(', round(read_time * 100/total_time, 2),'%)')
print('Parse time', parse_end - parse_start, 'cycles;',round(parse_time,2), 'ms(',round(parse_time*100/total_time,2),'%)')
print('Sum time', sum_end - sum_start, 'cycles;',round(sum_time,2), 'ms(', round(sum_time*100/total_time,2),'%)')