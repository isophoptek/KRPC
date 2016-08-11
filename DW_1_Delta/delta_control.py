# control for DW-1 Delta Experimental Drone


def keep_level_pitch():
        import krpc
        from time import sleep

        conn = krpc.connect(name='keep_level_pitch')
        vessel = conn.space_center.active_vessel
        ref_frame = vessel.surface_reference_frame
        flight = vessel.flight
        ap = vessel.auto_pilot
        ap.reference_frame = vessel.orbital_reference_frame
        vertical_speed = conn.add_stream(getattr, flight(ref_frame), 'vertical_speed')
        pitch_stream = conn.add_stream(getattr, flight(ref_frame), 'pitch')
        ap.target_pitch = 0
        ap.target_roll = 0
        ap.engage()

        try:
            while True:
                if vertical_speed > 0:
                    if pitch_stream() > -5:
                        ap.target_pitch -= 1
                    else:
                        ap.target_pitch += 1
                elif vertical_speed < 0:
                    ap.target_pitch += 1
                sleep(0.01)
        except KeyboardInterrupt:
            print('Interupted')

        ap.disengage()
        vertical_speed.remove()
        conn.close()


def keep_level_throttle(pitch, roll):
        import krpc
        from time import sleep

        conn = krpc.connect(name='keep_level_throttle')
        vessel = conn.space_center.active_vessel
        ref_frame = vessel.surface_reference_frame
        flight = vessel.flight
        ap = vessel.auto_pilot
        ap.reference_frame = vessel.orbital_reference_frame
        vertical_speed = conn.add_stream(getattr, flight(ref_frame), 'vertical_speed')
        ap.target_pitch = pitch
        ap.target_roll = roll
        ap.engage()

        try:
            while True:
                if vertical_speed < 0:
                    vessel.control.throttle += 0.01
                elif vertical_speed > 0:
                    vessel.control.throttle -= 0.01
                sleep(0.01)
        except KeyboardInterrupt:
            print('Interupted')

        ap.disengage()
        vertical_speed.remove()
        conn.close()
