"""Cluster interfaces."""


from blackcap.cluster.registry import ClusterRegistry
from blackcap.cluster.slurm_cluster import SlurmCluster


cluster_registry = ClusterRegistry()
cluster_registry.add_cluster(SlurmCluster())
