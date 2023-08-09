import subprocess
import os
def get_git_version():
    try:
        cwd = os.path.dirname(os.path.abspath(__file__))
        print(cwd)
        return subprocess.check_output(['git', 'rev-parse',  'HEAD'],cwd=cwd).decode('ascii').strip()
    except Exception as e:
        print(e)
        return 'unknown'

if __name__ == '__main__':
    print(get_git_version())