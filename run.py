from main import app
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

def make_shell_context():
    return dict(app=app, db=db, NowTable=NowTable, LifeTable=LifeTable, User = User)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":

    manager.run()
    # app.run(host='0.0.0.0', debug=False)


