import subprocess
import platform
import re

def ping_device(ip_address):
    """
    Executes a single ICMP echo query to determine node availability and round-trip delay metrics.
    Works natively across both Linux and Windows environments.
    """
    is_windows = platform.system().lower() == 'windows'
    param = '-n' if is_windows else '-c'
    timeout_param = '-w' if is_windows else '-W'
    
    # Construct terminal command execution block array
    command = ['ping', param, '1', timeout_param, '1', ip_address]
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Regular expression matrix search to parse latency metrics
        if is_windows:
            match = re.search(r'Average = (\d+)ms', output)
        else:
            match = re.search(r'time=([\d.]+)\s*ms', output)
            
        latency = float(match.group(1)) if match else 1.0
        return 'Online', latency
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return 'Offline', 0.0