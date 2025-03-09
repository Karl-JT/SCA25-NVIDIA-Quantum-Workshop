"""
@brief test of python interface 
"""
import sys, os
sys.path.append('../')
import cppimport
profile_util = cppimport.imp("profile_util_pyinterface")

def test_timer():
     timer = profile_util.Timer("file", "function", "line", False)
     print(timer.get())

if __name__ == '__main__':
    test_timer()
