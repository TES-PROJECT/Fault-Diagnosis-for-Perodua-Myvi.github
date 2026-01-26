import streamlit as st
import clips
import logging

if "mode" not in st.session_state:
    st.session_state.mode = "menu"

# Setup working environment
logging.basicConfig(level=logging.INFO,format='%(message)s')
env = clips.Environment()
router = clips.LoggingRouter()
env.add_router(router)

#------------------------------
#definetemplate
#------------------------------
env.build("""
(deftemplate symptom
   (slot name)
   (slot value))
""")

env.build("""
(deftemplate response
    (slot diagnosis)
    (slot potential_reason)
    (slot recommendation)
)

""")

env.build("""
(deftemplate solution
    (slot diagnosis)
    (slot title)
    (slot order)
    (multislot steps)
)
""")


class knowledge_bass:
    def electrical_kb(self):
        #1.Myvi Battery Issue
        env.build("""
        (defrule diagnose-myvi-battery
            (symptom (name myvi-push-start-no-sound) (value yes))
            (symptom (name instrument-panel-dim) (value yes))
            (or
                (symptom (name battery-over-18-months) (value yes))
                (symptom (name single-click-from-starter) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi battery weak")
                (potential_reason
                    "Battery cannot hold charge due to sulfation or aging; Possible parasitic drain or faulty charging system")
            ))

            (assert (solution
                (diagnosis "Myvi battery weak")
                (order 1)
                (title "Jump start the car")
                (steps
                    "Find another car with good battery and jumper cables"
                    "Connect RED clip to positive terminal of dead battery"
                    "Connect RED clip to positive terminal of good battery"
                    "Connect BLACK clip to negative terminal of good battery"
                    "Connect BLACK clip to unpainted metal part of engine"
                    "Start the good car, then start Myvi"
                    "Remove cables in reverse order"
                )
            ))

            (assert (solution
                (diagnosis "Myvi battery weak")
                (order 2)
                (title "Replace battery")
                (steps
                    "Purchase NS40 or NS60 battery"
                    "Disconnect negative terminal first"
                    "Disconnect positive terminal"
                    "Remove battery clamp"
                    "Install new battery"
                    "Reconnect positive then negative terminal"
                )
            ))

            (assert (solution
                (diagnosis "Myvi battery weak")
                (order 3)
                (title "Test alternator charging")
                (steps
                    "Start engine"
                    "Measure battery voltage"
                    "Normal range: 13.5V–14.5V"
                    "Below 13V or above 15V indicates alternator fault"
                )
            ))
        )
        """)

        #2.Myvi Alternator Issue
        env.build("""
        (defrule diagnose-myvi-alternator
            (symptom (name battery-light-on-myvi-dash) (value yes))
            (symptom (name headlights-dim-at-idle) (value yes))
            (symptom (name electric-power-steering-heavy) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi alternator not charging")
                (potential_reason "Alternator cannot supply proper charging current; wiring or belt issue")
            ))

            (assert (solution
                (diagnosis "Myvi alternator not charging")
                (order 1)
                (title "Check alternator wiring")
                (steps
                    "Inspect wiring near exhaust for damage"
                    "Ensure connectors are tight"
                    "Check for corrosion"
                )
            ))

            (assert (solution
                (diagnosis "Myvi alternator not charging")
                (order 2)
                (title "Test alternator output")
                (steps
                    "Start engine"
                    "Measure voltage at battery terminals"
                    "Normal range: 13.5–14.5V"
                    "Replace alternator if output abnormal"
                )
            ))
        )
        """)

        #3.Myvi Starter Motor Issue
        env.build("""
        (defrule diagnose-myvi-starter
            (symptom (name myvi-click-but-no-crank) (value yes))
            (symptom (name myvi-gear-in-p-position) (value yes))
            (symptom (name myvi-brake-pedal-pressed) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi starter motor fault")
                (potential_reason "Starter motor cannot engage or crank engine; possible worn brushes or faulty solenoid")
            ))

            (assert (solution
                (diagnosis "Myvi starter motor fault")
                (order 1)
                (title "Inspect starter")
                (steps
                    "Locate starter motor under intake manifold"
                    "Check electrical connections"
                    "Listen for clicking or grinding"
                )
            ))

            (assert (solution
                (diagnosis "Myvi starter motor fault")
                (order 2)
                (title "Replace starter if faulty")
                (steps
                    "Disconnect battery"
                    "Remove starter motor"
                    "Install new starter motor"
                    "Reconnect battery"
                )
            ))
        )
        """)

        #24.Myvi Fuse Issue
        env.build("""
        (defrule diagnose-myvi-fuse-and
            (symptom (name myvi-electrical-item-dead) (value yes))
            (symptom (name myvi-recently-added-gadget) (value yes))
            (symptom (name myvi-other-things-work) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi fuse blown")
                (potential_reason "Blown fuse cuts power to electrical device")
            ))

            (assert (solution
                (diagnosis "Myvi fuse blown")
                (order 1)
                (title "Replace blown fuse")
                (steps
                    "Locate fuse box near driver's left knee"
                    "Check for blown fuse using visual inspection"
                    "Replace with correct amperage fuse"
                )
            ))
        )
        """)
    def engine_kb(self):
        #4.Myvi Ignition Coil Issue
        env.build("""
        (defrule diagnose-myvi-ignition
            (symptom (name myvi-engine-shakes-rainy-day) (value yes))
            (symptom (name myvi-check-engine-light) (value yes))
            (symptom (name myvi-loss-power-aircon-on) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi ignition coil common failure")
                (potential_reason "Ignition coil weak or failing; causes misfire or power loss")
            ))

            (assert (solution
                (diagnosis "Myvi ignition coil common failure")
                (order 1)
                (title "Replace ignition coils")
                (steps
                    "Replace both ignition coils together"
                    "Use original Perodua parts"
                )
            ))
        )
        """)

        #5.Myvi Fuel Pump Issue
        env.build("""
        (defrule diagnose-myvi-fuel-pump
            (symptom (name myvi-cranks-no-start-hot-day) (value yes))
            (symptom (name myvi-fuel-gauge-above-quarter) (value yes))
            (symptom (name myvi-stalls-traffic-jam) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi fuel pump overheating")
                (potential_reason "Fuel pump overheats and fails temporarily; common in high temperatures")
            ))

            (assert (solution
                (diagnosis "Myvi fuel pump overheating")
                (order 1)
                (title "Let fuel pump cool")
                (steps
                    "Stop car and allow fuel pump to cool"
                    "Avoid repeated hot starts"
                )
            ))
        )
        """)

        #6.Myvi Fuel Filter Issue
        env.build("""
        (defrule diagnose-myvi-fuel-filter
            (symptom (name myvi-hesitation-acceleration) (value yes))
            (symptom (name myvi-rough-idle-traffic) (value yes))
            (symptom (name myvi-never-changed-fuel-pump) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi fuel filter likely clogged")
                (potential_reason "Fuel filter may be clogged, reducing fuel flow")
            ))

            (assert (solution
                (diagnosis "Myvi fuel filter likely clogged")
                (order 1)
                (title "Replace fuel filter assembly")
                (steps
                    "Replace fuel filter and integrated pump assembly"
                    "Check for proper fuel flow after replacement"
                )
            ))
        )
        """)

        #19.Myvi Air Filter Issue
        env.build("""
        (defrule diagnose-myvi-air-filter-or
            (symptom (name myvi-sluggish-pickup) (value yes))
            (or
                (symptom (name myvi-high-fuel-consumption) (value yes))
                (symptom (name myvi-air-filter-box-dirty) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi air filter dirty")
                (potential_reason "Dirty air filter reduces airflow; affects performance")
            ))

            (assert (solution
                (diagnosis "Myvi air filter dirty")
                (order 1)
                (title "Replace air filter")
                (steps
                    "Locate air filter near battery"
                    "Remove dirty filter"
                    "Install new filter"
                )
            ))
        )
        """)


    def cooling_kb(self):
        #7.Myvi Engine Overheating
        env.build("""
        (defrule diagnose-myvi-overheat
            (symptom (name myvi-temp-gauge-in-red) (value yes))
            (symptom (name myvi-aircon-stops-when-hot) (value yes))
            (symptom (name myvi-coolant-reservoir-low) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi engine overheating common")
                (potential_reason "Small radiator or low coolant; engine may overheat easily")
            ))

            (assert (solution
                (diagnosis "Myvi engine overheating common")
                (order 1)
                (title "Check coolant system")
                (steps
                    "Check coolant level in reservoir"
                    "Inspect radiator and hoses for leaks"
                    "Check water pump operation"
                )
            ))
        )
        """)

        #8.Myvi Cooling Fan Issue
        env.build("""
        (defrule diagnose-myvi-cooling-fan
            (symptom (name myvi-overheat-traffic-only) (value yes))
            (symptom (name myvi-fan-not-spinning) (value yes))
            (symptom (name myvi-normal-on-highway) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi cooling fan motor faulty")
                (potential_reason "Cooling fan motor not working; relay or fuse may be faulty")
            ))

            (assert (solution
                (diagnosis "Myvi cooling fan motor faulty")
                (order 1)
                (title "Check fan motor")
                (steps
                    "Inspect fan motor under radiator"
                    "Check relay and fuse"
                    "Replace motor if necessary"
                )
            ))
        )
        """)

        #9.Myvi Thermostat Issue
        env.build("""
        (defrule diagnose-myvi-thermostat
            (symptom (name myvi-temp-never-reaches-middle) (value yes))
            (symptom (name myvi-heater-not-hot-enough) (value yes))
            (symptom (name myvi-poor-fuel-economy) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi thermostat stuck open")
                (potential_reason "Thermostat stuck open; engine does not reach optimal temperature")
            ))

            (assert (solution
                (diagnosis "Myvi thermostat stuck open")
                (order 1)
                (title "Replace thermostat")
                (steps
                    "Locate thermostat near water pump"
                    "Replace with original part"
                )
            ))
        )
        """)

    def brake_kb(self):
        #10.Myvi Brake Fluid Issue
        env.build("""
        (defrule diagnose-myvi-brake-fluid
            (symptom (name myvi-brake-pedal-soft) (value yes))
            (symptom (name myvi-brake-warning-light) (value yes))
            (symptom (name myvi-shift-lock-problem) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi brake fluid low")
                (potential_reason "Brake fluid level low; may affect braking performance")
            ))

            (assert (solution
                (diagnosis "Myvi brake fluid low")
                (order 1)
                (title "Check and refill brake fluid")
                (steps
                    "Locate master cylinder behind battery"
                    "Refill with DOT 3 or DOT 4 fluid"
                    "Check for leaks in brake lines"
                )
            ))
        )
        """)


        #11.Myvi Brake Pad Wear
        env.build("""
        (defrule diagnose-myvi-brake-pad-or
            (symptom (name myvi-squealing-front-brakes) (value yes))
            (or
                (symptom (name myvi-brake-dust-front-wheels) (value yes))
                (symptom (name myvi-vibration-when-braking) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi front brake pads worn")
                (potential_reason "Brake pads worn; may affect braking performance")
            ))

            (assert (solution
                (diagnosis "Myvi front brake pads worn")
                (order 1)
                (title "Check brake pads")
                (steps
                    "Inspect front brake pads visually"
                    "Look for wear indicator or thickness less than 3mm"
                )
            ))

            (assert (solution
                (diagnosis "Myvi front brake pads worn")
                (order 2)
                (title "Replace brake pads")
                (steps
                    "Replace worn brake pads"
                    "Check rotors for damage and resurface if necessary"
                )
            ))
        )
        """)


    def tires_kb(self):
        #12.Myvi Tire Issue
        env.build("""
        (defrule diagnose-myvi-tire-pressure-or
            (symptom (name myvi-tpms-warning-light) (value yes))
            (or
                (symptom (name myvi-pulling-one-side) (value yes))
                (symptom (name myvi-tire-looks-flat) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi tire underinflated")
                (potential_reason "Tire pressure low; may cause uneven wear and poor handling")
            ))

            (assert (solution
                (diagnosis "Myvi tire underinflated")
                (order 1)
                (title "Check and inflate tires")
                (steps
                    "Measure tire pressure with gauge"
                    "Inflate to 210-220 kPa front, 200-210 kPa rear"
                )
            ))
        )
        """)

        #13.Myvi Tire Blowout
        env.build("""
        (defrule diagnose-myvi-tire-blowout-or
            (symptom (name myvi-loud-pop-sound) (value yes))
            (or
                (symptom (name myvi-steering-pulls-hard) (value yes))
                (symptom (name myvi-tire-completely-flat) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi tire blowout")
                (potential_reason "Tire ruptured; car may pull to one side")
            ))

            (assert (solution
                (diagnosis "Myvi tire blowout")
                (order 1)
                (title "Replace with spare tire")
                (steps
                    "Park safely and apply handbrake"
                    "Use jack points to lift car"
                    "Replace blown tire with spare"
                )
            ))

            (assert (solution
                (diagnosis "Myvi tire blowout")
                (order 2)
                (title "Check tire pressure")
                (steps
                    "Inspect other tires for proper pressure"
                    "Inflate or repair as needed"
                )
            ))
        )
        """)

        #14.Myvi Steering Wheel Shake
        env.build("""
        (defrule diagnose-myvi-steering-vibration-or
            (symptom (name myvi-shaking-steering-wheel) (value yes))
            (or
                (symptom (name myvi-worse-at-100-110kmh) (value yes))
                (symptom (name myvi-front-tires-worn) (value yes))
            )
            (symptom (name myvi-hit-pothole-recently) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi wheel imbalance")
                (potential_reason "Wheel imbalance or uneven tire wear; vibration at certain speeds")
            ))

            (assert (solution
                (diagnosis "Myvi wheel imbalance")
                (order 1)
                (title "Check tire balance")
                (steps
                    "Inspect front tires for wear"
                    "Rotate tires if necessary"
                    "Balance wheels at workshop"
                )
            ))
        )
        """)

        #26.Myvi Wheel Bearing Issue
        env.build("""
        (defrule diagnose-myvi-wheel-bearing-and
            (symptom (name myvi-humming-noise-wheels) (value yes))
            (symptom (name myvi-noise-increases-speed) (value yes))
            (symptom (name myvi-noise-worse-certain-corners) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi wheel bearing failure")
                (potential_reason "Front wheel bearings worn; noise increases with speed")
            ))

            (assert (solution
                (diagnosis "Myvi wheel bearing failure")
                (order 1)
                (title "Inspect wheel bearings")
                (steps
                    "Jack up front wheels safely"
                    "Spin wheels and listen for humming or roughness"
                )
            ))

            (assert (solution
                (diagnosis "Myvi wheel bearing failure")
                (order 2)
                (title "Replace wheel bearings")
                (steps
                    "Replace front wheel bearings in pairs"
                    "Grease bearings and torque bolts to specification"
                )
            ))
        )
        """)

    def transmission_kb(self):
        #15.Myvi 4AT Transmission Issue
        env.build("""
        (defrule diagnose-myvi-4at-or
            (symptom (name myvi-rough-1-2-shift) (value yes))
            (or
                (symptom (name myvi-delay-shift-p-to-d) (value yes))
                (symptom (name myvi-atf-dark-burnt) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi 4AT transmission issue")
                (potential_reason "Fluid degradation or wear; affects shifting quality")
            ))

            (assert (solution
                (diagnosis "Myvi 4AT transmission issue")
                (order 1)
                (title "Check ATF")
                (steps
                    "Inspect transmission fluid level and color"
                    "Top up with Toyota Type IV ATF if needed"
                )
            ))
        )
        """)

        #16.Myvi D-CVT Transmission Issue
        env.build("""
        (defrule diagnose-myvi-dcvt-or
            (symptom (name myvi-high-revs-low-speed) (value yes))
            (or
                (symptom (name myvi-whining-cvt-noise) (value yes))
                (symptom (name myvi-shudder-low-speed) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi D-CVT transmission problem")
                (potential_reason "CVT fluid or belt issue; causes whining or shudder")
            ))

            (assert (solution
                (diagnosis "Myvi D-CVT transmission problem")
                (order 1)
                (title "Check CVT fluid")
                (steps
                    "Use only Perodua CVT fluid"
                    "Do not use regular ATF"
                )
            ))
        )
        """)

    def ac_kb(self):
        #20.Myvi AC Not Cooling
        env.build("""
        (defrule diagnose-myvi-aircon-or
            (symptom (name myvi-ac-warm-idle) (value yes))
            (or
                (symptom (name myvi-compressor-not-running) (value yes))
                (symptom (name myvi-ac-cold-only-when-moving) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi AC refrigerant low")
                (potential_reason "AC refrigerant low; reduces cooling performance")
            ))

            (assert (solution
                (diagnosis "Myvi AC refrigerant low")
                (order 1)
                (title "Check refrigerant")
                (steps
                    "Inspect condenser for leaks"
                    "Check for oily spots indicating leak"
                    "Recharge refrigerant if needed"
                )
            ))
        )
        """)


        #21.Myvi AC Compressor Issue
        env.build("""
        (defrule diagnose-myvi-ac-compressor-and
            (symptom (name myvi-loud-ac-compressor) (value yes))
            (symptom (name myvi-ac-not-cold-at-all) (value yes))
            (symptom (name myvi-burning-smell-ac) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi AC compressor faulty")
                (potential_reason "Compressor worn or seized; AC not cooling")
            ))

            (assert (solution
                (diagnosis "Myvi AC compressor faulty")
                (order 1)
                (title "Check AC compressor fuse")
                (steps
                    "Locate fuse for AC compressor"
                    "Replace blown fuse if necessary"
                )
            ))

            (assert (solution
                (diagnosis "Myvi AC compressor faulty")
                (order 2)
                (title "Replace AC compressor")
                (steps
                    "Replace compressor and dryer"
                    "Recharge AC system with correct refrigerant"
                )
            ))
        )
        """)

        #22.Myvi AC Drain Clog
        env.build("""
        (defrule diagnose-myvi-ac-drain-and
            (symptom (name myvi-water-passenger-footwell) (value yes))
            (symptom (name myvi-musty-smell-interior) (value yes))
            (symptom (name myvi-wet-passenger-carpet) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi AC drain tube clogged")
                (potential_reason "Drain tube blocked; water accumulates inside car")
            ))

            (assert (solution
                (diagnosis "Myvi AC drain tube clogged")
                (order 1)
                (title "Clear AC drain tube")
                (steps
                    "Locate drain tube under passenger side"
                    "Use compressed air or flexible wire to clear blockage"
                )
            ))
        )
        """)

    def body_kb(self):
        #17.Myvi Exhaust Rust
        env.build("""
        (defrule diagnose-myvi-exhaust-or
            (symptom (name myvi-exhaust-louder) (value yes))
            (or
                (symptom (name myvi-rust-middle-exhaust) (value yes))
                (symptom (name myvi-car-over-3-years) (value yes))
            )
            =>
            (assert (response
                (diagnosis "Myvi exhaust pipe rusted")
                (potential_reason "Middle section rusted; may cause noise or leak")
            ))

            (assert (solution
                (diagnosis "Myvi exhaust pipe rusted")
                (order 1)
                (title "Inspect and patch")
                (steps
                    "Inspect middle section for rust"
                    "Weld or patch small rust holes"
                    "Replace section if severely corroded"
                )
            ))
        )
        """)





        #23.Myvi Head light Yellowing
        env.build("""
        (defrule diagnose-myvi-headlight-and
            (symptom (name myvi-headlights-yellow-cloudy) (value yes))
            (symptom (name myvi-poor-night-vision) (value yes))
            (symptom (name myvi-parked-outside-always) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi headlight oxidation")
                (potential_reason "UV exposure causes lens yellowing; reduces light output")
            ))

            (assert (solution
                (diagnosis "Myvi headlight oxidation")
                (order 1)
                (title "Restore headlights")
                (steps
                    "Use headlight restoration kit"
                    "Polish lens surface until clear"
                )
            ))
        )
        """)

    def suspension_kb(self):
        #25.Myvi Suspension Issue
        env.build("""
        (defrule diagnose-myvi-suspension-and
            (symptom (name myvi-bouncy-ride) (value yes))
            (symptom (name myvi-clunking-front-suspension) (value yes))
            (symptom (name myvi-nose-dives-when-braking) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi suspension worn")
                (potential_reason "Front struts and bushings worn; affects ride stability")
            ))

            (assert (solution
                (diagnosis "Myvi suspension worn")
                (order 1)
                (title "Inspect front suspension")
                (steps
                    "Check for worn struts and bushings"
                    "Look for oil leaks or damaged components"
                )
            ))

            (assert (solution
                (diagnosis "Myvi suspension worn")
                (order 2)
                (title "Replace worn components")
                (steps
                    "Replace front struts and bushings"
                    "Test drive to verify improved ride quality"
                )
            ))
        )
        """)

    def steering_kb(self):
        #27.Myvi Electric Power Steering Issue
        env.build("""
        (defrule diagnose-myvi-eps-and
            (symptom (name myvi-steering-heavy-sometimes) (value yes))
            (symptom (name myvi-eps-warning-light) (value yes))
            (symptom (name myvi-steering-not-smooth) (value yes))
            =>
            (assert (response
                (diagnosis "Myvi EPS system fault")
                (potential_reason "EPS control unit or motor fault; steering may feel heavy or uneven")
            ))

            (assert (solution
                (diagnosis "Myvi EPS system fault")
                (order 1)
                (title "Check EPS warning light")
                (steps
                    "Confirm EPS warning light is on"
                    "Turn off car and restart to see if light clears"
                )
            ))

            (assert (solution
                (diagnosis "Myvi EPS system fault")
                (order 2)
                (title "Check EPS unit")
                (steps
                    "Inspect EPS control unit under dash"
                    "If problem persists, take to professional workshop for recalibration or repair"
                )
            ))
        )
        """)
    def load_all(self):
        self.electrical_kb()
        self.engine_kb()
        self.cooling_kb()
        self.brake_kb()
        self.tires_kb()
        self.transmission_kb()
        self.ac_kb()
        self.body_kb()
        self.suspension_kb()
        self.steering_kb()






#------------------------------
#Interactive input function
#------------------------------
symptoms_by_category = {

    "electrical": [
        "myvi-push-start-no-sound",
        "instrument-panel-dim",
        "battery-over-18-months",
        "single-click-from-starter",
        "battery-light-on-myvi-dash",
        "headlights-dim-at-idle",
        "electric-power-steering-heavy",
        "myvi-click-but-no-crank",
        "myvi-gear-in-p-position",
        "myvi-brake-pedal-pressed",
        "myvi-electrical-item-dead",
        "myvi-recently-added-gadget",
        "myvi-other-things-work",
    ],

    "engine": [
        "myvi-engine-shakes-rainy-day",
        "myvi-check-engine-light",
        "myvi-loss-power-aircon-on",
        "myvi-cranks-no-start-hot-day",
        "myvi-fuel-gauge-above-quarter",
        "myvi-stalls-traffic-jam",
        "myvi-hesitation-acceleration",
        "myvi-rough-idle-traffic",
        "myvi-never-changed-fuel-pump",
        "myvi-sluggish-pickup",
        "myvi-high-fuel-consumption",
        "myvi-air-filter-box-dirty",
    ],

    "cooling": [
        "myvi-temp-gauge-in-red",
        "myvi-aircon-stops-when-hot",
        "myvi-coolant-reservoir-low",
        "myvi-overheat-traffic-only",
        "myvi-fan-not-spinning",
        "myvi-normal-on-highway",
        "myvi-temp-never-reaches-middle",
        "myvi-heater-not-hot-enough",
        "myvi-poor-fuel-economy",
    ],

    "brake": [
        "myvi-brake-pedal-soft",
        "myvi-brake-warning-light",
        "myvi-shift-lock-problem",
        "myvi-squealing-front-brakes",
        "myvi-brake-dust-front-wheels",
        "myvi-vibration-when-braking",
    ],

    "tires_wheels": [
        "myvi-tpms-warning-light",
        "myvi-pulling-one-side",
        "myvi-tire-looks-flat",
        "myvi-loud-pop-sound",
        "myvi-steering-pulls-hard",
        "myvi-tire-completely-flat",
        "myvi-shaking-steering-wheel",
        "myvi-worse-at-100-110kmh",
        "myvi-front-tires-worn",
        "myvi-hit-pothole-recently",
        "myvi-humming-noise-wheels",
        "myvi-noise-increases-speed",
        "myvi-noise-worse-certain-corners",
    ],

    "transmission": [
        "myvi-rough-1-2-shift",
        "myvi-delay-shift-p-to-d",
        "myvi-atf-dark-burnt",
        "myvi-high-revs-low-speed",
        "myvi-whining-cvt-noise",
        "myvi-shudder-low-speed",
    ],

    "aircon": [
        "myvi-ac-warm-idle",
        "myvi-compressor-not-running",
        "myvi-ac-cold-only-when-moving",
        "myvi-loud-ac-compressor",
        "myvi-ac-not-cold-at-all",
        "myvi-burning-smell-ac",
        "myvi-water-passenger-footwell",
        "myvi-musty-smell-interior",
        "myvi-wet-passenger-carpet",
    ],

    "body": [
        "myvi-exhaust-louder",
        "myvi-rust-middle-exhaust",
        "myvi-car-over-3-years",
        "myvi-headlights-yellow-cloudy",
        "myvi-poor-night-vision",
        "myvi-parked-outside-always",
    ],

    "suspension": [
        "myvi-bouncy-ride",
        "myvi-clunking-front-suspension",
        "myvi-nose-dives-when-braking",
    ],

    "steering": [
        "myvi-steering-heavy-sometimes",
        "myvi-eps-warning-light",
        "myvi-steering-not-smooth",
    ],
}

questions_by_category = {

    "electrical": [
        "Does the Myvi push start button make no sound when you press it?",
        "Does the instrument panel appear dim or darker than usual?",
        "Is the car battery older than 18 months?",
        "Do you hear a single clicking sound when trying to start the car?",
        "Is the battery warning light turned on on the Myvi dashboard?",
        "Do the headlights become dim when the engine is idling?",
        "Does the electric power steering feel heavy when turning?",
        "Do you hear a click sound but the engine does not crank?",
        "Is the gear lever currently in the P (Park) position?",
        "Are you pressing the brake pedal while trying to start the car?",
        "Are most electrical items (radio, windows, lights) not working?",
        "Have you recently installed any new electrical gadgets or accessories?",
        "Do some electrical components still work normally?",
    ],

    "engine": [
        "Does the engine shake more than usual on rainy days?",
        "Is the check engine light currently turned on?",
        "Does the car lose power when the air conditioner is turned on?",
        "Does the engine crank but fail to start on a hot day?",
        "Is the fuel gauge showing more than a quarter tank?",
        "Does the engine stall when driving in heavy traffic?",
        "Does the car hesitate when you press the accelerator?",
        "Does the engine idle roughly when stuck in traffic?",
        "Have you never changed the fuel pump before?",
        "Does the car feel sluggish when accelerating?",
        "Is the fuel consumption higher than normal?",
        "Is the air filter box dirty or clogged?",
    ],

    "cooling": [
        "Does the temperature gauge rise into the red zone?",
        "Does the air conditioner stop working when the engine gets hot?",
        "Is the coolant level in the reservoir low?",
        "Does the car overheat only when driving in traffic jams?",
        "Is the radiator fan not spinning when the engine is hot?",
        "Does the car operate at normal temperature when driving on the highway?",
        "Does the engine temperature never reach the normal middle level?",
        "Is the heater not producing enough hot air?",
        "Is the fuel economy worse than usual?",
    ],

    "brake": [
        "Does the brake pedal feel soft or spongy when pressed?",
        "Is the brake warning light illuminated on the dashboard?",
        "Do you have difficulty shifting out of Park due to a shift lock issue?",
        "Do you hear a squealing sound from the front brakes?",
        "Is there excessive brake dust on the front wheels?",
        "Do you feel vibration when braking?",
    ],

    "tires_wheels": [
        "Is the TPMS (tire pressure) warning light on?",
        "Does the car pull to one side while driving?",
        "Does one of the tires look flat?",
        "Did you hear a loud popping sound while driving?",
        "Does the steering pull strongly to one side?",
        "Is one of the tires completely flat?",
        "Does the steering wheel shake while driving?",
        "Is the shaking worse at speeds between 100–110 km/h?",
        "Are the front tires visibly worn?",
        "Have you hit a pothole recently?",
        "Do you hear a humming noise from the wheels?",
        "Does the noise increase as the car speed increases?",
        "Is the noise worse when turning in certain corners?",
    ],

    "transmission": [
        "Does the car shift roughly from first to second gear?",
        "Is there a noticeable delay when shifting from Park to Drive?",
        "Does the transmission fluid appear dark or burnt?",
        "Does the engine rev high but the car moves slowly?",
        "Do you hear a whining noise from the CVT transmission?",
        "Does the car shudder when moving at low speed?",
    ],

    "aircon": [
        "Does the air conditioner blow warm air when the car is idling?",
        "Is the air conditioner compressor not running?",
        "Does the air conditioner only blow cold air when the car is moving?",
        "Is the air conditioner compressor unusually loud?",
        "Is the air conditioner not cold at all?",
        "Do you notice a burning smell when the air conditioner is on?",
        "Is there water leaking into the passenger footwell?",
        "Is there a musty or moldy smell inside the car?",
        "Is the passenger-side carpet wet?",
    ],

    "body": [
        "Is the exhaust sound louder than usual?",
        "Is there visible rust in the middle section of the exhaust?",
        "Is the car more than three years old?",
        "Are the headlights yellowed or cloudy?",
        "Is your night-time visibility poor?",
        "Is the car usually parked outdoors?",
    ],

    "suspension": [
        "Does the car feel bouncy while driving?",
        "Do you hear clunking noises from the front suspension?",
        "Does the front of the car dive down when braking?",
    ],

    "steering": [
        "Does the steering sometimes feel heavy?",
        "Is the EPS warning light turned on?",
        "Does the steering feel rough or not smooth?",
    ],
}




#------------------------------
#Output Diagnostics and Solutions
#------------------------------

kb = knowledge_bass()

def run_inference():
    for fact in env.facts():
        if fact.template.name != "response":
            continue

        diagnosis = fact["diagnosis"]

        st.success(f"Diagnosis: {diagnosis}")
        st.write("**Potential Reason:**")
        st.write(fact["potential_reason"])


        if "recommendation" in fact and fact["recommendation"]:
            print("\nRecommendation:")
            print(fact["recommendation"])

        #Collect solutions for the corresponding diagnosis
        solutions = []

        for s in env.facts():
            if s.template.name == "solution" and s["diagnosis"] == diagnosis:
                solutions.append(s)

        solutions.sort(key=lambda x: x["order"])

        if solutions:
            st.subheader("Solutions")
            for sol in solutions:
                with st.expander(sol["title"]):
                    for i, step in enumerate(sol["steps"], 1):
                        st.write(f"{i}. {step}")

def ask_symptom(name):
    while True:
        ans = input(f"{name} [yes/no] or [y/n]: ").strip().lower()
        if ans in ('y', 'n'):
            return ans
        if ans in ('yes' , 'no'):
            if ans == 'yes':
                return 'y'
            else:
                return 'n'
        print("Please enter 'yes' or 'no'.")

def check_number():
    while True:
        number = input("\nPlease Enter Your Choice : ").strip()
        if number.isdigit() and 1 <= int(number) <=11:
            return int(number)
        else:
            print("Invalid input. Please enter a number between 1 and 11.")


def active_expert_system():
    mode = st.session_state.mode
    kb = knowledge_bass()



    # ======================
    #PAGE 1: MENU
    # ======================
    if mode == "menu":
        st.write("=========================================")
        st.title("Welcome To Vehicle Diagnostics Expert System")
        st.write("=========================================")
        st.text("What kind of the Vehicle Fault Points ( Enter the number [1-11])")
        st.text("1. Electrical Problem")
        st.text("2. Engine & Fuel")
        st.text("3. Cooling")
        st.text("4. Brakes")
        st.text("5. Tires & Wheels")
        st.text("6. Transmission")
        st.text("7. Air Conditioning")
        st.text("8. Body")
        st.text("9. Suspension")
        st.text("10. Steering")
        st.text("11. Not sure(Comprehensive inspection)")

        choice = st.selectbox(
            "Please Enter Your Choice (1–11):",
            list(range(1, 12)),
            key="menu_choice"
        )

        if st.button("➡ Next"):
            st.session_state.choice = choice
            st.session_state.mode = "symptom"
            st.rerun()

    # ======================
    #PAGE 2: SYMPTOMS
    # ======================
    elif mode == "symptom":
        if "answers" not in st.session_state:
            st.session_state.answers = {}

        choice = st.session_state.choice

        match choice:
            case 1:
                kb.electrical_kb()
                category = "electrical"
            case 2:
                kb.engine_kb()
                category = "engine"
            case 3:
                kb.cooling_kb()
                category = "cooling"
            case 4:
                kb.brake_kb()
                category = "brake"
            case 5:
                kb.tires_kb()
                category = "tires_wheels"
            case 6:
                kb.transmission_kb()
                category = "transmission"
            case 7:
                kb.ac_kb()
                category = "aircon"
            case 8:
                kb.body_kb()
                category = "body"
            case 9:
                kb.suspension_kb()
                category = "suspension"
            case 10:
                kb.steering_kb()
                category = "steering"
            case 11:
                kb.load_all()
                category = ""


        if category == "":
            symptoms = [s for v in symptoms_by_category.values() for s in v]
            questions = [q for v in questions_by_category.values() for q in v]
        else:
            symptoms = symptoms_by_category[category]
            questions = questions_by_category[category]

        st.subheader("Symptom Checklist")

        for symptom_name, question in zip(symptoms, questions):
            col_q, col_ans = st.columns([6, 2])
            with col_q:
                st.write(question)
            with col_ans:
                prev = st.session_state.answers.get(symptom_name)

                choice = st.radio(
                    label="Answer",
                    options=["YES", "NO"],
                    index=(
                        0 if prev == "YES"
                        else 1 if prev == "NO"
                        else None
                    ),
                    horizontal=True,
                    key=f"sym_{symptom_name}",
                    label_visibility="collapsed"
                )

                st.session_state.answers[symptom_name] = choice

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Back"):
                st.session_state.mode = "menu"
                st.rerun()

        with col2:
            if st.button("Submit"):
                if any(v is None for v in st.session_state.answers.values()):
                    st.error("Please answer ALL symptom questions before continuing.")
                else:
                    st.session_state.mode = "result"
                    st.rerun()

    # ======================
    # PAGE 3: RESULT
    # ======================
    elif mode == "result":
        st.subheader("Diagnosis Result")

        env.reset()
        kb.load_all()


        for symptom_name, ans in st.session_state.answers.items():
            if ans == "YES":
                env.assert_string(
                    f"(symptom (name {symptom_name}) (value yes))"
                )

        env.run()
        run_inference()

        if st.button("⬅ Back to Symptoms"):
            st.session_state.mode = "symptom"
            st.rerun()

        if st.button("🏠 Home"):
            st.session_state.mode = "menu"

            if "answers" in st.session_state:
                del st.session_state.answers

            if "choice" in st.session_state:
                del st.session_state.choice

            st.rerun()

active_expert_system()

