from typing import Callable

from dbus_next.service import ServiceInterface, method

from mprisv.core import Command

class Interface(ServiceInterface):

    def __init__(self, name, dispatch: Callable):
        super().__init__(name)
        self.dispatch = dispatch

    @method()
    async def Play(self):
        await self.dispatch(Command.PLAY)

    @method()
    async def Pause(self):
        await self.dispatch(Command.PAUSE)

    @method()
    async def Next(self):
        await self.dispatch(Command.NEXT)

    @method()
    async def Prev(self):
        await self.dispatch(Command.PREV)

    @method()
    async def Stop(self):
        await self.dispatch(Command.STOP)

    @method()
    async def PlayPause(self):
        await self.dispatch(Command.PLAY_PAUSE)   
