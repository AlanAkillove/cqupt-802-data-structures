# -*- coding: utf-8 -*-
"""One-command rebuild of all derived artifacts. Run from repository root:

    python scripts/rebuild_all.py

Order: metadata -> statistics -> coverage/exposure -> validate (QA).
"""
import os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, 'scripts')
STEPS = ['build_metadata.py', 'build_statistics.py', 'build_syllabus_coverage.py', 'validate_repository.py']


def main():
    for s in STEPS:
        print('\n$ python scripts/' + s)
        r = subprocess.run([sys.executable, os.path.join(S, s)], cwd=ROOT)
        if r.returncode not in (0, 1):  # validate returns 1 on FAIL but should still chain report
            print('step failed: ' + s)
            return r.returncode
    print('\nrebuild_all: done')


if __name__ == '__main__':
    main()
