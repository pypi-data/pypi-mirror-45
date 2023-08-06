import soundengine as se


def test_play():
    se.play_file('12922_newgrounds_jermai.mp3')


def test_err():
    se.loop_file('test.flac', 9999)
    err = None
    while err is None:
        err = se.SoundErrorPub.get_data()
    print(err)
