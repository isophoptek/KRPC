# Low level control functions


def sectionheader(sectiontitle):
    print('----------------------------------------')
    print(sectiontitle)
    print('----------------------------------------')


def uplink(uplink_name):
    import krpc
    global mc_uplink
    print('connecting to server as ' + str(uplink_name))
    try:
        mc_uplink = krpc.connect(name=str(uplink_name))
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)


def prog():
    import krpc

    print('connecting to server as Control:Prograge')
    try:
        conn_control = krpc.connect(name='Control:Prograde')
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)

    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (0, 1, 0)
    print('Autopilot set to vector: %s' % (ap.target_direction,))
    ap.wait()
    print ('Turn complete, SAS active')
    vessel.auto_pilot.sas = True
    conn_control.close()
    print ('Connection closed.')


def retrog():
    import krpc

    print('connecting to server as Control:Retrograde')
    try:
        conn_control = krpc.connect(name='Control:Retrograde')
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)

#    conn_control = krpc.connect(name='Control:Retrograde')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (0, -1, 0)
    print('Autopilot set to vector: %s' % (ap.target_direction,))
    ap.wait()
    print ('Turn complete, SAS active')
    vessel.auto_pilot.sas = True
    conn_control.close()
    print ('Connection closed.')


def norm():
    import krpc

    print('connecting to server as Control:Normal')
    try:
        conn_control = krpc.connect(name='Control:Normal')
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)

#    conn_control = krpc.connect(name='Control:Normal')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (0, 0, 1)
    print('Autopilot set to vector: %s' % (ap.target_direction,))
    ap.wait()
    print ('Turn complete, SAS active')
    vessel.auto_pilot.sas = True
    conn_control.close()
    print ('Connection closed.')


def antinorm():
    import krpc

    print('connecting to server as Control:AntiNormal')
    try:
        conn_control = krpc.connect(name='Control:AntiNormal')
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)

#    conn_control = krpc.connect(name='Control:AntiNormal')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (0, 0, -1)
    print('Autopilot set to vector: %s' % (ap.target_direction,))
    ap.wait()
    print ('Turn complete, SAS active')
    vessel.auto_pilot.sas = True
    conn_control.close()
    print ('Connection closed.')


def radial():
    import krpc

    print('connecting to server as Control:Radial')
    try:
        conn_control = krpc.connect(name='Control:Radial')
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)

#    conn_control = krpc.connect(name='Control:Radial')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (1, 0, 0)
    print('Autopilot set to vector: %s' % (ap.target_direction,))
    ap.wait()
    print ('Turn complete, SAS active')
    vessel.auto_pilot.sas = True
    conn_control.close()
    print ('Connection closed.')


def antiradial():
    import krpc

    print('connecting to server as Control:AntiRadial')
    try:
        conn_control = krpc.connect(name='Control:AntiRadial')
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)

#    conn_control = krpc.connect(name='Control:AntiRadial')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (-1, 0, 0)
    print('Autopilot set to vector: %s' %(ap.target_direction,))
    ap.wait()
    print ('Turn complete, SAS active')
    vessel.auto_pilot.sas = True
    conn_control.close()
    print ('Connection closed.')


def turnvector(r, g, n):
    import krpc

    print('connecting to server as Control:TurnVector')
    try:
        conn_control = krpc.connect(name='Control:TurnVector')
    except krpc.error.NetworkError:
        print('Connection to server could not be established.')
        print('Check if server is running and accepts connections, accept connection manually if necessary.')
        exit(1)

#    conn_control = krpc.connect(name='Control:TurnVector')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (r, g, n)
    print('Autopilot set to vector: %s' % (ap.target_direction,))
    ap.wait()
    print ('Turn complete, SAS active')
    vessel.auto_pilot.sas = True
    conn_control.close()
    print ('Connection closed.')
