"""Observer to fetch metrcis from a central monitoring system."""

from blackcap.observer.elastic_observer import ElasticObserver
from blackcap.observer.registry import ObserverRegistry


observer_registry = ObserverRegistry()
observer_registry.add_observer(ElasticObserver())
