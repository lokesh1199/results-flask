from app import app as application
import sys

if __name__ == '__main__':
    app.run()

activate_this = '/path/to/env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
sys.path.insert(0, 'C:/changethis')

