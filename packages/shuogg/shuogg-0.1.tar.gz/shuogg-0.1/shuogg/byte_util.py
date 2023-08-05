import jpype


def to_hex_str(value, byte_size):
    """
    10进制数转16进制字符串
    :param value:
    :param byte_size: 字节数,主要针对负数
    :return:
    """
    jvmPath = jpype.getDefaultJVMPath()
    jpype.startJVM(jvm=jvmPath)
    num2Hex_func = jpype.java.lang.Long.toHexString
    raw_str = num2Hex_func(value)[16 - 2 * byte_size:]
    return '0x' + raw_str.upper()

if __name__ == '__main__':
    print(to_hex_str(-25, 2))
