# Telemetry For KSP


def log_launch(path, interval):

        import krpc
        from time import sleep
        from datetime import timedelta
        from math import radians

        print('Seeking connection, please ensure server is running...')
        conn_log_launch = krpc.connect(name='log_launch')

        vessel = conn_log_launch.space_center.active_vessel
        ref_frame = vessel.surface_reference_frame
        orbit = vessel.orbit
        flight = vessel.flight

        print('Output path:')
        print(path)
        print('Polling interval:')
        print(interval)

        # add streams
        missionelapsedtime = conn_log_launch.add_stream(getattr, vessel, 'met')
        meanaltitude = conn_log_launch.add_stream(getattr, flight(ref_frame), 'mean_altitude')
        apoapsis = conn_log_launch.add_stream(getattr, orbit, 'apoapsis_altitude')
        time_to_ap = conn_log_launch.add_stream(getattr, orbit, 'time_to_apoapsis')
        periapsis = conn_log_launch.add_stream(getattr, orbit, 'periapsis_altitude')
        time_to_pe = conn_log_launch.add_stream(getattr, orbit, 'time_to_periapsis')
        inclination = conn_log_launch.add_stream(getattr, orbit, 'inclination')
        pitch = conn_log_launch.add_stream(getattr, flight(ref_frame), 'pitch')
        aoa = conn_log_launch.add_stream(getattr, flight(ref_frame), 'angle_of_attack')
        currentgforce = conn_log_launch.add_stream(getattr, flight(ref_frame), 'g_force')
        speed = conn_log_launch.add_stream(getattr, flight(ref_frame), 'speed')
        atmo_density = conn_log_launch.add_stream(getattr, flight(ref_frame), 'atmosphere_density')
        dynamic_pressure = conn_log_launch.add_stream(getattr, flight(ref_frame), 'dynamic_pressure')
        drag = conn_log_launch.add_stream(getattr, flight(ref_frame), 'drag_coefficient')
        thrust_specific_fuel_consumption = conn_log_launch.add_stream(getattr, flight(ref_frame),
                                                                      'thrust_specific_fuel_consumption')

        filename = str(vessel.name) + "_Log_Launch.csv"
        filename = str(path) + str(filename)
        print('Generated output path:')
        print(filename)

        with open(filename, mode='a+') as exportFile:
            exportFile.write('MET,')
            exportFile.write('ASL,')
            exportFile.write('Ap,')
            exportFile.write('ToA,')
            exportFile.write('Pe,')
            exportFile.write('ToP,')
            exportFile.write('Inc,')
            exportFile.write('Pitch,')
            exportFile.write('AoA,')
            exportFile.write('G Force,')
            exportFile.write('Speed,')
            exportFile.write('Atmo density,')
            exportFile.write('Dynamic pressure,')
            exportFile.write('Drag,')
            exportFile.write('thrust_specific_fuel_consumption,')
            exportFile.write("\n")

        while True:
            line = ("{met},"
                    "{asl},"
                    "{ap},"
                    "{toa},"
                    "{pe},"
                    "{top},"
                    "{inc},"
                    "{pitch},"
                    "{aoa},"
                    "{g_Force},"
                    "{speed},"
                    "{atmo_density},"
                    "{dyn_pressure},"
                    "{drag},"
                    "{t_velocity},"
                    "\n").format(met=str(timedelta(seconds=int(missionelapsedtime))),
                                 asl=int(meanaltitude()),
                                 ap=int(apoapsis()),
                                 toa=str(timedelta(seconds=int(time_to_ap))),
                                 pe=int(periapsis()),
                                 top=str(timedelta(seconds=int(time_to_pe))),
                                 inc=radians(int(inclination())),
                                 pitch=int(pitch()),
                                 aoa=int(aoa()),
                                 g_Force=int(currentgforce()),
                                 speed=int(speed()),
                                 atmo_density=int(atmo_density()),
                                 dyn_pressure=int(dynamic_pressure()),
                                 drag=int(drag()),
                                 t_velocity=int(thrust_specific_fuel_consumption()), )
            exportFile.write(line)
            sleep(interval)

        exportFile.close()

        missionelapsedtime.remove()
        meanaltitude.remove()
        apoapsis.remove()
        time_to_ap.remove()
        periapsis.remove()
        time_to_pe.remove()
        inclination.remove()
        pitch.remove()
        aoa.remove()
        currentgforce.remove()
        speed.remove()
        atmo_density.remove()
        dynamic_pressure.remove()
        drag.remove()
        thrust_specific_fuel_consumption.remove()
        conn_log_launch.close()


def delta_drone():

    import os
    import krpc
    from time import sleep
    from datetime import timedelta

    conn = krpc.connect(name='Telemetry')
    vessel = conn.space_center.active_vessel
    ref_frame = vessel.surface_reference_frame
    flight = vessel.flight
    orbit = vessel.orbit

    # add streams
    missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
    meanaltitude = conn.add_stream(getattr, flight(ref_frame), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
    time_to_ap = conn.add_stream(getattr, orbit, 'time_to_apoapsis')
    periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')
    time_to_pe = conn.add_stream(getattr, orbit, 'time_to_periapsis')
    inclination = conn.add_stream(getattr, orbit, 'inclination')
    pitch = conn.add_stream(getattr, flight(ref_frame), 'pitch')
    aoa = conn.add_stream(getattr, flight(ref_frame), 'angle_of_attack')
    sideslip = conn.add_stream(getattr, flight(ref_frame), 'sideslip_angle')
    temp_stat = conn.add_stream(getattr, flight(ref_frame), 'static_air_temperature')
    stall_fraction = conn.add_stream(getattr, flight(ref_frame), 'stall_fraction')
    drag_coefficient = conn.add_stream(getattr, flight(ref_frame), 'drag_coefficient')
    lift_coefficient = conn.add_stream(getattr, flight(ref_frame), 'lift_coefficient')

    while True:
        os.system('cls')
        print('MET:' + str(timedelta(seconds=int(missionelapsedtime()))))
        print('ASL:' + str(meanaltitude()))
        print('Ap:' + str(apoapsis()))
        print('Time to Ap:' + str(timedelta(seconds=int(time_to_ap()))))
        print('Pe:' + str(periapsis()))
        print('Time to Pe:' + str(timedelta(seconds=int(time_to_pe()))))
        print('Inc:' + str(inclination()))
        print('Pitch:' + str(pitch()))
        print('AoA:' + str(aoa()))
        print('Sideslip:' + str(sideslip()))
        print('Static temp:' + str(temp_stat()))
        print('Stall:' + str(stall_fraction()))
        print('Drag:' + str(drag_coefficient()))
        print('Lift:' + str(lift_coefficient()))
        sleep(1)
