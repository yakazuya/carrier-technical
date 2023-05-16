def national_judgment(key):
    # 4661等の日本株銘柄(int型)なら日本型銘柄用に変換
    if type(key) != str:
        key = str(key) + '.T'
    # .Tが不要になったら取り除く
    elif key.endswith('.T'):
        key = int(key.rstrip('.T'))
    return key