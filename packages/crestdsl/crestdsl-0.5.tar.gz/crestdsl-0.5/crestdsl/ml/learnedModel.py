import crestdsl.model as crest


import logging
logger = logging.getLogger(__name__)


def get_learned_modifier(modifier, learner):
    
    if isinstance(modifier, crest.Transition):
        learned_mod = LearnedTransition(modifier.source, modifier.target, modifier.guard)
    if isinstance(modifier, crest.Update):
        learned_mod = LearnedUpdate(modifier.state, modifier.target, modifier.function)
    elif isinstance(modifier, crest.Influence):
        learned_mod = LearnedInfluence(modifier.source, modifier.target, modifier.function)
    elif isinstance(modifier, crest.Action):
        learned_mod = LearnedAction(modifier.function, modifier.transition, modifier.target)
    
    learned_mod.wrapped = modifier
    learned_mod.learner = learner
    
    return learned_mod


class LearnedTransition(crest.Transition):
    
    def __init__(self, source, target, guard, name="", parent=""):
        pass
    
    @property
    def source(self):
        return self.wrapped.source
        
    @property
    def target(self):
        return self.wrapped.target
    
    @property
    def guard(self):
        return self.learner.learned_function

    def __deepcopy__(self, memo):
        new = LearnedTransition(None, None, None)
        new.wrapped = copy.deepcopy(self.wrapped, memo)
        new.learner = self.learner
        return new

class LearnedUpdate(crest.Update):
    
    def __init__(self, function, state, target, name="", parent=None):
        pass
    
    @property
    def state(self):
        return self.wrapped.state
        
    @property
    def target(self):
        return self.wrapped.target
    
    @property
    def function(self):
        return self.learner.learned_function

    def __deepcopy__(self, memo):
        new = LearnedUpdate(None, None, None)
        new.wrapped = copy.deepcopy(self.wrapped, memo)
        new.learner = self.learner
        return new
    

class LearnedInfluence(crest.Influence):

    def __init__(self, source, target, function=None, name="", parent=None):
        pass
    
    @property
    def source(self):
        return self.wrapped.source
        
    @property
    def target(self):
        return self.wrapped.target
    
    @property
    def function(self):
        return self.learner.learned_function

    def __deepcopy__(self, memo):
        new = LearnedInfluence(None, None, None)
        new.wrapped = copy.deepcopy(self.wrapped, memo)
        new.learner = self.learner
        return new
        
    @property
    def _parent(self):
        return self.wrapped._parent 
    
    @_parent.setter
    def set_parent(self, value):
        if self.wrapped != None:
            self.wrapped._parent = value
    
    @property
    def _name(self):
        return self.wrapped._name 
    
    @_name.setter
    def set_name(self, value):
        if self.wrapped != None:
            self.wrapped._name = value



class LearnedAction(crest.Action):
    
    def __init__(self, function, transition, target, name="", parent=None):
        pass
    
    @property
    def transition(self):
        return self.wrapped.transition
        
    @property
    def target(self):
        return self.wrapped.target
    
    @property
    def function(self):
        return self.learner.learned_function
        
    def __deepcopy__(self, memo):
        new = LearnedAction(None, None, None)
        new.wrapped = copy.deepcopy(self.wrapped, memo)
        new.learner = self.learner
        return new
        
    @property
    def _parent(self):
        return self.wrapped._parent 
    
    @_parent.setter
    def set_parent(self, value):
        if self.wrapped != None:
            self.wrapped._parent = value
    
    @property
    def _name(self):
        return self.wrapped._name 
    
    @_name.setter
    def set_name(self, value):
        if self.wrapped != None:
            self.wrapped._name = value


