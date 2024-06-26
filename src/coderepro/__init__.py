"""
coderepro: An LLM tool for evaluating reproducibility of research code. 
"""

from __future__ import annotations

from importlib.metadata import version

__all__ = ("__version__",)
__version__ = version(__name__)
