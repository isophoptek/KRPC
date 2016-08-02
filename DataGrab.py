# DataGrabber for KSP

# (C) Snieder Marton

import krpc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path fox export")
parser.add_argument("-n", "--polls", help="Number of polls", type=int, default=1)
args = parser.parse_args()

# argument interpretation

num_of_polls = args.polls
outFile = args.path

# connect to server
try:
    print('Connecting to server...')
    conn = krpc.connect(name='DataGrab')

except krpc.error.NetworkError as e:
    print('Connection to server could not be established.')
    print('Check if server is running and accepts connections, accept connection manually if necessary.')
    exit(1)

# create data streams

vessel = conn.space_center.active_vessel
orbit = vessel.orbit
flight = vessel.flight
apoapsis = conn.add_stream(getattr, orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, orbit, 'periapsis_altitude')
currentbody = conn.add_stream(getattr, orbit, 'body')
inclination = conn.add_stream(getattr, orbit, 'inclination')
missionelapsedtime = conn.add_stream(getattr, vessel, 'met')
currentgforce = conn.add_stream(getattr, flight, 'g_force')
meanaltitude = conn.add_stream(getattr, flight, 'mean_altitude')
terminalvelocity = conn.add_stream(getattr, flight, 'terminal_velocity')

# export file definition

if num_of_polls == 1:
    fileName = "SinglePoll_" + str(vessel.name) + "_" + str(vessel.situation) + "_" + str(missionelapsedtime) + ".csv"
else:
    fileName = "PollLog_" + str(vessel.name) + "_" + str(missionelapsedtime) + ".csv"

outFile += fileName

# poll loop

poll = 0
with open(outFile) as exportFile:
    exportFile.write("UT",
                     "MET",
                     "Current Body",
                     "Apoapsis",
                     "Periapsis",
                     "Inclination",
                     "MeanAltitude",
                     "G Force",
                     "Terminal Velocity",
                     "TWR",
                     "Stage dV",
                     "Total dV",
                     "/n")

while poll < num_of_polls:
    # TODO calculate current stage and total deltaV
    line = ("{ut},"
            "{met},"
            "{body},"
            "{apo},"
            "{peri},"
            "{inc},"
            "{mean_alt},"
            "{gforce},"
            "{vt},"
            "{twr},"
            "{stagedv},"
            "{totaldv},"
            "/n").format(ut=conn.space_center.ut,
                         met=missionelapsedtime,
                         body=currentbody,
                         apo=apoapsis,
                         peri=periapsis,
                         inc=inclination,
                         mean_alt=meanaltitude,
                         gforce=currentgforce,
                         vt=terminalvelocity,
                         twr=vessel.available_thrust,
                         stagedv="",
                         totaldv="",)
# TODO get deltaV data

# TODO write to file
    exportFile.write(line)

    poll += 1

print("Cycle(s) done")

exportFile.close()

# remove streams

conn.remove.stream(apoapsis)
conn.remove.stream(periapsis)
conn.remove.stream(currentbody)
conn.remove.stream(inclination)
conn.remove.stream(missionelapsedtime)
conn.remove.stream(currentgforce)
conn.remove.stream(meanaltitude)
conn.remove.stream(terminalvelocity)
