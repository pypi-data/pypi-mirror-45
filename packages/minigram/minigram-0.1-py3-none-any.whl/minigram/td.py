import json

class Generic:
    def __init__(self):
        self._raw = {"@type": self.__class__.__name__}
        
    def __getattribute__(self, key):
        if key in ["_raw", "__class__", "serialize"]: return object.__getattribute__(self, key)
        if key == "_type": return self._raw["@type"]
        try:
            return self._raw[key]
        except KeyError:
            return None
            
    def __setattr__(self, key, value):
        if key == "_raw": return object.__setattr__(self, key, value)
        self._raw[key] = value
        
    def serialize(self):
        d = {}
        for key, value in self._raw.items():
            d[key] = value.serialize() if issubclass(type(value), Generic) else value
            
        return json.dumps(d)
        
def parse(raw):
    if raw == "":
        return
    raw = json.loads(raw)
    if "@type" not in raw:
        raise ValueError("Parsing requires a @type attribute")
    
    t = raw.pop("@type")
    obj = __getattr__(t)()
    
    for key, value in raw.items():
        if type(value) is dict:
            setattr(obj, key, parse(value))
        else:
            setattr(obj, key, value)
    
    return obj
    
_types = {}

def __getattr__(type_name):
    if type_name == "parse":
        return parse
    try:
        return _types[type_name]
    except KeyError:
        new_class = type(type_name, (Generic,), {})
        new_class.type = type_name
        _types[type_name] = new_class
        return new_class

    
