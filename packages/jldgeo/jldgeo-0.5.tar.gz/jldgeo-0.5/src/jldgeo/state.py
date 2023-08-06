'''
Created on Apr. 24, 2019

@author: jldupont

state(a,b,c) = action
'''

class StateExists(Exception): pass
class NoDefaultStateExists(Exception): pass

class States:
    """
    Collection of [state, action] pairs
    
    The hierarchical map is constructed using the following:
    
      { l1_state1: { l2_state1: { l3_state1: action_state1 } }
       ,l1_state2: { l2_state2: { l3_state2: action_state2 } }
       ,l1_state3: { l2_state3: action_state3 }
       ... 
      }
      
    Whereas 'action' is a callable object and 'state' is a string.
    """
    
    def __init__(self):
        self._map = {}
    
    def add(self, action, *components):
        """
        Add a [state, action] pair
        
        Each positional parameter constitute
        a level in the hierarchy of the map
        """
        assert len(components) > 0, "Must have at least of state component"
        assert callable(action), "Parameter 'action' must be a callable"
        
        def _add(_map, action, cp):
            
            # Terminate the recursion
            if len(cp) == 0:
                return
            
            # Are we at the last step, ready to assign the action?
            if len(cp) == 1:
                #
                # Is there already something at this state?
                #
                try:
                    _ = _map[cp[0]]
                except:
                    #
                    # State does not exists so use, perfect.
                    #
                    _map[cp[0]] = action
                else:
                    raise StateExists("State is already defined at: "+str(components))
                
                return
            
            #
            # We are in the "middle" of the process.
            # 
            #
            down_map = _map.get(cp[0], {})
            
            if callable(down_map):
                raise StateExists("Action already present at this state: "+str(components))
            
            #
            # This is just really necessary to initialize the chain
            #
            _map[cp[0]] = down_map
            
            # Recurse...
            #
            _add(down_map, action, cp[1:])
        
        _add(self._map, action, components)
        
    def get(self, *components):
        """
        Retrieves a mapping [state, action]
        """
        assert len(components) > 0, "Must have at least 1 state component"
        
        def _drill(_map, cp):
            comp = cp[0]
            if len(cp) == 1:
                maybe_action = _map.get(comp, None)
                if maybe_action is None:
                    return None
                
                if callable(maybe_action):
                    return maybe_action
                
                #
                # It's not a callable
                #  so it can't be a match at this point...
                #
                return None
            
            maybe_next_level = _map.get(comp, None)
            if maybe_next_level is None:
                return None
            
            return _drill(maybe_next_level, cp[1:])
        
        return _drill(self._map, components)
    
    def step(self, context, *components):
        """
        Performs a step
        """
        action = self.get(*components)
        
        if action is None:
            catch_all_entry = list(components[:-1])
            catch_all_entry.append('*')
            # Is there a catch-all in place ?
            default_action = self.get(*catch_all_entry)
            if default_action is None:
                raise NoDefaultStateExists(str(catch_all_entry))
            
            action = default_action
        
        return action({"context": context, "state": components})

    