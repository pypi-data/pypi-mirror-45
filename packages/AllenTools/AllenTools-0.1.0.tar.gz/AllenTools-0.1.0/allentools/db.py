def row2dict(row, not_include=None, **kwargs):
    r = {}
    not_include = not_include if not_include else []
    for c in row.__table__.columns:
        if c.name not in not_include:
            r[c.name] = str(getattr(row, c.name))
    return {**r, **kwargs}

def commit_anyway(session, max_try=10):
    success = False
    try_time = 0
    while True:
        if success:
            return True
        if try_time > max_try:
            return False
        try:
            try_time += 1
            session.commit()
            success = True
        except:
            session.rollback()