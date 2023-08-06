'''
Created on Apr. 24, 2019

@author: jldupont
'''
import unittest

from ..state import States, StateExists#, NoDefaultStateExists
#from ..fsm import Fsm, MissingState


class TestException(unittest.TestCase):
    
    def testOne(self):
        
        try:
            result = True # something that won't raise
        except:
            result = False
        else:
            result = 'OK'

        assert result == 'OK'


class Test(unittest.TestCase):

    @staticmethod
    def action_a(): pass

    @staticmethod
    def action1(): pass

    @staticmethod
    def action2(): pass
    
    @staticmethod
    def whatever(): pass
    
    @staticmethod
    def default(c): return c

    def testAddSimple(self):
               
        s=States()
        s.add(Test.action_a, 'a')
        
        assert s.get('a') == Test.action_a

    def testAddMissing(self):
        
        s=States()
        
        s.add(Test.action_a, 'a1', 'a2', 'a3')
        
        assert s.get('a1', 'a2', 'a3') == Test.action_a
        assert s.get('a1') == None

    def testAddComplex2(self):
        
        s=States()
        
        s.add(Test.action1, 'a11', 'a12', 'a13')
        s.add(Test.action2, 'a21', 'a22', 'a23')        
        
        assert s.get('a11', 'a12', 'a13') == Test.action1
        assert s.get('a21', 'a22', 'a23') == Test.action2
        
        assert s.get('a11') == None
        assert s.get('a11','a12') == None
        assert s.get('a11','a12','a*') == None

    def testDefault(self):
        
        s=States()
        s.add(Test.action1, 'a21', 'a22', 'a23')
        s.add(Test.default, 'a21', 'a22', '*')        
        
        result = s.step({'result': 666}, 'a21', 'a22', 'aX3')
        assert result['context']['result'] == 666

    def testAddRaiseStateExists1(self):
        
        s=States()
        
        s.add(Test.action_a, 'a1', 'a2', 'a3')

        self.assertRaises(StateExists, lambda: s.add(Test.whatever, 'a1', 'a2'))

    def testAddRaiseStateExists2(self):
        
        s=States()
        
        s.add(Test.action_a, 'a1', 'a2', 'a3')

        self.assertRaises(StateExists, lambda: s.add(Test.whatever, 'a1', 'a2', 'a3'))


"""
class TestReportErrors(unittest.TestCase):
    
    def testCallable(self):
        assert callable(ReportErrors.state_missing)

class TestFsm(unittest.TestCase):
    
    def testEcho(self):
        s=States() 
        f=Fsm(s)
        
        s.add(f.echo, 'c1')       
        
        ctx = {"in": "test"}
        
        result = f.step(ctx, "c1")
        assert result['context']['in'] == 'test'
        
    def testMissingState(self):
        s=States()
        f=Fsm(s)
        
        ctx={}
        self.assertRaises(MissingState, lambda: f.step(ctx,'invalidState'))
"""
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()