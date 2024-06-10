import unittest

def sum_of_two_numberss(a, b):
    return a + b

class TestSums(unittest.TestCase):
    def test_sum_of_two_numbers(self):
        # Arrange
        a = 5
        b = 7

        # Act
        result = sum_of_two_numberss(a, b)

        # Assert
        self.assertEqual(result, 12)

if __name__ == '__main__':
    unittest.main()