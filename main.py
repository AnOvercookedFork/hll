import random, time, math, hashlib

class HLL:
    def __init__(self, b):
        self.b = b
        self.longest = [0] * (2 ** self.b)
        if b == 4:
            self.alpham = 0.673
        elif b == 5:
            self.alpham = 0.697
        elif b == 6:
            self.alpham = 0.709
        else:
            self.alpham = 0.7213/ (1 + 1.079 / (2 ** b))


    def ingest(self, data):
        bcount = [0] * (2 ** self.b)
        for d in data:
            h = int(hashlib.md5(str(d).encode()).hexdigest(), 16)
            bucket = h >> (128 - self.b)
            bcount[bucket] += 1
            h = h << self.b
            lz = self.count_leading_zeroes(h)
            if lz > self.longest[bucket]:
                self.longest[bucket] = lz
        return self.estimate()

    def estimate(self):
        m = 2 ** self.b
        acc = 0
        for l in self.longest:
            acc += 2 ** (-1 * l)
        # print(acc)
        hmean =  m / acc

        raw_estimate = self.alpham * m * hmean
        # print(hmean)
        # print(raw_estimate)
        # print(f'{[i for i in self.longest if i != 0]}')
        # print(f'{[i for i in bcount if i != 0]}')
        # small value correction (linear counting)
        if raw_estimate < 5 / 2 * m:
            count = 0
            for bucket in self.longest:
                if bucket == 0:
                    count += 1
            print(count)
            print('using linear counting')
            raw_estimate = m * math.log(m / count)
            

        return round(raw_estimate)

    def count_leading_zeroes(self, i):
        count = 1
        mask = 1 << 63  # Start with a mask that has a 1 at the 64th bit
        while mask and not (i & mask):
            count += 1
            mask >>= 1
            if count > 128 - self.b:
                return 128 - self.b
        return count
    
    def merge(self, hll):
        if self.b != hll.b:
            raise ValueError('target hll does not have same b as this hll')
        else:
            for i in range(0, len(self.longest)):
                self.longest[i] = max(self.longest[i], hll.longest[i])
    

def generate_int_dataset(size, min, max):
    l = []
    for _ in range(0, size):
        l.append(int(random.random() * (max + 1) + min))
    return l

def set_count(data):
    s = set(data)
    return (len(set(data)), s)

def main():
    t = time.time()
    print('Generating dataset...')
    data = generate_int_dataset(10 ** 7, 0, 2 ** 32 - 1)
    # data = [i for i in range(0, 1000)]
    print(f'Finished in {time.time() - t} seconds')

    t = time.time()
    print('Counting using set...')
    count1, s = set_count(data)
    print(f'Set contains {count1} unique elements')
    print(f'Counting completed in {time.time() - t}')

    hll = HLL(4)
    t = time.time()
    print('Counting using HLL...')
    hll.ingest(data)
    count = hll.estimate()
    print(f'Set contains approximately {count} unique elements')
    print(f'HLL counting completed in {time.time() - t}')

    print()

if __name__ == '__main__':
    main()