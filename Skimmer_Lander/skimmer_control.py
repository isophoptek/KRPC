def ascend_to_ap(target_ap):
    import krpc

    conn = krpc.connect(name='ascend_procedure')
    vessel = conn.space_center.active_vessel
    orbit = vessel.orbit
    ref_frame = vessel.surface_reference_frame
    ref_frame_vel = vessel.orbit.body.reference_frame
    ref_frame_orbit = vessel.orbital_reference_frame
    flight = vessel.flight

    ground_clearance_altitude = 500
    ap_vector_clearance_altitude = 750

    meanaltitude = conn.add_stream(getattr, flight(ref_frame), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
    time_to_ap = conn.add_stream(getattr, orbit, 'time_to_apoapsis')
    speed = conn.add_stream(getattr, flight(ref_frame_vel), 'speed')

    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbital_reference_frame