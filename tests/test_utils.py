from mprisv.utils import is_headphones

base_props = [
    'org.freedesktop.DBus.Properties', 
    'org.freedesktop.DBus.Introspectable'
]

def test_is_headphones():
    assert is_headphones(base_props + ['org.bluez.MediaPlayer1']) == False
    assert is_headphones(base_props + ['org.bluez.MediaTransport1']) == True
