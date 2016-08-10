# Telemetry For KSP

# Requies FAR


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
                    "{t_isp},"
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
                                 t_isp=int(thrust_specific_fuel_consumption()), )
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
    from math import radians

    conn = krpc.connect(name='Telemetry')
    vessel = conn.space_center.active_vessel
    ref_frame = vessel.surface_reference_frame
    ref_frame_vel = vessel.orbit.body.reference_frame
    ref_frame_orbit = vessel.orbital_reference_frame
    flight = vessel.flight
    orbit = vessel.orbit
    display = conn.ui.add_canvas()
    display.add_text('Telemetry log active')

    # add streams
    missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
    meanaltitude = conn.add_stream(getattr, flight(ref_frame), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
    time_to_ap = conn.add_stream(getattr, orbit, 'time_to_apoapsis')
    periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')
    time_to_pe = conn.add_stream(getattr, orbit, 'time_to_periapsis')
    inclination = conn.add_stream(getattr, orbit, 'inclination')
    speed = conn.add_stream(getattr, flight(ref_frame_vel), 'speed')
    pitch = conn.add_stream(getattr, flight(ref_frame), 'pitch')
    aoa = conn.add_stream(getattr, flight(ref_frame), 'angle_of_attack')
    sideslip = conn.add_stream(getattr, flight(ref_frame), 'sideslip_angle')
    temp_stat = conn.add_stream(getattr, flight(ref_frame), 'static_air_temperature')
    stall_fraction = conn.add_stream(getattr, flight(ref_frame), 'stall_fraction')
    drag_coefficient = conn.add_stream(getattr, flight(ref_frame_orbit), 'drag_coefficient')
    lift_coefficient = conn.add_stream(getattr, flight(ref_frame_orbit), 'lift_coefficient')
    atmo_density = conn.add_stream(getattr, flight(ref_frame), 'atmosphere_density')
    dynamic_pressure = conn.add_stream(getattr, flight(ref_frame), 'dynamic_pressure')
    mass = conn.add_stream(getattr, vessel, 'mass')
    dry_mass = conn.add_stream(getattr, vessel, 'dry_mass')

    # open file for write

    path = 'D:/PyCharm/'
    filename = str(vessel.name) + "_Telemetry.csv"
    filename = str(path) + str(filename)

    # add header

    try:

        with open(filename, mode='a+') as exportFile:
            exportFile.write('MET;')
            exportFile.write('ASL;')
            exportFile.write('Ap;')
            exportFile.write('ToA;')
            exportFile.write('Pe;')
            exportFile.write('ToP;')
            exportFile.write('Inc;')
            exportFile.write('Speed;')
            exportFile.write('Pitch;')
            exportFile.write('AoA;')
            exportFile.write('Sideslip;')
            exportFile.write('Static temp;')
            exportFile.write('Stall;')
            exportFile.write('Drag;')
            exportFile.write('Lift;')
            exportFile.write('Atmospheric Density;')
            exportFile.write('Dynamic Pressure;')
            exportFile.write('Mass;')
            exportFile.write('Dry mass;')
            exportFile.write(';')
            exportFile.write("\n")

        while True:
            line = ("{met};"
                    "{asl};"
                    "{ap};"
                    "{toa};"
                    "{pe};"
                    "{top};"
                    "{inc};"
                    "{speed};"
                    "{pitch};"
                    "{aoa};"
                    "{sideslip};"
                    "{static_temp};"
                    "{stall};"
                    "{drag};"
                    "{lift};"
                    "{atmo_density};"
                    "{dyn_pressure};"
                    "{mass};"
                    "{dry_mass};"
                    "\n").format(met=str(timedelta(seconds=int(missionelapsedtime()))),
                                 asl=int(meanaltitude()),
                                 ap=int(apoapsis()),
                                 toa=str(timedelta(seconds=int(time_to_ap()))),
                                 pe=int(periapsis()),
                                 top=str(timedelta(seconds=int(time_to_pe()))),
                                 inc=radians(int(inclination())),
                                 speed=int(speed()),
                                 pitch=int(pitch()),
                                 aoa=int(aoa()),
                                 sideslip=int(sideslip()),
                                 static_temp=int(temp_stat()),
                                 stall=stall_fraction(),
                                 drag=drag_coefficient(),
                                 lift=lift_coefficient(),
                                 atmo_density=atmo_density(),
                                 dyn_pressure=int(dynamic_pressure()),
                                 mass=int(mass()),
                                 dry_mass=int(dry_mass()),)
            with open(filename, mode='a+') as exportFile:
                exportFile.write(line)

            sleep(1)
    except KeyboardInterrupt:
        print('Telementry stream interupted by user.')

    # remove streams
    missionelapsedtime.remove()
    meanaltitude.remove()
    apoapsis.remove()
    time_to_ap.remove()
    periapsis.remove()
    time_to_pe.remove()
    inclination.remove()
    speed.remove()
    pitch.remove()
    aoa.remove()
    sideslip.remove()
    temp_stat.remove()
    stall_fraction.remove()
    drag_coefficient.remove()
    lift_coefficient.remove()
    mass.remove()
    dry_mass.remove()
    display.remove()
    conn.close()
