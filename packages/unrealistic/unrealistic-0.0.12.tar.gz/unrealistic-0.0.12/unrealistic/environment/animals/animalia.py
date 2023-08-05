from abc import ABC,abstractmethod
class Animal(ABC):

    def __init__(self,age=0):
        self._age=age
        
    @abstractmethod
    def move(self):
        """All animals can move"""

    @property
    def age(self):
        return self._age
    @age.setter
    def age(self,value):
        self._age=value

