import soundengine as se


def test_play():
    se.play_file('12922_newgrounds_jermai.mp3')


def test_err():
    try:
        se.loop_file('test.flac', 9999)
    except FileNotFoundError as fnf:
        assert 'Could not find file: test.flac' in str(fnf)


def test_injection():
    try:
        se.loop_file('-evilfunc', 9999)
    except FileNotFoundError as fnf:
        assert 'Could not find file: -evilfunc' in str(fnf)

    try:
        se.play_file('-evilfunc')
    except FileNotFoundError as fnf:
        assert 'Could not find file: -evilfunc' in str(fnf)

    success = False
    try:
        se.loop_file('__init__.py', 'nan')
    except AssertionError as fnf:
        success = True
    assert success
