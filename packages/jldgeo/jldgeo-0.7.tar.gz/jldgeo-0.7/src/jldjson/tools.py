'''
Created on Apr. 28, 2019

@author: jldupont
'''
import json


class ExpectingDict(Exception):
    """
    The value in the (key:value) pair
    is not of type dict
    """

class ExpectingJSONObject(Exception):
    """
    Expecting to decode a JSON object
    from the provided string
    """

class ControlFlow(Exception):
    """
    Base class for flow control exceptions
    """

class Skip(ControlFlow):
    """
    Skip the current iteration
    """

def stringify(input_obj, which_key_to_stringify):
    
    for key in which_key_to_stringify:
        value_to_stringify = input_obj[key]
        
        try:
            result = json.dumps(value_to_stringify)
        except:
            raise ExpectingJSONObject(str(value_to_stringify))
        
        input_obj[key] = result
        
    return input_obj


def loader(line):
    
    line = " ".join(line.split())
    
    if len(line) == 0:
        raise Skip()
    
    try:
        jobj = json.loads(line)
        
    except:
        raise ExpectingJSONObject("Got: "+str(line))
    
    return jobj


def keep(input_obj, which_key_to_keep):
    out = {}
    for key in which_key_to_keep:
        if key in input_obj:
            out[key] = input_obj[key]
    return out
    

def unpack(input_obj, which_key_to_unpack):
    
    out = {}
    
    for key, value in input_obj.items():
        
        if key in which_key_to_unpack:
            if not isinstance(value, dict):
                raise ExpectingDict("key: "+key)
            
            out.update(input_obj[key])
            
        else:
            out[key] = value
        
    return out
