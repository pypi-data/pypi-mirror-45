'''
Created on Apr. 25, 2019

@author: jldupont
'''
import unittest

from jldgeo.fsm import GeojsonFsm, MissingState

class Test(unittest.TestCase):

    def setUp(self):
        
        self.f = GeojsonFsm()

    def testFsmSimple(self):
        
        self.f.submitEvent(None, None, None)
        
        assert self.f.state == 'waitStartFeaturesItem', "got: "+self.f.state
        
    def testFsmSimple2(self):
        
        self.f.submitEvent('features', 'start_array')
        assert self.f.state == 'waitStartFeaturesItem'

    def testFsmSimple3(self):

        self.f.submitEvent('features', 'start_array')
        self.f.submitEvent('features.item', 'start_map')

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFsmSimple']
    unittest.main()