import multiprocessing

def read_file(file_path):
   
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"Contents of {file_path}:\n{content}\n")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    n = 3 
    file_paths = [f"file{i}.txt" for i in range(1, n+1)]  

   
    processes = []
    for file_path in file_paths:
        p = multiprocessing.Process(target=read_file, args=(file_path,))
        processes.append(p)
        p.start()

   
    for p in processes:
        p.join()
