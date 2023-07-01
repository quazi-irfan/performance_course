import json, time, myjson

with open('json_points', encoding='utf-8') as f:
    d = f.read()

start = time.time()
py_dict1 = json.loads(d)
print(len(py_dict1['pairs']))
print(time.time() - start)

start = time.time()
py_dict2 = myjson.load(d)
print(len(py_dict2['pairs']))
print(time.time() - start)


# 100_000
# 0.09768033027648926
# 7.15291690826416

# 1_000_000
# 0.8824529647827148
# 73.65929889678955