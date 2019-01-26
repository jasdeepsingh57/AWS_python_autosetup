from subprocess import Popen, PIPE

url = open("git.txt", 'r')
url = url.read()

proc = Popen(['git', 'clone', url], stdin=PIPE, stdout=PIPE, stderr=PIPE)

proc.communicate(b'yes\n')
