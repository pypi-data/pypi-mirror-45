import emoji


def char(character):
    return character in emoji.UNICODE_EMOJI


def string(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False
