#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main entry point for the general chat service with multiple character support.
"""

import sys
import os
# Add the src directory to the Python path to properly import modules
sys.path.append(os.path.join(os.path.dirname(__file__)))

from service.general_chat_service import run_server

if __name__ == "__main__":
    run_server()