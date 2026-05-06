
#!/usr/bin/env python3
"""运行A股数据更新"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from fetch_real_data import main

if __name__ == "__main__":
    main()

