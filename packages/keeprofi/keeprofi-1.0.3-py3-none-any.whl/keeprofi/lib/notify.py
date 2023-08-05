
import dnotify

server = dnotify.NotifyServer('keeprofi')

def Notify(*args):
	return server.Notify(*args)
