def say_hello(name= None):
    if name is None:
        return "Hello, World! version1 >>1.0.1.0"
    else:
        return f"Hello, {name}! version1 >>1.0.1.0"