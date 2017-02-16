# data listing scripts for vessel analysis


def list_parts_by_title():
    # lists all parts (using title attribute) in hierarchy
    import krpc
    conn = krpc.connect()
    vessel = conn.space_center.active_vessel

    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part, depth = stack.pop()
        print('listing parts by title:')
        print(' '*depth, part.title)
        for child in part.children:
            stack.append((child, depth+1))
    conn.close()


def list_parts_by_name():
    # lists all parts (using name attribute) in hierarchy
    import krpc
    conn = krpc.connect()
    vessel = conn.space_center.active_vessel

    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part, depth = stack.pop()
        print('listing parts by name:')
        print(' '*depth, part.name)
        for child in part.children:
            stack.append((child, depth+1))
    conn.close()


def list_parts_by_tag():
    # lists all parts (using tag attribute) in hierarchy
    import krpc
    conn = krpc.connect()
    vessel = conn.space_center.active_vessel

    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part, depth = stack.pop()
        print('listing parts by tag:')
        print(' '*depth, part.tag)
        for child in part.children:
            stack.append((child, depth+1))
    conn.close()


def list_parts_with_stage():
    # lists all parts (using tag title) in hierarchy with additional stageing info
    import krpc
    conn = krpc.connect()
    vessel = conn.space_center.active_vessel

    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part, depth = stack.pop()
        print('listing parts (title, stage, decouple_stage):')
        print(' '*depth, part.title, part.stage, part.decouple_stage)
        for child in part.children:
            stack.append((child, depth+1))
    conn.close()


def list_parts_with_modules():
    # lists all parts (using tag title) in hierarchy with additional module info
    import krpc
    conn = krpc.connect()
    vessel = conn.space_center.active_vessel

    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part, depth = stack.pop()
        print('listing parts (title, modules):')
        print(' '*depth, part.title, part.modules)
        for child in part.children:
            stack.append((child, depth+1))
    conn.close()


def list_engines():
    # list all engines
    import krpc
    conn = krpc.connect()
    vessel = conn.space_center.active_vessel

    list = vessel.parts.engines
    while len(list) > 0:
        part = list.pop()
        print(part.title, part.stage, part.decouple_stage)
    conn.close()


def list_resources():
    # list resources
    import krpc
    conn = krpc.connect()
    vessel = conn.space_center.active_vessel

    list = vessel.resources
    name_list = list.names
    for name in name_list:
        resource_amount = list.amount(name)
        resource_max = list.max(name)
        print('{}:{}/{}').format(name, resource_amount, resource_max)
    conn.close()
