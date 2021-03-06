#!/usr/bin/python2

MAX_MISS_COUNT = 3

class HashTable(object):
    def __init__(self, capacity=1000, max_density=0.4):
        self.size = 0
        self.capacity = capacity

        assert type(max_density) == float and max_density > 0 \
                and max_density < 1

        self.max_density = max_density
        self.table = [None for _ in xrange(capacity)]

    def _hash_fn(self, key):
        return hash(key) % self.capacity

    def _check_capacity(self):
        """
        Returns a value between 0 and 1 of how full this hash table is
        """
        use = float(self.size) / float(self.capacity)
        return self.size / float(self.capacity)

    def _over_capacity(self):
        """
        Returns true iff this hash table should grow
        """
        return self._check_capacity() >= self.max_density

    def grow(self):
        """
        Grow the size of the hash table by double
        """
        old_capacity = self.capacity
        self.capacity = (self.capacity * 2 + 1) # Extra bit to throw off collisions in mod operation
        old_table = self.table
        self.table = [None for _ in xrange(self.capacity)]

        # Insert all entries from old table
        for entry in old_table:
            if entry is not None:
                self.put(entry.key, entry.value)

    def put(self, key, value):
        if self._over_capacity():
            self.grow()

        entry = HashTableEntry(key, value)
        hash_key = self._find_empty(entry)

        self.table[hash_key] = entry

        self.size += 1

    def _find_empty(self, entry):
        """
        Finds a hash key corresponding to an empty space in the hash table
        """
        hash_key = self._hash_fn(entry.key)
        candidate = self.table[hash_key]

        miss_count = 0

        while candidate is not None:
            miss_count += 1

            # Grow our table if we miss too many times, then start trying again
            if miss_count > MAX_MISS_COUNT:
                self.grow()
                miss_count = 0

                hash_key = self._hash_fn(entry.key)
                candidate = self.table[hash_key]
                continue

            hash_key += 1
            candidate = self.table[hash_key]

        return hash_key

    def _find_existing(self, key):
        """
        Finds a hash key corresponding to the place where the given key is stored
        Throws a KeyError if not in this hash table
        """
        hash_key = self._hash_fn(key)

        candidate = self.table[hash_key]

        def candidate_valid(cand, target_key):
            return (cand is not None) and (cand.key == target_key)

        while not candidate_valid(candidate, key):
            if candidate is None:
                return None

            else:
                hash_key += 1
                candidate = self.table[hash_key]

        return hash_key

    def get(self, key):
        hash_key = self._find_existing(key)

        if hash_key is not None:
            return self.table[hash_key].value

        raise KeyError("Key %s not in this table" % key)

    def delete(self, key):
        """
        Removes an entry associated with given key from hash table
        """
        existing_key = self._find_existing(key)
        if existing_key is not None:
            del self.table[existing_key]
            self.size -= 1


    def reshuffle(self):
        pass

class HashTableEntry(object):
    def __init__(self, k, v):
        self.key = k
        self.value = v
