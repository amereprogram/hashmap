# Name: Amir Najafi
# OSU Email: najafiam@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7 Hash Map
# Due Date: 12/3/2021
# Description: Implement the Hash Map class. Will have put, get, remove, contains keys, clear, empty buckets,
# resize table, table load and get keys methods.


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change the underlying hash table capacity.
        """
        clear_hash = LinkedList()
        capacity = self.capacity
        for i in range(0, capacity):
            self.buckets.set_at_index(i, clear_hash)
            self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map, returns None.
        """

        if self.contains_key(key) == False:  # returns None if key is not in hash map
            return None

        hash_func = self.hash_function(key)
        capacity = self.capacity
        index = hash_func % capacity
        return self.buckets[index].contains(key).value   # returns the key value


    def put(self, key: str, value: object) -> None:
        """
        Updates key / value pair in hash map. If a given key already exists, its associated value
        is replaced with the new value. If a given key is not in the hash map, a key / value pair must be added.
        """
        hash_func = self.hash_function(key)
        index = hash_func % self.capacity
        b_list = self.buckets[index]

        if self.contains_key(key) == True:   # if key already in hash map then it removes key and replaces with key
            # and new value.
            b_list.remove(key)
            b_list.insert(key, value)
        else:                               # else a new key value pair is added
            b_list.insert(key, value)
            self.size += 1


    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If a given key is not in the hash map,
        the method does nothing.
        """
        hash_func = self.hash_function(key)
        capacity = self.capacity
        index = hash_func % capacity

        if self.buckets[index].contains(key) is None:   # if key not in hash map, method does nothing
            return

        self.buckets[index].remove(key)
        self.size -= 1   # reduces size after removing key


    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in hash map, otherwise returns False.
        An empty hash map does not contain any keys.
        """
        hash_func = self.hash_function(key)
        index = hash_func % self.capacity
        list = self.buckets[index]

        if list.contains(key) is None:
            return False
        else:
            return True


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        counter = 0     # create a counter to count empty buckets
        capacity = self.capacity
        for i in range(0, capacity):
            if self.buckets[i].length() == 0:
                counter += 1    # increments if buckets are empty
        return counter

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        load_factor = self.size / self.capacity
        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. If new_capacity is less than 1, method will do nothing.
        """
        if new_capacity < 1:    # if new capacity is less than 1 method does nothing
            return

        old_data = self.buckets
        self.buckets = DynamicArray()
        self.capacity = new_capacity    # set new capacity value of hash map

        for i in range(new_capacity):
            self.buckets.append(LinkedList())   # iterates through new capacity to change the amount of buckets

        self.size = 0           # re initialize hash map after emptying

        for n in range(0, old_data.length()):    # iterates through the original buckets
            # and retrieve values for rehashing
            chains = old_data[n]
            for l in chains:
                self.put(l.key, l.value)


    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all keys stored in your hash map.
        """
        get_dyn_arr = DynamicArray()
        for i in range(self.capacity):   # iterate through indexes
            for n in self.buckets.get_at_index(i):    # iterate through values
                get_dyn_arr.append(n.key)      # adds all keys to new Dynamic Array object
        return get_dyn_arr



# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
