from re import findall, compile, S, M ,I

def check(config: dict, log: str):
    """
    This function returns a list of commonly known log issues. See the readme for more info. (Scuffed)
    
    The return type is 'list'.

    """
    remDup = lambda x : list(dict.fromkeys(x))

    issues = []

    for i in config:
        r = compile(i['r'], S | M | I)

        results = findall(r, log)

        if not results:
            continue
        results = remDup(results)

        if not i['smart']:
            issues.append(i["desc"])
            continue

        r = compile(i['smart'], I)

        for j in results:
            smartSearch = findall(r, j)

            if not smartSearch:
                continue

            issues.append(f'{i["desc"]} {smartSearch[0]}')
        continue

    issues = remDup(issues)
    return issues