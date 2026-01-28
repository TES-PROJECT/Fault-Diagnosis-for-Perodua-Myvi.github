#import necessary library
import streamlit as st
import clips
import logging
import os

#use to locate the project root directory for loading files such as images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#load the css file
with open(".streamlit/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#initialization(if first time coming,then set the has_started)
if "has_started" not in st.session_state:
    st.session_state.has_started = False

#Only display welcome when first come
if "mode" not in st.session_state: #if first time come, direct to welcome page
    st.session_state.mode = "welcome"
    
#setup working environment
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
    )
""")

env.build("""
(deftemplate solution
    (slot diagnosis)
    (slot title)
    (slot order)
    (multislot steps))
""")

env.build("""
(deftemplate symptom-question
   (slot category)
   (slot name)
   (slot sentence)
   (multislot image))
""")

class knowledge_bass:
    def electrical_kb(self):
        env.build("""
        (deffacts electrical-questions
        
            (symptom-question
            (category electrical)
            (name myvi-push-start-no-sound)
            (sentence "Does the Myvi push start button make no sound when you press it?")
            (image "picture/myvi-push-start-no-sound.png")
            )

           (symptom-question
              (category electrical)
              (name instrument-panel-dim)
              (sentence "Does the instrument panel appear dim or darker than usual?")
              (image "picture/instrument-panel-dim.png")
           )
        
           (symptom-question
              (category electrical)
              (name battery-over-18-months)
              (sentence "Is the car battery older than 18 months?")
           )
        
           (symptom-question
              (category electrical)
              (name single-click-from-starter)
              (sentence "Do you hear a single clicking sound when trying to start the car?")
           )
        
           (symptom-question
              (category electrical)
              (name battery-light-on-myvi-dash)
              (sentence "Is the battery warning light turned on on the Myvi dashboard?")
              (image "picture/battery-light-on-myvi-dash.png")
           )

           (symptom-question
               (category electrical)
               (name headlights-dim-at-idle)
               (sentence "Do the headlights become dim when the engine is idling?")
               (image "picture/headlights-dim-at-idle.png")
            )
            
            (symptom-question
               (category electrical)
               (name electric-power-steering-heavy)
               (sentence "Does the electric power steering feel heavy when turning?")
            )
            
            (symptom-question
               (category electrical)
               (name myvi-click-but-no-crank)
               (sentence "Do you hear a click sound but the engine does not crank?")
            )
            
            (symptom-question
               (category electrical)
               (name myvi-gear-in-p-position)
               (sentence "Is the gear lever currently in the P (Park) position?")
               (image "picture/myvi-gear-in-p-position.png")
            )
            
            (symptom-question
               (category electrical)
               (name myvi-brake-pedal-pressed)
               (sentence "Are you pressing the brake pedal while trying to start the car?")
               (image "picture/myvi-brake-pedal-pressed.png")
            )
            
            (symptom-question
               (category electrical)
               (name myvi-electrical-item-dead)
               (sentence "Are most electrical items not working?")
            )
            
            (symptom-question
               (category electrical)
               (name myvi-recently-added-gadget)
               (sentence "Have you recently installed any new electrical gadgets?")
            )
            
            (symptom-question
               (category electrical)
               (name myvi-other-things-work)
               (sentence "Do some electrical components still work normally?")
            )
        )
        """)

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
                    "Normal range: 13.5V-14.5V"
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
                    "Normal range: 13.5-14.5V"
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
        env.build("""
        (deffacts engine-questions
        
           (symptom-question
              (category engine)
              (name myvi-engine-shakes-rainy-day)
              (sentence "Does the engine shake more than usual on rainy days?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-check-engine-light)
              (sentence "Is the check engine light currently turned on?")
              (image "picture/myvi-check-engine-light.png")
           )
        
           (symptom-question
              (category engine)
              (name myvi-loss-power-aircon-on)
              (sentence "Does the car lose power when the air conditioner is turned on?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-cranks-no-start-hot-day)
              (sentence "Does the engine crank but fail to start on a hot day?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-fuel-gauge-above-quarter)
              (sentence "Is the fuel gauge showing more than a quarter tank?")
              (image "picture/myvi-fuel-gauge-above-quarter.png")
           )
        
           (symptom-question
              (category engine)
              (name myvi-stalls-traffic-jam)
              (sentence "Does the engine stall when driving in heavy traffic?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-hesitation-acceleration)
              (sentence "Does the car hesitate when you press the accelerator?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-rough-idle-traffic)
              (sentence "Does the engine idle roughly when stuck in traffic?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-never-changed-fuel-pump)
              (sentence "Have you never changed the fuel pump before?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-sluggish-pickup)
              (sentence "Does the car feel sluggish when accelerating?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-high-fuel-consumption)
              (sentence "Is the fuel consumption higher than normal?")
           )
        
           (symptom-question
              (category engine)
              (name myvi-air-filter-box-dirty)
              (sentence "Is the air filter box dirty or clogged?")
              (image "picture/myvi-air-filter-box-dirty.png")
           )
        
        )
        """)

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
        env.build("""
        (deffacts cooling-questions
        
           (symptom-question (category cooling) (name myvi-temp-gauge-in-red)
              (sentence "Does the temperature gauge rise into the red zone?")
              (image "picture/myvi-temp-gauge-in-red.png"))
        
           (symptom-question (category cooling) (name myvi-aircon-stops-when-hot)
              (sentence "Does the air conditioner stop working when the engine gets hot?"))
        
           (symptom-question (category cooling) (name myvi-coolant-reservoir-low)
              (sentence "Is the coolant level in the reservoir low?")
              (image "picture/myvi-coolant-reservoir-low-1.png" "picture/myvi-coolant-reservoir-low-2.png")
              )
        
           (symptom-question (category cooling) (name myvi-overheat-traffic-only)
              (sentence "Does the car overheat only when driving in traffic jams?"))
        
           (symptom-question (category cooling) (name myvi-fan-not-spinning)
              (sentence "Is the radiator fan not spinning when the engine is hot?"))
        
           (symptom-question (category cooling) (name myvi-normal-on-highway)
              (sentence "Does the car operate at normal temperature on the highway?")
              (image "picture/engine-temperature.png"))
        
           (symptom-question (category cooling) (name myvi-temp-never-reaches-middle)
              (sentence "Does the engine temperature never reach the normal middle level?")
              (image "picture/engine-temperature.png"))
        
           (symptom-question (category cooling) (name myvi-heater-not-hot-enough)
              (sentence "Is the heater not producing enough hot air?"))
        
           (symptom-question (category cooling) (name myvi-poor-fuel-economy)
              (sentence "Is the fuel economy worse than usual?"))
        
        )
        """)

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
        env.build("""
        (deffacts brake-questions
        
           (symptom-question (category brake) (name myvi-brake-pedal-soft)
              (sentence "Does the brake pedal feel soft or spongy when pressed?"))
        
           (symptom-question (category brake) (name myvi-brake-warning-light)
              (sentence "Is the brake warning light illuminated on the dashboard?")
              (image "picture/myvi-brake-warning-light.png"))
        
           (symptom-question (category brake) (name myvi-shift-lock-problem)
              (sentence "Do you have difficulty shifting out of Park due to a shift lock issue?")
              (image "picture/myvi-shift-lock-problem.png"))
        
           (symptom-question (category brake) (name myvi-squealing-front-brakes)
              (sentence "Do you hear a squealing sound from the front brakes?"))
        
           (symptom-question (category brake) (name myvi-brake-dust-front-wheels)
              (sentence "Is there excessive brake dust on the front wheels?")
              (image "picture/myvi-brake-dust-front-wheels.png"))
        
           (symptom-question (category brake) (name myvi-vibration-when-braking)
              (sentence "Do you feel vibration when braking?"))
        
        )
        """)

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
        env.build("""
        (deffacts tire-questions
        
           (symptom-question (category tires_wheels) (name myvi-tpms-warning-light)
              (sentence "Is the TPMS (tire pressure) warning light on?"))
        
           (symptom-question (category tires_wheels) (name myvi-pulling-one-side)
              (sentence "Does the car pull to one side while driving?"))
        
           (symptom-question (category tires_wheels) (name myvi-tire-looks-flat)
              (sentence "Does one of the tires look flat?"))
        
           (symptom-question (category tires_wheels) (name myvi-loud-pop-sound)
              (sentence "Did you hear a loud popping sound while driving?"))
        
           (symptom-question (category tires_wheels) (name myvi-steering-pulls-hard)
              (sentence "Does the steering pull strongly to one side?"))
        
           (symptom-question (category tires_wheels) (name myvi-tire-completely-flat)
              (sentence "Is one of the tires completely flat?"))
        
           (symptom-question (category tires_wheels) (name myvi-shaking-steering-wheel)
              (sentence "Does the steering wheel shake while driving?"))
        
           (symptom-question (category tires_wheels) (name myvi-worse-at-100-110kmh)
              (sentence "Is the shaking worse at speeds between 100–110 km/h?"))
        
           (symptom-question (category tires_wheels) (name myvi-front-tires-worn)
              (sentence "Are the front tires visibly worn?"))
        
           (symptom-question (category tires_wheels) (name myvi-hit-pothole-recently)
              (sentence "Have you hit a pothole recently?"))
        
           (symptom-question (category tires_wheels) (name myvi-humming-noise-wheels)
              (sentence "Do you hear a humming noise from the wheels?"))
        
           (symptom-question (category tires_wheels) (name myvi-noise-increases-speed)
              (sentence "Does the noise increase as the car speed increases?"))
        
           (symptom-question (category tires_wheels) (name myvi-noise-worse-certain-corners)
              (sentence "Is the noise worse when turning in certain corners?"))
        
        )
        """)

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
        env.build("""
        (deffacts transmission-questions
        
           (symptom-question (category transmission) (name myvi-rough-1-2-shift)
              (sentence "Does the car shift roughly from first to second gear?"))
        
           (symptom-question (category transmission) (name myvi-delay-shift-p-to-d)
              (sentence "Is there a noticeable delay when shifting from Park to Drive?"))
        
           (symptom-question (category transmission) (name myvi-atf-dark-burnt)
              (sentence "Does the transmission fluid appear dark or burnt?"))
        
           (symptom-question (category transmission) (name myvi-high-revs-low-speed)
              (sentence "Does the engine rev high but the car moves slowly?"))
        
           (symptom-question (category transmission) (name myvi-whining-cvt-noise)
              (sentence "Do you hear a whining noise from the CVT transmission?"))
        
           (symptom-question (category transmission) (name myvi-shudder-low-speed)
              (sentence "Does the car shudder when moving at low speed?"))
        
        )
        """)

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
        env.build("""
        (deffacts aircon-questions
        
           (symptom-question (category aircon) (name myvi-ac-warm-idle)
              (sentence "Does the air conditioner blow warm air when the car is idling?"))
        
           (symptom-question (category aircon) (name myvi-compressor-not-running)
              (sentence "Is the air conditioner compressor not running?"))
        
           (symptom-question (category aircon) (name myvi-ac-cold-only-when-moving)
              (sentence "Does the air conditioner only blow cold air when the car is moving?"))
        
           (symptom-question (category aircon) (name myvi-loud-ac-compressor)
              (sentence "Is the air conditioner compressor unusually loud?"))
        
           (symptom-question (category aircon) (name myvi-ac-not-cold-at-all)
              (sentence "Is the air conditioner not cold at all?"))
        
           (symptom-question (category aircon) (name myvi-burning-smell-ac)
              (sentence "Do you notice a burning smell when the air conditioner is on?"))
        
           (symptom-question (category aircon) (name myvi-water-passenger-footwell)
              (sentence "Is there water leaking into the passenger footwell?"))
        
           (symptom-question (category aircon) (name myvi-musty-smell-interior)
              (sentence "Is there a musty or moldy smell inside the car?"))
        
           (symptom-question (category aircon) (name myvi-wet-passenger-carpet)
              (sentence "Is the passenger-side carpet wet?"))
        
        )
        """)

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
        env.build("""
        (deffacts body-questions
        
           (symptom-question (category body) (name myvi-exhaust-louder)
              (sentence "Is the exhaust sound louder than usual?"))
        
           (symptom-question (category body) (name myvi-rust-middle-exhaust)
              (sentence "Is there visible rust in the middle section of the exhaust?"))
        
           (symptom-question (category body) (name myvi-car-over-3-years)
              (sentence "Is the car more than three years old?"))
        
           (symptom-question (category body) (name myvi-headlights-yellow-cloudy)
              (sentence "Are the headlights yellowed or cloudy?"))
        
           (symptom-question (category body) (name myvi-poor-night-vision)
              (sentence "Is your night-time visibility poor?"))
        
           (symptom-question (category body) (name myvi-parked-outside-always)
              (sentence "Is the car usually parked outdoors?"))
        
        )
        """)

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
        env.build("""
        (deffacts suspension-questions
        
           (symptom-question (category suspension) (name myvi-bouncy-ride)
              (sentence "Does the car feel bouncy while driving?"))
        
           (symptom-question (category suspension) (name myvi-clunking-front-suspension)
              (sentence "Do you hear clunking noises from the front suspension?"))
        
           (symptom-question (category suspension) (name myvi-nose-dives-when-braking)
              (sentence "Does the front of the car dive down when braking?"))
        
        )
        """)

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
        env.build("""
        (deffacts steering-questions
        
           (symptom-question (category steering) (name myvi-steering-heavy-sometimes)
              (sentence "Does the steering sometimes feel heavy?"))
        
           (symptom-question (category steering) (name myvi-eps-warning-light)
              (sentence "Is the EPS warning light turned on?"))
        
           (symptom-question (category steering) (name myvi-steering-not-smooth)
              (sentence "Does the steering feel rough or not smooth?"))
        
        )
        """)

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

    def load_all(self): #if user choice all , then load all
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


#q_label: text of the question to be displayed (like "Q1. ...")
#images: list of image paths related to this question
def question_image(q_label, images):
    st.markdown(
        f"<div class='question-text'>{q_label}</div>",
        unsafe_allow_html=True
    )

    if images:
        #section for reference images
        with st.expander("💡 What does this look like?"):
            #img: relative image path from the kb
            for img in images:
                img_path = os.path.join(BASE_DIR, img) #convert relative image path to absolute file path

                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                    #show the image in the webpage
                else:
                    st.error(f"Image not found: {img_path}")
                    #error message if image file is missing


#------------------------------
#output diagnostics and solutions
#------------------------------
kb = knowledge_bass()#set class knowledge_bass = kb

#category: select fault category
def ask_symptom(category):
    questions = [] #list to store symptom questions for the webpage

    #loop through all CLIPS facts
    for fact in env.facts():
        #select symptom-question facts only
        if fact.template.name == "symptom-question":
            #filter questions by category
            if category == "" or fact["category"] == category:
                images = fact["image"] if fact["image"] else [] #images: related image paths
                questions.append(
                    (
                        fact["name"], #symptom id
                        fact["sentence"], #question text
                        images #images for this question
                    )
                )
    return questions #return filter questions

def run_inference():
    diagnosis_index = 1 # set the index number to 1 first
    for fact in env.facts(): #read all the clips facts
        if fact.template.name != "response": #only read the fact that = response
            continue # if no,skip first

        diagnosis = fact["diagnosis"]#let diagnosis = diagnosis that inside the fact

        st.markdown(
        f"""
            <div class="diagnosis-card">

            <div class="diagnosis-title">{diagnosis_index}. {diagnosis}</div> 

            <div class="diagnosis-section">Potential Reason</div>
            <div class="diagnosis-reason">
                {fact["potential_reason"]}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )#use to diaplay the diagnosis number ,disgnosis and the potential reason that also inside the clpis


        #Collect solutions for the corresponding diagnosis
        solutions = []

        for s in env.facts():
            if s.template.name == "solution" and s["diagnosis"] == diagnosis:
                solutions.append(s) 
        #one diagnosis might have multiple solution, insert them all save into "solution"
        solutions.sort(key=lambda x: x["order"])#follow by the number

        if solutions: #make sure solution is valid,not blank
            st.markdown(
                '<div class="solution-block">', 
                unsafe_allow_html=True
            )
    
            st.markdown(
                '<div class="diagnosis-section">Solution</div>', 
                unsafe_allow_html=True
            )#show the title
            
            for sol in solutions:# this is an expander, prevent the whole message display
                with st.expander(sol["title"]):#only display when user click it
                    st.markdown("**Step:**")#showing the step that take from clips
                    for i, step in enumerate(sol["steps"], 1):
                        st.write(f"{i}. {step}")
            
        st.markdown(
            '<hr class="diagnosis-divider">', 
            unsafe_allow_html=True
        )#make a segment

        diagnosis_index += 1 #next disgnosis, and repeat the loop

def active_expert_system():#main system
    mode = st.session_state.mode #if first time coming, above will let it = welcome. If not, go to the corresponding page

    # ======================
    #PAGE 1: MENU
    # ======================
    if mode == "welcome": #first time, show the welcome page
        st.markdown(
            "<div class='page'>"
                "<h2 class='welcome-hero'>Welcome to Fault Diagnosis for Perodua Myvi</h2>"
                "<div class='welcome-title'></div>"
                "<p class='welcome-subtitle'>"
                "An expert system for diagnosing common vehicle faults based on observed symptoms.<br>Answer a series of simple questions to identify possible causes and recommended solutions."
                "<br><br>"
                "Click <strong>Start</strong> to begin the diagnosis process."
                "</p>"
            "</div>",
            unsafe_allow_html=True
        )#some intro 

        col1, col2, col3 = st.columns([2, 1, 2]) # make 3 column

        with col2:#only column 2/mid display the start button
            if st.button("Start"):
                st.session_state.has_started = True
                st.session_state.mode = "menu"
                st.rerun()

        return #once user press button start,mode will= menu, and rerun the page to direct to menu page

    if mode == "menu": #menu page
        st.markdown(
            '<h2 class="menu-title">Fault Diagnosis for Perodua Myvi</h2>',
            unsafe_allow_html=True
        )#title

        st.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True) #segment

        st.markdown(
            '<p class="menu-instruction">'
            'Select a fault category to begin the diagnosis process.'
            '</p>',
            unsafe_allow_html=True
        )#some instruction

        st.markdown(
            """
            <ul class="menu-category-list">
                <li>1. Electrical Problem</li>
                <li>2. Engine & Fuel</li>
                <li>3. Cooling</li>
                <li>4. Brakes</li>
                <li>5. Tires & Wheels</li>
                <li>6. Transmission</li>
                <li>7. Air Conditioning</li>
                <li>8. Body</li>
                <li>9. Suspension</li>
                <li>10. Steering</li>
                <li>11. Not sure (Comprehensive inspection)</li>
            </ul>
            """,
            unsafe_allow_html=True
        )#using html to display all choice

        choice = st.selectbox(
            "Select a category (1–11):",
            list(range(1, 12)),
            key="menu_choice"
        ) #let user choice the number that correspond to the choice

        if st.button("➡ Continue"): #if press button continue, mode=symptom and let the choice = user choice
            st.session_state.choice = choice
            st.session_state.mode = "symptom"
            st.rerun() #rerun the page 

        st.markdown('</div>', unsafe_allow_html=True)

    # ======================
    #PAGE 2: SYMPTOMS
    # ======================
    
    elif mode == "symptom":#after user choice the category
        if "answers" not in st.session_state: #declare the "answer"
            st.session_state.answers = {}

        env.reset() #reset the clips environment to prevent the previous facts affect
        choice = st.session_state.choice #user choice

        match choice: #load the kb and category based on user choice
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
            case 11: #if user not sure and choice all, load all
                kb.load_all()
                category = ""

        env.reset()#reset environment again for double confirm previous facts will not affect
        questions = ask_symptom(category)#extract the question from kb
        error_box = st.empty()

        st.markdown(
            '<h3 class="symptom-title">Symptom Checklist</h3>',
            unsafe_allow_html=True
        )#display title

        st.markdown(
            '<p class="symptom-instruction">'
            'Please answer the following questions based on your vehicle condition.'
            '</p>',
            unsafe_allow_html=True
        )#instruction
        num = 1 #question number
        all_answered = True

        for symptom_name, sentence, images in questions: #display all question
            prev = st.session_state.answers.get(symptom_name) #if user back, display the previos choice
            question_image(
                f"Q{num}. {sentence}",
                images
            )#display question and picture
            choice = st.radio(
                label="dummy",
                options=["YES", "NO"],
                index=(
                    0 if prev == "YES"
                    else 1 if prev == "NO"
                    else None
                ),
                key=f"sym_{symptom_name}",
                horizontal=True,
                label_visibility="collapsed"
            )# provide yes or no to choose, if previous have choose, then display previous one
            st.markdown("<div class='radio-tight'></div>", unsafe_allow_html=True)

            if choice is None:#make sure all the question choose yes or no. If have question haven fill in, all answer set to false
                all_answered = False

            num = num + 1 #next question
            st.session_state.answers[symptom_name] = choice #save the user answer 
        error_box = st.empty()
        col1, _, col2 = st.columns([1, 4, 1]) #creat column

        with col1:#column 1 provide the back button to direct to menu 
            if st.button("⬅ Back"):
                st.session_state.mode = "menu"
                st.rerun()
        
        submit_clicked = False #set false first

        with col2:#column 2 is button submit
            submit_clicked = st.button("Submit") #set submit_clicked to true

        if submit_clicked:#if click submit
            if not all_answered:#if have question haven fill in
                error_box.error(
                    "Please answer ALL symptom questions before continuing."
                )#display the error
            else:#all question fill in
                error_box.empty()
                st.session_state.mode = "result" #direct to next result page
                st.rerun()#rerun page

        st.markdown('</div>', unsafe_allow_html=True)

    # ======================
    # PAGE 3: RESULT
    # ======================
    elif mode == "result":#if result page
        st.markdown(
            '<h3 class="result-title">Diagnosis Result</h3>',
            unsafe_allow_html=True
        )#title

        st.markdown(
            '<div class="result-divider"></div>',
            unsafe_allow_html=True
        )#segment
        env.reset()
        kb.load_all()

        for symptom_name, ans in st.session_state.answers.items(): #view all the user answer by question
            if ans == "YES": #if answer = yes
                env.assert_string(
                    f"(symptom (name {symptom_name}) (value yes))") #the question answer= yes

        env.run()#and run the clips
        has_response = any(
                fact.template.name == "response"
                for fact in env.facts()
            )#checking is there have response result or not

        if has_response:# if yes,run function to display
            run_inference()
        else:#if no result
            st.warning("No Diagnosis Found")
            st.info(
                "The selected symptoms do not satisfy any predefined diagnosis rules.\n\n"
                "This may indicate:\n"
                "- The condition is uncommon\n"
                "- Insufficient or conflicting symptoms\n"
                "- Multiple minor issues\n\n"
            )

        rcol1, _, rcol2 = st.columns([1, 4, 1]) #creat colum

        with rcol1:#display back button to go back to symtom page
            if st.button("⬅ Back"):
                st.session_state.mode = "symptom"
                st.rerun()

        with rcol2:#if click home than go to menu page
            if st.button("Home"):
                st.session_state.mode = "menu"
                st.session_state.pop("answers", None)
                st.session_state.pop("choice", None)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)


active_expert_system()#run the system
