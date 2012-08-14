import unittest

def insertion_sort(lst):
    for j in range(1,len(lst)):
        v = lst[j]
        i = j - 1
        while i >= 0 and lst[i] > v:
            lst[i+1] = lst[i]
            i -= 1
        lst[i+1] = v

    return lst

def merge(left, right):
    result = []
    while len(left) > 0 or len(right) > 0:
        if len(left) > 0 and len(right) > 0:
            if left[0] <= right[0]:
                result.append(left[0])
                left = left[1:]
            else:
                result.append(right[0])
                right = right[1:]
        elif len(left) > 0:
            result.append(left[0])
            left = left[1:]
        elif len(right) > 0:
            result.append(right[0])
            right= right[1:]
    return result

def merge_sort(lst):
    if len(lst) <= 1:
        return lst
    m = len(lst) / 2
    left, right = [], []
    for i in lst[:len(lst)/2]:
        left.append(i)
    for i in lst[len(lst)/2:]:
        right.append(i)
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)

class SortTest(unittest.TestCase):
    def setUp(self):
        self.lst = [9,3,1,5,4,2,8,10,7,6]
    def test_insertion_sort(self):
        lst = insertion_sort(self.lst)
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])
    def test_merge(self):
        lst = merge([1,3,6,9,10],[2,4,5,7,8])
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])

    def test_merge_sort(self):
        lst = merge_sort(self.lst)
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])

if __name__ == '__main__':
    unittest.main()


