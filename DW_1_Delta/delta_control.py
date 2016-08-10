# control for DW-1 Delta Experimental Drone


def keep_level_pitch():
        import krpc
        from time import sleep

        conn = krpc.connect(name='keep_level_pitch')
        vessel = conn.space_center.active_vessel
        ref_frame = vessel.surface_reference_frame
        flight = vessel.flight
        ap = vessel.auto_pilot

        vertical_speed = conn.add_stream(getattr, flight(ref_frame), 'vertical_speed')
        ap.target_pitch = 0
        ap.engage()

        try:
            while True:
                if vertical_speed < 0:
                    ap.target_pitch += 1
                elif vertical_speed < 0:
                    ap.target_pitch -= 1
                sleep(0.01)
        except KeyboardInterrupt:
            print('Interupted')

        ap.disengage()
        vertical_speed.remove()
        conn.close()


def keep_level_throttle(pitch):
        import krpc
        from time import sleep

        conn = krpc.connect(name='keep_level_throttle')
        vessel = conn.space_center.active_vessel
        ref_frame = vessel.surface_reference_frame
        flight = vessel.flight
        ap = vessel.auto_pilot
        vertical_speed = conn.add_stream(getattr, flight(ref_frame), 'vertical_speed')
        ap.target_pitch = pitch
        ap.engage()

        try:
            while True:
                if vertical_speed < 0:
                    vessel.control.throttle += 0.1
                elif vertical_speed > 0:
                    vessel.control.throttle -= 0.1
                sleep(0.01)
        except KeyboardInterrupt:
            print('Interupted')

        ap.disengage()
        vertical_speed.remove()
        conn.close()
