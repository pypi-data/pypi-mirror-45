'''
Created on Apr. 28, 2019

@author: jldupont
'''
import unittest

from jldjson.tools import unpack

class Test(unittest.TestCase):

    def testUnpack1(self):
        d={"a": 666, "b": {"b1": 777, "b2": 888}}

        r=unpack(d, ["b"])
        
        assert r['a'] == 666
        assert r['b1'] == 777
        assert r['b2'] == 888
        
        assert r.get("b", None) == None

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()