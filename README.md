## about the project
mprisv is a small daemon that can automatically control mpris enabled media players. it's meant to be a replacement for playerctl, and can be used to:

 - Play/pause media on headphones reconnect/disconnect (bluetooth only at the moment)
 - Pause music when playing a video in a browser
 - Pause music on suspend

It uses the python [dbus-next](https://github.com/altdesktop/python-dbus-next) library to listen for events.

This is sort of a first pass - it needs to be refactored for better testability and configurability, but it seems to work well in my case.

## usage
It can be enabled as, e.g. a systemd user unit to listen for events and automatically play/pause media. `mprisv` starts the daemon.

With the daemon running it can also be controlled with `mprisv` subcommands. Subcommands are:

 - mprisv {play, pause, stop, next, prev, playpause}
