"""
Holds ip and port per session
"""

from multiprocessing import Process , Queue

from Katari.logging import KatariLogging



class SipSessionTable:
    def __init__(self):
        self.session_table = {}

    def get_session(self, session_identifier):
        try:
            return self.session_table[session_identifier]
        except:
            return False

    def set_session(self,session_identifier,app):
        """

        :param session_identifier:
        :param app:
        :return:
        """
        q1, q2 = self.create_queues()
        queue_storage = {"send": None , "recv": None}
        self.session_table[session_identifier] = queue_storage
        self.session_table[session_identifier]['send'] = q1
        self.session_table[session_identifier]['recv'] = q2
        app.set_queues(q1,q2)
        app_thread = Process(target=app._server_run)
        app_thread.start()


    def is_session(self,session_identifier):
        try:
            self.session_table[session_identifier]
            return True
        except:
            return False

    def create_queues(self):
        q1 = Queue()
        q2 = Queue()
        return q1 ,q2

    def session_recv(self,session_identifier,message):
        self.session_table[session_identifier]['recv'].put(message)

    def session_send(self,session_identifier):
        self.session_table[session_identifier]['send'].get()
