import aiocron
from datetime import datetime

from loader import pg
from handlers.notify import notify


@aiocron.crontab('* * * * *', start=False)
async def check_reminders():
    current_time = datetime.now().replace(second=0, microsecond=0)

    query = """ SELECT * FROM notes WHERE reminder_time = $1; """
    notes = await pg.execute(query, current_time, fetch=True)

    for note in notes:
        user_id = note['owner_id']
        note_id = note['id']
        note_title = note['note_title']
        note_text = note['note_text']

        await notify(user_id, note_id, note_title, note_text)
