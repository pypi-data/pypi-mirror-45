from telethon import functions, types
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, ChatForbidden, ChannelForbidden, Channel, Chat

api_id = 0
api_hash = ''
username = ''
phone = ''

def check_auth(client):
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

def create_client():
    client = TelegramClient(username, api_id, api_hash)
    client.connect()
    check_auth(client)
    return client

def get_my_chats_and_channels(client):
    print("Getting chats-list..")
    get_dialogs = GetDialogsRequest(offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=30,
        hash = 0)
    
    print("Got.")
    return client(get_dialogs).chats

def delete_my_messages(client, chat):
    msgs = client.get_messages(entity=chat, from_user="me")
    return client.delete_messages(chat, msgs, revoke=True)


def main():
    print("Open Telegram session..")
    client = create_client()
    print("Opened.")

    for dialog in get_my_chats_and_channels(client):
        if not ((isinstance(dialog, Channel) and dialog.megagroup) or isinstance(dialog, Chat)):
            continue
        
        if dialog.admin_rights or dialog.creator:
            continue

        deleted_msgs = delete_my_messages(client, dialog)
        if len(deleted_msgs) != 0 and deleted_msgs[0].pts_count > 0:
            print(dialog.title, ": deleted ", deleted_msgs[0].pts_count, " messages")
        
    print("Deletion completed.")

try:
    main()
except Exception as e:
    print(e)
