from abc import abstractmethod, ABC


class DBSpec(ABC):

    @property
    @abstractmethod
    def num_trajectories(self) -> int:
        pass

    @abstractmethod
    def push_trajectory(self, trajectory):
        pass

    @abstractmethod
    def get_trajectory(self, index=None):
        pass

    @abstractmethod
    def dump_weights(self, weights, prefix):
        pass

    @abstractmethod
    def load_weights(self, prefix):
        pass
