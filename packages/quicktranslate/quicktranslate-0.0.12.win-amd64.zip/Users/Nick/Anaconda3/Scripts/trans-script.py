#!C:\Users\Nick\Anaconda3\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'quicktranslate==0.0.12','console_scripts','trans'
__requires__ = 'quicktranslate==0.0.12'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('quicktranslate==0.0.12', 'console_scripts', 'trans')()
    )
