from Homevee.Item.User import User
from Homevee.VoiceAssistant import VoiceAssistant


def user_is_at_home(username, db):
        user = User.load_username_from_db(username, db)
        return user.at_home

def do_voice_command(username, text, user_last_location, location, db, language):
    return VoiceAssistant().do_voice_command(username, text, user_last_location, location, db, language)