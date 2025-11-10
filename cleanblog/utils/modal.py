
class Modal(object):
    __instance = None

    def __new__(cls, request):
        if cls.__instance is None:
            cls.__instance = super(Modal, cls).__new__(cls)
        cls.request = request
        return cls.__instance
    
    def create_message(self, request, message):
        request.session['open_modal'] = True
        request.session['message'] = message

    
        