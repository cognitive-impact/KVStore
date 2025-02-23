import requests
import numpy as np
import base64
import random
from uuid import uuid4
from tqdm import trange
import time
import json
import os

if not os.path.exists("./data.txt"):
    x = np.random.randint(25, 100, (1000, 1024))

    f_ = []

    for i in range(1000):
        f_.append(base64.b64encode(x[i].tobytes()).decode("utf-8"))

    for i in range(10):
        print(random.choice(f_))

    keys = []
    for i in range(1000):
        keys.append(str(uuid4()))

    data_ = list(zip(keys, f_))

    print(data_[:10])
    with open("data.txt", "w") as f:
        f.write(json.dumps(data_))

data = json.load(open("data.txt"))
    
top_100 = [x[1] for x in data[:100]]
top_100_keys = [x[0] for x in data[:100]]

batch_100 = [x[1] for x in data[100:600]]
batch_100_keys = [x[0] for x in data[100:600]]
print(len(batch_100[0]))



print("Setting keys 1 by 1")
times = []

for i in trange(100):
    start = time.time()
    requests.post("http://localhost:1234/kvstore/v1/set", json={"key": top_100_keys[i], "value": top_100[i]})
    times.append(time.time()-start)
print(f"Time taken per request over 100 requests: {np.round(np.mean(times)*1000, 4)}ms to SET")

print("Getting keys 1 by 1")
times = []
f_ = []
start = time.time()
for i in trange(100):
    start = time.time()
    f_.append(requests.get(f"http://localhost:1234/kvstore/v1/get?key={top_100_keys[i]}").json())
    times.append(time.time()-start)
print(f"Time taken per request over 100 requests: {np.round(np.mean(times)*1000, 4)}ms to GET")

for i in f_:
    try:
        if not i["value"] == top_100[f_.index(i)]:
            print(f"Error: {i}")
    except:
        print(f"Error: {i}")

print("Deleting keys 1 by 1")
times = []
f_ = []
for i in trange(100):
    start = time.time()
    f_.append(requests.post(f"http://localhost:1234/kvstore/v1/delete?key={top_100_keys[i]}").json())
    times.append(time.time()-start)
print(f"Time taken per request over 100 requests: {np.round(np.mean(times)*1000, 4)}ms to DELETE")

print("Setting keys in batch")
start = time.time()
resp = requests.post("http://localhost:1234/kvstore/v1/mset", json={"keys": batch_100_keys, "values": batch_100})
print(f"Time taken to MSET 100 keys: {np.round((time.time()-start)*1000, 4)}ms")

f_ = []
print("Getting keys in batch")
start = time.time()
f_ = requests.post("http://localhost:1234/kvstore/v1/mget", json=batch_100_keys).json()
print(f"Time taken to MGET 500 keys: {np.round((time.time()-start)*1000, 4)}ms")

for i in f_:
    if not i["value"] == batch_100[f_.index(i)]:
        print("Error")

print("Deleting keys in batch")
start = time.time()
resp = requests.post("http://localhost:1234/kvstore/v1/mdelete", json=batch_100_keys)
print(f"Time taken to MDELETE 500 keys: {np.round((time.time()-start)*1000, 4)}ms")

count = 2000
print(f"Generating prefix and contains filter data: {count} datapoints")
new_data = np.random.randint(25, 100, (100000, 1024))

search_data = []

for i in trange(count):
    search_data.append(base64.b64encode(new_data[i].tobytes()).decode("utf-8"))

prefix_search_keys = [f"user_id::{str(uuid4())}" for i in range(count//2)]
contains_search_keys = [f"user_id::{str(uuid4())}::deactivated" for i in range(count//2)]

all_search_keys = prefix_search_keys.copy()
all_search_keys.extend(contains_search_keys)
print(len(all_search_keys))

index_name = "Test Index"
response = requests.post("http://localhost:1234/kvstore/v2/exists", json={"index":index_name, "key":"random_key"})
print(response.status_code, response.text)

response = requests.post("http://localhost:1234/kvstore/v2/set", json={"index":index_name, "key":"random_key", "value":"random_value"})
print(response.status_code, response.text)

response = requests.post("http://localhost:1234/kvstore/v2/exists", json={"index":index_name, "key":"random_key"})
print(response.status_code, response.text)

response = requests.post("http://localhost:1234/kvstore/v2/delete", json={"index":index_name, "key":"random_key"})
print(response.status_code, response.text)


# print(f"Setting filter data {count} keys")
# f_set = {
#     "index":index_name, 
#     "keys":all_search_keys,
#     "values":search_data
# }
# start = time.time()
# f_ = requests.post("http://localhost:1234/kvstore/v2/mset", json=f_set)
# print(f"Time taken to MSET {count} keys: ", np.round((time.time()-start)*1000, 4))
# print(f_.status_code, f_.json())

# f_get = {
#     "index":index_name,
#     "keys":all_search_keys[:10]
# }

# print(f"Getting data (100) points")
# start = time.time()
# f_ = requests.post("http://localhost:1234/kvstore/v2/mget", json=f_get)
# print(f"Time taken to MGET 10 keys: ", np.round((time.time()-start)*1000, 4))
# print(f_.json())


# prefix_filter = "user_id"
# print(f"Getting prefix filter data")
# f_get = {
#     "index":index_name,
#     "prefix":prefix_filter
# }

# start = time.time()
# f_ = requests.post("http://localhost:1234/kvstore/v2/prefixFilter", json=f_get)
# print(f"Time taken to PREFIXFILTER {count} keys: ", np.round((time.time()-start)*1000, 4))
# print(f_.status_code)

# contains_filter = "deactivated"
# print(f"Getting contains filter data")
# f_get = {
#     "index":index_name,
#     "contains":contains_filter
# }

# start = time.time()
# f_ = requests.post("http://localhost:1234/kvstore/v2/filter", json=f_get)
# print(f"Time taken to FILTER {count} keys: ", np.round((time.time()-start)*1000, 4))
# print(f_.json()[0].keys())
# print(f_.status_code)


# print("Deleting filter data")
# f_del = {
#     "index":index_name,
#     "keys":all_search_keys
# }
# start = time.time()
# f_ = requests.post("http://localhost:1234/kvstore/v2/mdelete", json=f_del)
# print(f_.status_code)
# print(f"Time taken to MDELETE {count} keys: ", np.round((time.time()-start)*1000, 4))

