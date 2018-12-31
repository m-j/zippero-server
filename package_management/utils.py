def fullname(name: str, version: str):
    return f'{name}@{version}'


def parse_fullname(fullname: str):
    if not '@' in fullname:
        raise ValueError(f'"{fullname}" is not proper package fullname')

    [name, version] = fullname.split('@')
    return (name, version)


def package_link(protocol: str, host: str, name: str, version: str):
    return f'{protocol}://{host}/packages/{name}/{version}'