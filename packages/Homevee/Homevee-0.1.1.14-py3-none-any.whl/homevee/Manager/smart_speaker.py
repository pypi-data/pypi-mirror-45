from homevee.Helper.helper_functions import has_permission
from homevee.items.Room import Room


def get_smart_speakers(username, db):
    speakers =[]

    with db:
        cur = db.cursor()

        cur.execute("SELECT * FROM SMART_SPEAKER ORDER BY LOCATION ASC")

        for speaker in cur.fetchall():
            if has_permission(username, speaker['LOCATION'], db):
                item = {'name': speaker['NAME'], 'id': speaker['ID'], 'key': speaker['KEY'],
                        'location': speaker['LOCATION'], 'location_name': Room.get_name_by_id(speaker['LOCATION'], db)}

                speakers.append(item)

    return {'speakers': speakers}

def add_edit_smart_speaker(username, db):
    return