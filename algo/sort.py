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


class SortTest(unittest.TestCase):
    def setUp(self):
        self.lst = [9,3,1,5,4,2,8,10,7,6]
    def insertion_sort_test(self):
        lst = insertion_sort(self.lst)
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])

if __name__ == '__main__':
    unittest.main()

