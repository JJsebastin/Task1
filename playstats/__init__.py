"""
playstats
=========
PlayStats - Sports Score Visualizer
Core package exposing all four major components.
"""

from .data_manager import DataManager
from .analytics_engine import AnalyticsEngine
from .visualization_engine import VisualizationEngine
from .cli_controller import CLIController

__all__ = ["DataManager", "AnalyticsEngine", "VisualizationEngine", "CLIController"]
