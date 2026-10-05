"""Machine-specific locations, in one place. Override with environment variables."""
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
MC = os.environ.get('BM_MC', '/home/claude/mc263') + '/'        # tools/build_ref263.py writes this
