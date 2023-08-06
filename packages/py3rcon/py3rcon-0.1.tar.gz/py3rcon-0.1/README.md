# pyRcon
Python3 RCON API for Python3
Built and tested for Quake3, but will work with most RCON systems.

## Installation:

`$ pip install pyrcon`

## Examples:

Send RCON commands without waiting for a response:
```python
from pyrcon import RCON

rcon = RCON("127.0.0.1", "secret_password") 
rcon.send_command("say Hello, world!")
```

Send RCON commands and get their response:
```python
from pyrcon import RCON

rcon = RCON("127.0.0.1", "secret_password")
status = rcon.send_command("status", response=True, port=27960) #port is optional
print(status)
```
