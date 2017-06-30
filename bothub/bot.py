# -*- coding: utf-8 -*-

from bothub_client.bot import BaseBot
from bothub_client.messages import Message


class Bot(BaseBot):
    """Represent a Bot logic which interacts with a user.

    BaseBot superclass have methods belows:

    * Send message
      * self.send_message(message, user_id=None, channel=None)
    * Data Storage
      * self.set_project_data(data)
      * self.get_project_data()
      * self.set_user_data(data, user_id=None, channel=None)
      * self.get_user_data(user_id=None, channel=None)

    When you omit user_id and channel argument, it regarded as a user
    who triggered a bot.
    """

    def handle_message(self, event, context):
        content = event['content']
        if content.startswith('/'):
            if content == '/start':
                self.send_start_message(event)
            elif content.startswith('/list'):
                self.send_word_list(event)
            return

        self.count_word(content)
        self.search_word(event)

    def send_start_message(self, event):
        message = Message(event).set_text("Hi! I'm a wordbook bot.\n"\
                                          'Enter a word, you gets dictionary URL.\n'\
                                          'You can check search history afterword.')\
                                .add_postback_button('Word list', '/list')
        self.send_message(message)

    def send_word_list(self, event):
        content = event['content']
        splitted = content.split()

        words_to_count = self.get_user_data()
        sorted_list = sorted(words_to_count.items(), key=lambda d: d[1], reverse=True)

        start_pos = int(splitted[1]) if len(splitted) > 1 else 0
        paged_list = sorted_list[start_pos:start_pos+10]
        word_list = '\n'.join([
            '{}, {}'.format(word, count)
            for word, count
            in paged_list
        ])

        has_next = len(paged_list) == 10
        message = Message(event).set_text(word_list)

        if has_next:
            message.add_postback_button('Next list', '/list {}'.format(start_pos+10))
        self.send_message(message)

    def count_word(self, word):
        data = self.get_user_data()
        data.setdefault(word, 0)
        data[word] += 1
        self.set_user_data(data)
        
    def search_word(self, event):
        content = event['content']
        url = 'http://www.ldoceonline.com/dictionary/{}'.format(content)
        message = Message(event).set_text('Lookup a definition')\
                                .add_url_button('{}'.format(content), url)
        self.send_message(message)
