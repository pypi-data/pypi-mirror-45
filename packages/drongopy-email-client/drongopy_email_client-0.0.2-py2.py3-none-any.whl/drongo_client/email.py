from drongo.client import DrongoClient


class EmailClient(DrongoClient):
    def __init__(self, *args, **kwargs):
        super(EmailClient, self).__init__(*args, **kwargs)
        self._ns = 'core'
        self._instance = None

    def set_namespace(self, ns):
        self._ns = ns

    def set_instance(self, instance):
        self._instance = instance

    def send_email(self, email_from, email_to, subject,
                   message_text=None, message_html=None):
        url = '/{ns}/email/{instance}/send'.format(
            ns=self._ns, instance=self._instance)
        data = {
            'email_from': email_from,
            'email_to': email_to,
            'subject': subject,
            'message_text': message_text,
            'message_html': message_html
        }
        response = self.post_json(url, data)

        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])
