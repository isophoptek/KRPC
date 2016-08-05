# Low level control functions


def prog():
    import krpc
    conn_control = krpc.connect(name='Control:Prograde')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (0, 1, 0)
    ap.wait()
    conn_control.close()


def retrog():
    import krpc
    conn_control = krpc.connect(name='Control:Retrograde')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (0, -1, 0)
    ap.wait()
    conn_control.close()


def norm():
    import krpc
    conn_control = krpc.connect(name='Control:Normal')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (0, 0, 1)
    ap.wait()
    conn_control.close()


def antinorm():
    import krpc
    conn_control = krpc.connect(name='Control:AntiNormal')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (0, 0, -1)
    ap.wait()
    conn_control.close()


def radial():
    import krpc
    conn_control = krpc.connect(name='Control:Radial')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (1, 0, 0)
    ap.wait()
    conn_control.close()


def antiradial():
    import krpc
    conn_control = krpc.connect(name='Control:AntiRadial')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (-1, 0, 0)
    ap.wait()
    conn_control.close()


def turnvector(r, g, n):
    import krpc
    conn_control = krpc.connect(name='Control:TurnVector')
    vessel = conn_control.space_center.active_vessel
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame
    ap.engage()
    ap.target_direction = (r, g, n)
    ap.wait()
    conn_control.close()
