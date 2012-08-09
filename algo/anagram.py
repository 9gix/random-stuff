import unittest
import string

def isAnagram(str1, str2):
    for i in str1:
        if i.lower() not in str2.lower() and i in string.letters: return False
    for i in str2:
        if i.lower() not in str1.lower() and i in string.letters: return False
    return True

class TestAnagramFunction(unittest.TestCase):
    def setUp(self):
        # Exact Matches
        self.wordA1 = "i love python"
        self.wordA2 = "live hot pony"
        # Space Difference
        self.wordB1 = "Indonesia"
        self.wordB2 = "Idea in son"
        # Capitalization Difference
        self.wordC1 = "Indonesia"
        self.wordC2 = "IdeaInSon"
        # Symbolics Difference
        self.wordD1 = "abcDefghiJklMnoPqrsTuVwxyz       "
        self.wordD2 = "Mr. Jock, TV quiz PhD bags few lynx."

    def test_anagram_exact(self):
        result = isAnagram(self.wordA1, self.wordA2)
        self.assertTrue(result)

    def test_anagram_space(self):
        result = isAnagram(self.wordB1, self.wordB2)
        self.assertTrue(result)

    def test_anagram_capitalize(self):
        result = isAnagram(self.wordC1, self.wordC2)
        self.assertTrue(result)

    def test_anagram_punctuation(self):
        result = isAnagram(self.wordD1, self.wordD2)
        self.assertTrue(result)

    def test_not_anagram(self):
        result = isAnagram(self.wordA1, self.wordB1)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

