
# Casserole Singleton Infrastructure
# Based on https://stackoverflow.com/q/6760685 - creating
# singletons with metaclasses. Namely, any class which should
# be a singleton should inherit `metaclass=Singleton` in its constructor
# On the first instantiaion, the single instance will be created and added
# to the global _instances dictionary

# When the instance is destroyed, 

_instances = {}

class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if cls not in _instances:
            #print(f"{type(cls)}-new cls:{cls}")
            _instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            #print(f"{type(cls)}-instances are after adding:{_instances}")
        #print(f"{type(cls)}-returning={_instances[cls]}")
        return _instances[cls]
    
def destroyAllSingletonInstances():
    global _instances
    print(f"instances were:{_instances}")
    _instances = {}
    print(f"instances are:{_instances}")

def noSingletonsAround():
    print(f"instances are:{_instances}")
    return len(_instances)==0
    
class ShortSingltonLivesUnderTest:
    # https://stackoverflow.com/questions/26405380/how-do-i-correctly-setup-and-teardown-for-my-pytest-class-with-tests

    @classmethod
    def setup_class(cls): # pylint: disable=invalid-name
        assert noSingletonsAround()


    @classmethod
    def teardown_class(cls): # pylint: disable=invalid-name
        destroyAllSingletonInstances()
