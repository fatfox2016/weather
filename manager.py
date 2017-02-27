from main import app
from flask_script import Manager,Shell,Server
from flask_bootstrap import Bootstrap
from flask_moment import Moment

bootstrap = Bootstrap(app)
moment = Moment(app)

server = Server(host="0.0.0.0",port=80)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, NowTable=NowTable, LifeTable=LifeTable, User = User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver",Server())

if __name__ == "__main__":

    manager.run()
    # app.run(host='0.0.0.0', debug=False)


