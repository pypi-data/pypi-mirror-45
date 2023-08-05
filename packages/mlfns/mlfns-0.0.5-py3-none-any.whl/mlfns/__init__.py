"""
Machine Learning utilities module for Python
============================================

Python utility functions to reduce repeatable codes.
"""
import sys
import re
import warnings
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

# Make sure that DeprecationWarning within this package always gets printed
warnings.filterwarnings('always', category=DeprecationWarning,
                        module=r'^{0}\.'.format(re.escape(__name__)))
                        
__all__ = ['train', 'evaluate', 'plot']