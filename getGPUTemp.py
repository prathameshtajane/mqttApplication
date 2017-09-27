import sys
import subprocess
from subprocess import call
s2_out=call(["vcgencmd","measure_temp"])
#print(s2_out.split("=")[1].split("'")[0])
print(s2_out)