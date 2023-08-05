"""
Holds ip and port per session
"""
import threading



class SipSessionTable:
    def __init__(self):
        self.session_table = {}

    def get_session(self, session_identifier):
        try:
            return self.session_table[session_identifier]
        except:
            return False

    def set_session(self,session_identifier):
        pass

    def is_session(self):
        pass



class Session:

    def __init__(self,app=None):
        pass

    def send(self):
        pass

    def recv(self):
        pass