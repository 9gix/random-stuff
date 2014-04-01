import unittest

def selection_sort_right(lst):
    """Start sorting from the higest value to smallest
    start from the right to the left
    find the index which hold the highest value
    swap the highest index to the right 
    Growth: O(n^2)
    """

    # n-1 -> 1
    for i in range(len(lst)-1, 0, -1): 
        # Growth: O(t * (n-1))

        # Step1: Find Lowest Index
        index = i
        for j in range(i): 
            # Growth: O(t*(n-1)*n) = O(n^2)

            if lst[j] > lst[index]:
                index = j

        # Step2: Swap
        tmp = lst[i]
        lst[i] = lst[index]
        lst[index] = tmp

    return lst

def selection_sort_left(lst):
    """Start sorting from the lowest value to highest
    start from the left to the right
    find the index which hold the lowest value
    swap the lowest index to the left
    Growth: O(n^2)
    """

    # 1 -> n-1
    for i in range(len(lst)):  # Step 0: loop for the next lowest
        # Growth: O(t * (n-1))

        # Step1: Find Lowest Index
        index = i
        for j in range(i+1, len(lst)): 
            # Growth: O(t*(n-1)*n) = O(n^2)

            if lst[j] < lst[index]:
                index = j

        # Step2: Swap
        tmp = lst[i]
        lst[i] = lst[index]
        lst[index] = tmp

    return lst

def insertion_sort(lst):
    """Start sorting from the left to right
    swap for each elements if it is greater than the element before
    Growth: O(n^2)

    Ref: 
    """

    # 1 -> n-1
    for i in range(1,len(lst)): 
        # O(t*(n-1))

        v = lst[i]
        j = i - 1
        while j >= 0 and lst[j] > v:

            # O(t*(n-1)*n)
            lst[j+1] = lst[j]
            j -= 1

        lst[j+1] = v

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
    def test_ertion_sort(self):
        lst = insertion_sort(self.lst)
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])
    def test_selection_sort_left(self):
        lst = selection_sort_left(self.lst)
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])
    def test_selection_sort_right(self):
        lst = selection_sort_right(self.lst)
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])
    def test_merge(self):
        lst = merge([1,3,6,9,10],[2,4,5,7,8])
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])

    def test_merge_sort(self):
        lst = merge_sort(self.lst)
        self.assertEquals(lst, [1,2,3,4,5,6,7,8,9,10])

if __name__ == '__main__':
    unittest.main()


