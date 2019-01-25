def db_url(engine, user, password, host, port, name):
    if engine.lower() == 'postgres':
        return 'postgres://{user}:{password}@{host}:{port}/{name}'\
            .format(user=user, password=password, host=host, port=port, name=name)
