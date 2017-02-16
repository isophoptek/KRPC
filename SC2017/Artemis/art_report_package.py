import krpc
from time import sleep
from datetime import timedelta
from math import radians


def uplink(name):
    print('Seeking connection, please ensure server is running...')
    link = krpc.connect(name=str(name))
    return link


def calculate_resource_use(resource, vessel):
    resource_amount_reference = vessel.resources.amount(resource)
    sleep(2)
    resource_amount = vessel.resources.amount(resource)
    balance = resource_amount_reference - resource_amount
    return balance


def package_occ(link):
    vessel = link.space_center.active_vessel


print('Seeking connection, please ensure server is running...')
conn = krpc.connect(name='data package uplink')

vessel = conn.space_center.active_vessel
ref_frame = vessel.surface_reference_frame
orbit = vessel.orbit
flight = vessel.flight
control = vessel.control

path = None

# create ui

display = conn.ui
screen_size = display.stock_canvas.rect_transform.size
canvas = display.add_canvas()
panel = canvas.add_panel()
panel.rect_transform.size = (200, 600)
panel.rect_transform.position = (110-(screen_size[0]/2), 0)
gui_message = panel.add_text('Telemetry log active')
gui_message.color = (0, 255, 0)
gui_message.rect_transform.position = (0, -20)
stop_button = panel.add_button("Stop transmission")
stop_button.rect_transform.position = (0, 20)
stop_button_clicked = conn.add_stream(getattr, stop_button, "clicked")

occ_button = panel.add_button("OCC Report transmission")
occ_button.rect_transform.position = (0, 40)
occ_button_clicked = conn.add_stream(getattr, occ_button, "clicked")

tmb_pre_button = panel.add_button("TMB0")
tmb_pre_button.rect_transform.position = (0, 60)
tmb_pre_button_clicked = conn.add_stream(getattr, tmb_pre_button, "clicked")

tmb_post_button = panel.add_button("TMB1")
tmb_post_button.rect_transform.position = (0, 80)
tmb_post_button_clicked = conn.add_stream(getattr, tmb_post_button, "clicked")

tmd_button = panel.add_button("TMD")
tmd_button.rect_transform.position = (0, 100)
tmd_button_clicked = conn.add_stream(getattr, tmd_button, "clicked")

mar_button = panel.add_button("MAR")
mar_button.rect_transform.position = (0, 120)
mar_button_clicked = conn.add_stream(getattr, mar_button, "clicked")

prc_button = panel.add_button("PRC")
prc_button.rect_transform.position = (0, 140)
prc_button_clicked = conn.add_stream(getattr, prc_button, "clicked")

poc_button = panel.add_button("POC")
poc_button.rect_transform.position = (0, 160)
poc_button_clicked = conn.add_stream(getattr, poc_button, "clicked")

orb_button = panel.add_button("ORB")
orb_button.rect_transform.position = (0, 180)
orb_button_clicked = conn.add_stream(getattr, orb_button, "clicked")

prr_button = panel.add_button("PRR")
prr_button.rect_transform.position = (0, 200)
prr_button_clicked = conn.add_stream(getattr, prr_button, "clicked")

por_button = panel.add_button("POR")
por_button.rect_transform.position = (0, 220)
por_button_clicked = conn.add_stream(getattr, por_button, "clicked")

mde_button = panel.add_button("MDE")
mde_button.rect_transform.position = (0, 240)
mde_button_clicked = conn.add_stream(getattr, mde_button, "clicked")

rd_button = panel.add_button("RD")
rd_button.rect_transform.position = (0, 260)
rd_button_button_clicked = conn.add_stream(getattr, rd_button, "clicked")

rco_button = panel.add_button("RCO")
rco_button.rect_transform.position = (0, 280)
rco_button_button_clicked = conn.add_stream(getattr, rco_button, "clicked")

rpr_button = panel.add_button("RPR")
rpr_button.rect_transform.position = (0, 300)
rpr_button_button_clicked = conn.add_stream(getattr, rpr_button, "clicked")

re_button = panel.add_button("RE")
re_button.rect_transform.position = (0, 320)
re_button_button_clicked = conn.add_stream(getattr, re_button, "clicked")

print('Output path:')
print(path)

# package types

# OCC

# MET
# DeltaV spent
# DeltaV remaining
# LF remaining
# Ox remaining
# monopropellant
# EC Stored
# EC Reserve
# EC drain
# EC prod
# food
# water
# o2
# waste
# wastewater
# co2
# apoapsis
# periapsis
# inclination
# orbital period
# speed
# day/night
# darkside transition

# main loop

while True:
    if occ_button_clicked():
        package_occ(conn)
    if tmb_pre_button_clicked():
        package_tmb_pre(conn)
    if tmb_post_button_clicked():
        package_tmb_post(conn)
    if tmd_button_clicked():
        package_tmd(conn)
    if mar_button_clicked():
        package_mar(conn)
    if prc_button_clicked():
        package_prc(conn)
    if poc_button_clicked():
        package_poc(conn)
    if orb_button_clicked():
        package_orb(conn)
    if prr_button_clicked():
        package_prr(conn)
    if por_button_clicked():
        package_por(conn)
    if mde_button_clicked():
        package_mde(conn)
    if rd_button_clicked():
        package_rd(conn)
    if rco_button_clicked():
        package_rco(conn)
    if prp_button_clicked():
        package_prp(conn)
    if re_button_clicked():
        package_re(conn)
