from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod, ABCMeta


class PipelineFactory:
    """
        Abstract class for pipeline
    """

    __metaclass__ = ABCMeta


    def __init__(self):
        """
        Empty constructor for now. This is deliberately not marked as abstract, else every
        derived class would be forced to create one.
        """
        pass

    @abstractmethod
    def apply(self, configProperties):
        """

        :return:s
        """

    @abstractmethod
    def getParamMap(self, configProperties, sparkSession):
        """

        :param sparkSession:
        :return:
        """


    def save(self, configProperties, dataframe):
        """
        """
        pass