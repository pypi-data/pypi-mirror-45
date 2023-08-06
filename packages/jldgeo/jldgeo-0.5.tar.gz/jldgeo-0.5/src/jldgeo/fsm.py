'''
Definition of the state machine for this utility

Created on Apr. 25, 2019
@author: jldupont


Example:
{ "type": "Feature", "properties": { "PCA_ID": 180000059, "POSTALCODE": "P0R1L0", "PROV": "ON", "MAF_ID
": 350002523, "PREC_CODE": 2, "PCA_COUNT": 516, "DOM_PCA": 0, "MULTI_PC": 0, "DEL_M_ID": "LB0001", "LON
GITUDE": -83.442568069900005, "LATITUDE": 46.289068144200002 }, "geometry": { "type": "MultiPolygon", "
coordinates": [ [ [ [ -83.432379699999956, 46.29642750000005 ], ... , [ -83.433095599999945, 46
.296466300000077 ], [ -83.432379699999956, 46.29642750000005 ] ] ] ] } },
'''
import json

class MissingEventHandling(Exception): pass
class InvalidStringForJsonObject(Exception): pass
class MissingState(Exception): pass
class ControlFlow(Exception): pass
class Skip(ControlFlow): pass
class EndOfFile(ControlFlow): pass


class Fsm:
    
    def __init__(self):
       
        self.previous_event = None
        self.current_prefix = None
        self.current_event = None
        self.feature_string = ""
    
    def submitEvent(self, prefix, event, value=None):
        """
        Dispatch event to the method
        that handles current state
        """
        self.previous_event = self.current_event
        
        try:
            self.current_prefix = prefix
            self.current_event = event
            self.current_value = value
            fnc = getattr(self, "state_"+self.state)
        except:
            raise MissingState("Missing state method: "+self.state)
            
        try:
            fnc(prefix, event, value)
        except Skip:
            pass
        
    def wait(self, expected_prefix, expected_event, *_):
        """
        Skips the current event if it does not pass the gate
        """
        if expected_prefix != self.current_prefix:
            raise Skip()
        
        if expected_event is not None:
            if expected_event != self.current_event:
                raise Skip()

    def accumulate(self):
        """
        The event data is kept at the instance level
        """
        fnc = getattr(self, "evt_"+self.current_event)
        if fnc is None:
            raise MissingEventHandling("Expected: "+str(self.current_event))

        fnc()

    def start_feature(self):
        self.feature_string = ""

    def evt_null(self):
        self.feature_string += "null"

    def evt_start_map(self):
        self.feature_string += "{ "

    def evt_end_map(self):
        self.feature_string += " }"

    def evt_map_key(self):
        self.feature_string += '"' + self.current_value + '":'
        
    def evt_start_array(self):
        self.feature_string += '['
        
    def evt_end_array(self):
        self.feature_string += ']'
        
    def evt_string(self):
        self.feature_string += '"' + self.current_value + '"'
        
    def evt_number(self):
        self.feature_string += str(self.current_value)

    def add_comma(self):
        self.feature_string += ','

    def maybe_add_comma(self):
        
        if self.previous_event == 'end_map' or self.previous_event == 'end_array':
            if self.current_event != 'end_map' and self.current_event != 'end_array':
                return self.add_comma()
        
        if self.previous_event == 'string' or self.previous_event == 'number':
            if self.current_event != 'end_map' and self.current_event != 'end_array':
                return self.add_comma()
                
        if self.current_event == 'end_map':
            return
        
        if self.current_event == 'end_array':
            return
        
        if self.previous_event is None or len(self.previous_event) == 0:
            return
        
        if self.previous_event == 'end_map':
            return 
        
        if self.previous_event == 'end_array':
            return
        
        if self.previous_event == 'start_map':
            return
        
        if self.previous_event == 'start_array':
            return
        
        if self.previous_event == 'map_key':
            return
        
        self.feature_string += ','

    def event_feature(self):
        """
        Receives complete string representing 
        a feature
        """
        try:
            # We just need to make we have a valid json
            _ = json.loads(self.feature_string)
            
        except Exception as _e:
            print(self.feature_string)
            print(_e)
            raise InvalidStringForJsonObject()
        else:
            print(self.feature_string+"\n")

'''
When to prepend a comma:

>  NUMBER , NUMBER
>  STRING , NUMBER
>  STRING , STRING
>  STRING , {
>  STRING , [
>  NUMBER , {
>  NUMBER , [
>  ] , [
>  

When NOT to prepend a comma:
>  ___ [
>  ___ {
>  ] ]
>  } }
>  ] }
>  } ]
'''

        
class GeojsonFsm(Fsm):
    
    def __init__(self):
        super().__init__()
        self.state = 'waitStartFeaturesItem'
        
    def state_waitStartFeaturesItem(self, prefix, event, value):
        
        if event == 'end_map':
            if prefix == '':
                if value == None or value == '':
                    raise EndOfFile()
        
        self.wait('features.item', 'start_map')
        self.start_feature()
        self.evt_start_map()
        self.state = 'accumulateSymbolsUntilFeatureEnd'
        
    def state_accumulateSymbolsUntilFeatureEnd(self, prefix, event, _value):
        
        if event == 'end_map':
            self.evt_end_map()
            if prefix == 'features.item':
                self.event_feature()
                self.state = 'waitStartFeaturesItem'
        else:
            self.maybe_add_comma()
            self.accumulate()

