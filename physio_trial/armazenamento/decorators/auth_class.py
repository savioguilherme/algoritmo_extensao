from armazenamento.decorators.auth_method import auth_method

def auth_class(cls):
    for attr_name, attr in cls.__dict__.items():
        if callable(attr) and not attr_name.startswith("_"):
            setattr(cls, attr_name, auth_method(attr))
    return cls
