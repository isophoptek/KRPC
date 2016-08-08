# Telemetry For KSP


def log_launch(path, interval):

        import krpc
        from time import sleep
        from datetime import timedelta

        try:
            print('Seeking connection, please ensure server is running...')
            conn_log_launch = krpc.connect(name='log_launch')

        except krpc.error.NetworkError as e:
            print('Connection to server could not be established.')
            print('Check if server is running and accepts connections, accept connection manually if necessary.')
            exit(1)

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
        velocity = conn_log_launch.add_stream(getattr, flight(ref_frame), 'velocity')
        atmo_density = conn_log_launch.add_stream(getattr, flight(ref_frame), 'atmosphere_density')
        dynamic_pressure = conn_log_launch.add_stream(getattr, flight(ref_frame), 'dynamic_pressure')
        aerodynamic_force = conn_log_launch.add_stream(getattr, flight(ref_frame), 'aerodynamic_force')
        drag = conn_log_launch.add_stream(getattr, flight(ref_frame), 'drag')
        terminalvelocity = conn_log_launch.add_stream(getattr, flight(ref_frame), 'terminal_velocity')

        fileName = str(vessel.name) + "_Log_Launch.csv"
        outFile = str(path) + str(fileName)

        with open(outFile, mode='a+') as exportFile:
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
            exportFile.write('Velocity,')
            exportFile.write('Atmo density,')
            exportFile.write('Dynamic pressure,')
            exportFile.write('Aerodynamic force,')
            exportFile.write('Drag,')
            exportFile.write('Terminal velocity,')
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
                    "{velocity},"
                    "{atmo_density},"
                    "{dyn_pressure},"
                    "{aero_force},"
                    "{drag},"
                    "{t_velocity},"
                    "\n").format(met=str(timedelta(seconds=int(missionelapsedtime))),
                                 asl=int(meanaltitude()),
                                 ap=int(apoapsis()),
                                 toa=str(timedelta(seconds=int(time_to_ap))),
                                 pe=int(periapsis()),
                                 top=str(timedelta(seconds=int(time_to_pe))),
                                 inc=int(inclination()),
                                 pitch=int(pitch()),
                                 aoa=int(aoa()),
                                 g_Force=int(currentgforce()),
                                 velocity=int(velocity()),
                                 atmo_density=int(atmo_density()),
                                 dyn_pressure=int(dynamic_pressure()),
                                 aero_force=int(aerodynamic_force()),
                                 drag=int(drag()),
                                 t_velocity=int(terminalvelocity()), )
            exportFile.write(line)
            sleep(interval)