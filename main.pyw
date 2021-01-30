from multiprocessing import Pipe, Process, Value
from Sources.gui import Gui
from Sources.othercamera import Camera

class Application(object):
    def __init__(self):
        Parent, Child = Pipe(duplex=False)
        self.Alive = Value('b',True)
        self.processes = [
            Process(target = Gui, args=(Parent, self.Alive,)),
            Process(target = Camera, args=(Child, self.Alive,))
        ]

    def run(self):
        for process in self.processes:
            process.start()

    def tilEnd(self):
        while self.Alive:
            for process in self.processes:
                if not process.is_alive():
                    self.Alive = False
                process.join()

if __name__ == '__main__':
    main = Application()
    main.run()
    main.tilEnd()