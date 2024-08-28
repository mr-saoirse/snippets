from fasthtml.common import Script
from pathlib import Path

def read_main():
    with open(f"{Path(__file__).parent}/editor.js", 'r') as f:
        return f.read()

class EditorJS:
    def __init__(self):
        self.script = Script(code=read_main(), type='module')
    def __ft__(self):
        return self.script
 
        