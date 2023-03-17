import time

start_time = time.time()
time.sleep(5)
end_time = time.time()
elapsed_time = end_time - start_time
print('Total simulation time cost is {}'.format(elapsed_time))