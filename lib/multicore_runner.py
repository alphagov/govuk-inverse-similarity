from multiprocessing import Process, Queue

def run_multicore(cores, function, data):
  q = Queue()
  data_chunks = chunk_data(cores, data)
  output_unsorted = {}
  sorted_output = []
  for i in range(0, cores):
    process = Process(target=function, args=(q, data_chunks[i], i))
    process.start()
  while(True):
    output_unsorted.update( q.get() )
    if len(output_unsorted) == cores:
      break
    time.sleep(10)
  for i in range(0, cores):
    sorted_output.extend(output_unsorted[i])
  return sorted_output

def chunk_data(cores, data_list):
  out = []
  chunk_size = len(data_list) / cores
  for i in range(0, cores):
    start = chunk_size * i
    if i == (cores - 1):
      end = len(data_list)
    else:
      end = (chunk_size * (i+1))
    out.append(data_list[start:end])
  return out