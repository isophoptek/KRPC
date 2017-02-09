# Hodur Vessel Procedures Library


def deorbit():

    import krpc
    from time import sleep

# Connection

    try:
        print('Connecting to server as: Emergency Deorbit')
        conn = krpc.connect(name='Emergency Deorbit')
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)

    vessel = conn.space_center.active_vessel
    control = vessel.control
    ref_frame = vessel.surface_reference_frame
    flight = vessel.flight
    orbit = vessel.orbit
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
    periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')

    # turn to retrograde

    ap.sas_mode = 'retrograde'
    ap.engage()

    countdown = 15
    while countdown > 0:
        print countdown
        sleep(1)
    # try main engine
    # search for and activate main engine, deactivate other
    part_list = vessel.parts.with_tag('Main_Engine')
    for item in part_list:
        item.active = True
    part_list = vessel.parts.with_tag('Backup_Engine')
    for item in part_list:
        item.active = False
    part_list = vessel.parts.with_tag('Emergency_Engine')
    for item in part_list:
        item.active = False

    if vessel.available_thrust != 0:
        # activate main engine
        while apoapsis > 30000 or periapsis > 30000:
            control.throttle = 1
        control.throttle = 0
    else: # try backup engine
        # search for and activate backup engines, deactivate other
        part_list = vessel.parts.with_tag('Main_Engine')
        for item in part_list:
            item.active = False
        part_list = vessel.parts.with_tag('Backup_Engine')
        for item in part_list:
            item.active = True
        part_list = vessel.parts.with_tag('Emergency_Engine')
        for item in part_list:
            item.active = False

        if vessel.available_thrust != 0:
            # activate backup engine
            while apoapsis > 30000 or periapsis > 30000:
                control.throttle = 1
            control.throttle = 0
        else: # try emergency RCS
            # search for and activate emergency RCS engines, deactivate other
            part_list = vessel.parts.with_tag('Main_Engine')
            for item in part_list:
                item.active = False
            part_list = vessel.parts.with_tag('Backup_Engine')
            for item in part_list:
                item.active = False
            part_list = vessel.parts.with_tag('Emergency_Engine')
            for item in part_list:
                item.active = True

            if vessel.available_thrust != 0:
                # activate emergency RCS engine
                while apoapsis > 30000 or periapsis > 30000:
                    control.throttle = 1
                control.throttle = 0
    # burn until ap or pe less then 30km

    # decouple capsule, wait, separation burn (retrograde)


