import random, time

def generate_int_dataset(size, min, max):
    l = []
    for _ in range(0, size):
        l.append(int(random.random() * (max + 1) + min))
    return l

def set_count(data):
    return len(set(data))

def hll(data, b):
    raise NotImplementedError

def main():
    t1 = time.time()
    print('Generating dataset...')
    data = generate_int_dataset(10 ** 7, 0, 2 ** 32 - 1)
    print(f'Finished in {time.time() - t1} seconds')

    t2 = time.time()
    print('Counting using set...')
    print(f'Set contains {set_count(data)} unique elements')
    print(f'Counting completed in {time.time() - t2}')

if __name__ == '__main__':
    main()