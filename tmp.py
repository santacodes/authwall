from core import AuthWall

a = AuthWall()
a.add('test', 'test', 'ok', '0')
print(a.authenticate('test', 'test'))