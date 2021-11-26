"""Cluster registry."""

from typing import Optional

from blackcap.cluster.base import BaseCluster


class ClusterRegistry:
    """Cluster registry."""

    clusters = {}

    def add_cluster(self: "ClusterRegistry", cluster: BaseCluster) -> None:
        """Add custom cluster to registry.

        Args:
            cluster (BaseCluster): Custom cluster implementation
        """
        self.clusters[cluster.CONFIG_KEY_VAL] = cluster

    def get_cluster(self: "ClusterRegistry", cluster: str) -> Optional[BaseCluster]:
        """Get cluster.

        Args:
            cluster (str): Cluster name

        Returns:
            Optional[BaseCluster]: Returns the cluster if found else None
        """
        return self.clusters.get(cluster)
