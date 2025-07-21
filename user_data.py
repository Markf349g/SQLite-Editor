import json
from typing import Any

def AutoReload() -> str:
  data: Any = ''
  with open('config.json', 'r') as file:
    data = json.load(file)
  return data['settings']['auto_reload']

def StyleDefine() -> str:
  data: Any = ''
  with open('config.json', 'r') as file:
    data = json.load(file)
  return data['settings']['style']
