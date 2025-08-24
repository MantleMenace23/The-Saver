# Minimal fake audioop module so discord.py doesn't crash on platforms without it
def add(*args, **kwargs): return b""
def adpcm2lin(*args, **kwargs): return (b"", 0)
def avg(*args, **kwargs): return 0
def avgpp(*args, **kwargs): return 0
def bias(*args, **kwargs): return b""
def cross(*args, **kwargs): return 0
def getsample(*args, **kwargs): return 0
def lin2adpcm(*args, **kwargs): return (b"", 0)
def lin2lin(*args, **kwargs): return b""
def lin2ulaw(*args, **kwargs): return b""
def max(*args, **kwargs): return 0
def maxpp(*args, **kwargs): return 0
def minmax(*args, **kwargs): return (0, 0)
def mul(*args, **kwargs): return b""
def ratecv(*args, **kwargs): return (b"", None)
def rms(*args, **kwargs): return 0
def tomono(*args, **kwargs): return b""
def tostereo(*args, **kwargs): return b""
def ulaw2lin(*args, **kwargs): return b""
