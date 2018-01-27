# -*- coding: utf-8 -*-

from bothub_client.bot import BaseBot
from bothub_client.messages import Message
from bothub_client.decorators import command


class Bot(BaseBot):
    def on_default(self, event, context):
        content = event['content']
        self.count_word(content)
        self.search_word(event)

    @command('start')
    def send_start_message(self, event, context, args):
        message = Message(event).set_text("Hi! I'm a wordbook bot.\n"\
                                          'Enter a word, you gets dictionary URL.\n'\
                                          'You can check search history afterword.')\
                                .add_postback_button('Word list', '/list')
        self.send_message(message)

    @command('list')
    def send_word_list(self, event, context, args):
        content = event['content']

        words_to_count = self.get_user_data()
        sorted_list = sorted(words_to_count.items(), key=lambda d: d[1], reverse=True)

        start_pos = int(args[1]) if len(args) > 1 else 0
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
