
def long_to_mac(value, connector='-'):
    raw_mac = hex(value)[2:].zfill(12).upper()
    ret_mac = ''
    for char, index in zip(raw_mac, range(len(raw_mac))):
        ret_mac += char
        if index & 1 == 1:
            ret_mac += connector
    return ret_mac[:-1]


if __name__ == '__main__':
    print(long_to_mac(19929521329))
