from mprisv.core import App, Status, Command
from mprisv import events

def test_generates_pause_action_on_headphones_disconnect():
    app = App('mpd', Status.PLAYING)
    assert app.handle_event(events.Disconnect) == ('mpd', Command.PAUSE)

def test_generates_resume_action_on_reconnect():
    app = App('mpd', Status.PLAYING)
    app.handle_event(events.Disconnect)
    assert app.handle_event(events.Reconnect) == ('mpd', Command.PLAY)

def test_only_generates_resume_on_reconnect_if_playing_previously():
    app = App('mpd', Status.PAUSED)
    app.handle_event(events.Disconnect)
    assert app.handle_event(events.Reconnect) == None

def test_pauses_the_old_player_when_new_player_playing():
    app = App('mpd', Status.PLAYING)
    assert app.handle_event(events.PlayerPlayed('firefox')) == ('mpd', Command.PAUSE)
    assert app.last_player == 'mpd'

def test_switches_back_to_the_old_player():
    app = App('mpd', Status.PLAYING)
    app.handle_event(events.PlayerPlayed('firefox'))
    assert app.handle_event(events.PlayerStopped) == ('mpd', Command.PLAY)

def test_pause_on_suspend():
    app = App('mpd', Status.PLAYING)
    assert app.handle_event(events.Suspend) == ('mpd', Command.PAUSE)
    # Start playing if headphones plugged in after resume, but not on resume
    assert app.play_on_reconnect == True
