"""Run inside the OS network sandbox: verify denial, then run cached scenarios."""
import socket,runpy
from pathlib import Path
try:
 with socket.create_connection(('1.1.1.1',443),timeout=2):pass
except PermissionError as e:print('PASS: OS denied network connection:',e,flush=True)
except OSError as e:raise RuntimeError('Network failed but OS permission denial was not proven') from e
else:raise RuntimeError('Network access is still enabled')
runpy.run_path(str(Path(__file__).with_name('offline_demo.py')),run_name='__main__')
