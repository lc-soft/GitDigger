from app import app, db
from flask import url_for
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db, directory='db/migrate')
manager.add_command('db', MigrateCommand)

@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        endpoint = rule.endpoint
        methods = ','.join(rule.methods)
        line = '{:50s} {:20s} {}'.format(endpoint, methods, rule.rule)
        line = urllib.unquote(line)
        output.append(line)
    for line in sorted(output):
        print line

if __name__ == "__main__":
    manager.run()
