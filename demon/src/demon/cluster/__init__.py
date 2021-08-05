"""Cluster interfaces."""

from enum import Enum, unique
from functools import lru_cache

from demon import global_config
from demon.cluster.base import BaseCluster
from demon.cluster.slurm_cluster import SlurmCluster


@unique
class ClusterEnum(Enum):
    """Cluster enum."""

    SLURM = SlurmCluster


@lru_cache()
def get_cluster() -> BaseCluster:
    """Cache and return Cluster object.

    Returns:
        BaseCluster: An instance of a class that inherits BaseCluster
    """
    return ClusterEnum[global_config.Cluster].value()
