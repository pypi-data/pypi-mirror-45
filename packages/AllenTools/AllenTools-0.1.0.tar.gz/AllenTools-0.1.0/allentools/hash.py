import hashlib

def md5(s):
    """
    返回字符串的md5值
    """
    if type(s) is not bytes:
        s = s.encode()
    h = hashlib.md5()
    h.update(s)
    return h.hexdigest()

def check_info_by_md5(new_info, old_info):
    """
    通过md5摘要对比两段info是否相同
    :param new_info:
    :param old_info:
    :return: 不同为False 相同为True
    """
    if len(new_info) != len(old_info):
        return False
    h = hashlib.md5()
    h.update(new_info.encode("utf-8"))
    new_digest = h.hexdigest()
    h.update(old_info.encode("utf-8"))
    old_digest = h.hexdigest()
    return new_digest == old_digest

