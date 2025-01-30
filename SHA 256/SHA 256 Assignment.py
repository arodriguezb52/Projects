import hashlib
import multiprocessing

names = 'Louise Renan Henry Alejandro'
max_zeros = 10  # Target for leading zeros
num_processes = multiprocessing.cpu_count()  # Number of CPU cores

def hash_with_nonce(names, nonce):
    input_string = f'{names} {nonce}'
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

def find_nonce(start_nonce, step, names, max_zeros):
    nonce = start_nonce
    while True:
        hash_result = hash_with_nonce(names, nonce)
        if hash_result.startswith('0' * max_zeros):
            return nonce, hash_result
        nonce += step

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=num_processes)
    results = []

    # Use multiple processes, each searching with different starting points
    for i in range(num_processes):
        results.append(pool.apply_async(find_nonce, (i, num_processes, names, max_zeros)))

    # Get the first result that finds a valid nonce
    for result in results:
        nonce, hash_result = result.get()
        if hash_result.startswith('0' * max_zeros):
            print(f'Found nonce: {nonce}')
            print(f'Hash: {hash_result}')
            pool.terminate()  # Stop other processes once a valid nonce is found
            break
