import subprocess

def get_git_version():
    try:
        return subprocess.check_output(['git', 'rev-parse',  'HEAD']).decode('ascii').strip()
    except Exception as e:
        print(e)
        return 'unknown'

if __name__ == '__main__':
    print(get_git_version())