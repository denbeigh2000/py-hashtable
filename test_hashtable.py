#!/usr/bin/python2

ht = HashTable(10)

ht.put(1, 'world')
ht.put(11, 'planet')
ht.put(21, 'yahoo')
ht.put(31, 'altavista')
ht.put(41, 'bing')

print ht.get(1)
print ht.get(11)
print ht.get(21)
print ht.get(31)
print ht.get(41)
