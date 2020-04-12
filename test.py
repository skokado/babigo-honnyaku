from app.views import babinize


def test_babinize():
    # Simple
    assert babinize('こんにちは') == 'こぼんぶにびちびはば'
    assert babinize('コンニチハ') == 'コボンブニビチビハバ'
    
    # 変換対象に「ば行」を含む
    assert babinize('かば') == 'かばばば'
    assert babinize('バンド') == 'ババンブドボ'

    # 拗音(ようおん)を含む
    assert babinize('きょう') == 'きょぼうぶ'

    # 変換モードを変更
    assert babinize('きょう', mode='hira') == 'きょぼうぶ'
    assert babinize('きょう', mode='kata') == 'きょボうブ'
