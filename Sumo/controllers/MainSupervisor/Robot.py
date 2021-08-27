import math

from utils import LOSS_DIST

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        return self.queue.append(data)

    def dequeue(self):
        return self.queue.pop(0)

    def peek(self):
        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0


class RobotHistory(Queue):
    def __init__(self):
        super().__init__()

    def enqueue(self, data):
        if len(self.queue) > 8:
            self.dequeue()
        return self.queue.append(data)


class Robot:
    '''Robot object to hold values whether its in a base or holding a human'''

    def __init__(self, id, supervisor, node_name):
        self.id = id
        self.supervisor = supervisor
        self.node_name = node_name
        self.wb_node = supervisor.getFromDef(node_name)

        self.wb_translationField = self.wb_node.getField('translation')
        self.wb_rotationField = self.wb_node.getField('rotation')

        self.history = RobotHistory()

        self._timeStopped = 0
        self._stopped = False
        self._stoppedTime = None

        self.message = []

        self.inSimulation = True

        self._name=""

    @property
    def position(self) -> list:
        return self.wb_translationField.getSFVec3f()

    @position.setter
    def position(self, pos: list) -> None:
        self.wb_translationField.setSFVec3f(pos)

    @property
    def rotation(self) -> list:
        return self.wb_rotationField.getSFRotation()

    @rotation.setter
    def rotation(self, pos: list) -> None:
        self.wb_rotationField.setSFRotation(pos)

    def setMaxVelocity(self, vel: float) -> None:
        self.wb_node.getField('max_velocity').setSFFloat(vel)

    def _isStopped(self) -> bool:
        vel = self.wb_node.getVelocity()
        robotStopped = abs(vel[0]) < 0.01 and abs(vel[1]) < 0.01 and abs(vel[2]) < 0.01
        return robotStopped

    def timeStopped(self) -> float:
        self._stopped = self._isStopped()

        # if it isn't stopped yet
        if self._stoppedTime == None:
            if self._stopped:
                # get time the robot stopped
                self._stoppedTime = self.supervisor.getTime()
        else:
            # if its stopped
            if self._stopped:
                # get current time
                currentTime = self.supervisor.getTime()
                # calculate the time the robot stopped
                self._timeStopped = currentTime - self._stoppedTime
            else:
                # if it's no longer stopped, reset variables
                self._stoppedTime = None
                self._timeStopped = 0

        return self._timeStopped

    def outOfDohyo(self) ->bool:
        return(math.sqrt(self.position[0]*self.position[0]+self.position[2]*self.position[2])>LOSS_DIST)

    def crashed(self):
        vel = self.wb_node.getVelocity()
        posy=self.position[1]
        return(vel[1]>0.8 or posy>0.12)

    def restartController(self):
        self.wb_node.restartController()
