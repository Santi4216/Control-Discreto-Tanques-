"""Pages package - Simplified interface."""
from .simplified_controls import SimplifiedControlsPage
from .timed_sequence import TimedSequencePage
from .discrete_monitor import DiscreteMonitorPage

__all__ = [
    "SimplifiedControlsPage",
    "TimedSequencePage",
    "DiscreteMonitorPage"
]
