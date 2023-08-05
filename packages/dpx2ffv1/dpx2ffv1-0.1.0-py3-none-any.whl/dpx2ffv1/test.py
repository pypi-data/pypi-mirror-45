from unittest import TestCase
from dpx2ffv1.dpx2ffv1 import dpx2ffv1

class TestJoke(TestCase):
    def test_main_function(self):
        out = dpx2ffv1('./test/', 'out.mkv', 24)
        assert(out == 0)

if __name__ == '__main__':
    unittest.main()