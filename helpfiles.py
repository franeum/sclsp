#!/usr/bin/env python3

from pathlib import Path

p = Path('/home/neum/.local/share/SuperCollider/Help')

def iterate_html(path):
    for item in Path.iterdir(path):
        
    