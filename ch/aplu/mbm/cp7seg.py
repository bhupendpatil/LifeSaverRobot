# cp7seg.py
# Version 2.00, Dec. 6, 2018

from calliope_mini import pin26, pin27, sleep

PATTERN = b'\0\x86\x22\0\0\0\0\x02\0\0\0\0\x04\x40\x80\x52\x3f\x06\x5b\x4f\x66\x6d\x7d\x07\x7f\x6f\0\0\0\x48\0\0\x5d\x77\x7c\x39\x5e\x79\x71\x3d\x76\x30\x0e\x70\x38\x55\x54\x3f\x73\x67\x50\x2d\x78\x3e\x36\x6a\x49\x6e\x1b\x39\x64\x0f\x23\x08\x20\x77\x7c\x58\x5e\x79\x71\x3d\x74\x10\x0c\x70\x30\x55\x54\x5c\x73\x67\x50\x2d\x78\x1c\x36\x6a\x49\x6e\x1b\0\x30\0\x41'

_cw = pin26.write_digital
_dw = pin27.write_digital
_lum = 4
_colon = False

def show(text):
    text = str(text)  # digits to chars
    if len(text) < 4:
        text = "%-4s" % text
    data = _toSegment(text)
    _prepare(0x40)    
    _wB(0xC0)
    for i in range(4):
        _wB(data[i])
    _commit()
        
def colon(enable):
    global _colon
    _colon = enable
    
def luminosity(lum):
    global _lum
    _lum = lum
                        
def _wB(data):
    for i in range(8):
        _cw(0)
        if data & 0x01:
            _dw(1)
        else:
            _dw(0)
        data = data >> 1
        _cw(1)

    _cw(0)
    _dw(1)
    _cw(1)
    
    # wait for ACK
    while pin27.read_digital() == 1:
        sleep(1)

def _toSegment(text):
    data = []
    msb = 0
    if _colon:
        msb = 0x80
    for c in text:
        data.append(PATTERN[ord(c) - 32] + msb)
    return data

def _start():
    _cw(1)
    _dw(1)
    _dw(0) 
    _cw(0) 

def _stop():
    _cw(0) 
    _dw(0) 
    _cw(1)
    _dw(1)
    
def _prepare(addr):        
    _start()
    _wB(addr)
    _stop()
    _start()

def _commit():
    _stop()
    _start()
    _wB(0x88 + _lum)
    _stop()
