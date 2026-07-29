"""
Sports_visualizer.py
=====================
PlayStats – Sports Score Visualizer
Entry point for the application.

Usage:
    python Sports_visualizer.py

Dependencies:
    pip install pandas matplotlib
"""

from playstats import CLIController


if __name__ == "__main__":
    controller = CLIController()
    controller.main_menu()
