"""An amazing yynb package!"""

__version__ = '0.2.1'

def solve(*args):
    print("yy knows everything!")
    rarg = []
    for arg in args:
        print(str(arg) + " is too simple!")
        rarg.append("Solved")
    return rarg

def whoami():
    import webbrowser
    webbrowser.open("https://iamsmally.github.io/")
    return
