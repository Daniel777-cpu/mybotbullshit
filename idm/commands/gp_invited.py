from ..objects import dp, Event
from microvk import VkApiResponseException
from time import sleep

@dp.event_register('groupbots.invited')
def groupbots(event: Event) -> str:
    group_id = 0 - int(event.obj['group_id'])
    for item in event.api("messages.getConversations", count=100, filter="all")['items']:
        conv = item['conversation']
        if conv['peer']['type'] == "chat":
            sleep(0.3)
            for msg in event.api('messages.getHistory', peer_id = conv['peer']['id'])['items']:
                if msg['conversation_message_id'] == event.msg['conversation_message_id']:
                    if msg.get('action', {}).get('member_id') == group_id:
                        peer_id = msg['peer_id']
                        break
    msg_id = event.api.msg_op(1, peer_id, '👀 Обнаружена группа Ириса, пытаюсь выдать админку...')
    try:
        if event.api('messages.setMemberRole', peer_id = peer_id,
                     member_id = group_id, role = 'admin') == 1:
            event.api.msg_op(2, peer_id, '✅ Ириска назначен администратором беседы', msg_id)
    except VkApiResponseException as e:
        if e.error_code == 15:
            event.api.msg_op(2, peer_id, '❗ Не получилось назначить группу администратором.\nСкорее всего это либо чат сообщества, либо у меня нет прав для назначения администраторов', msg_id)
        else:
            event.api.msg_op(2, peer_id, f'❗ Ошибка VK: {e.error_msg}', msg_id)
    return "ok"