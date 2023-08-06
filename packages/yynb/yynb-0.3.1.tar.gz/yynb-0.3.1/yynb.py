"""An amazing yynb package!"""

__version__ = '0.3.1'

def solve(*args):
    print("yy knows everything!")
    if len(args) == 0:
        return
    rarg = []
    for arg in args:
        print(str(arg) + " is too simple!")
        rarg.append("Solved")
    return rarg

def whoami():
    import webbrowser
    webbrowser.open("https://iamsmally.github.io/")
    return
