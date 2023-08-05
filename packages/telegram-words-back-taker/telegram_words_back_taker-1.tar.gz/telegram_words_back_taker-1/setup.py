from setuptools import setup

setup(name='telegram_words_back_taker',
      version='1',
      description='Delete on both sides all of your messages in non-admin chats',
      url='https://github.com/Meeksher/TelegramWordsBackTaker',
      author='Mikhail Solodov',
      author_email='workclock359@gmail.com',
      packages=['telegram_words_back_taker'],
      install_requires=[
          'telethon',
      ],
      zip_safe=False)