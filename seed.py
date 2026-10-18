"""
Database seeding script for FixMyCar AI.
Populates the 8 core repair guides and their detailed step-by-step instructions.
Idempotent: will not create duplicate records when run multiple times.
"""

from app import create_app
from models import db, Repair, RepairStep

SEED_REPAIRS = [
    {
        "title": "Engine Oil Change",
        "slug": "engine-oil-change",
        "category": "Maintenance",
        "difficulty": "Beginner",
        "estimated_minutes": 45,
        "description": "Regular engine oil and filter changes are the single most critical maintenance task to prolong your engine's lifespan, maintain efficiency, and prevent premature wear of internal rotating components.",
        "required_tools": "Jack and rated jack stands (or ramps), Oil drain pan (at least 6-8 qt capacity), Socket wrench and oil drain plug socket, Oil filter wrench (strap or cup type), Clean funnel, Fresh engine oil (consult owner's manual for exact viscosity & spec), New OEM or premium oil filter, New crush washer for drain plug, Clean shop rags / paper towels, Heavy nitrile gloves, Safety glasses",
        "safety_warning": "CRITICAL SAFETY WARNING: NEVER work underneath a vehicle supported only by a hydraulic or scissor jack. Always secure the vehicle on heavy-duty, properly rated jack stands with wheel chocks on the ground wheels. Engine oil can reach over 200°F (93°C) and cause severe thermal burns; allow the engine to cool down to lukewarm before draining. Dispose of used oil and filter responsibly at an authorized recycling center or auto parts store.",
        "steps": [
            {
                "step_number": 1,
                "title": "Warm Engine Slightly & Prepare Workspace",
                "description": "Park your vehicle on a flat, solid, level surface. Engage the emergency parking brake firmly and place wheel chocks behind the rear wheels. Run the engine for 3 to 5 minutes so the oil warms up and suspends contaminants, allowing it to drain out smoothly and completely.",
                "warning": "Do not let the engine run to full operating temperature. Hot oil and exhaust pipes can cause severe burns."
            },
            {
                "step_number": 2,
                "title": "Safely Raise and Support Vehicle",
                "description": "Using a rated hydraulic floor jack on the manufacturer-designated front jacking point, raise the front of the vehicle. Position heavy-duty jack stands under the factory pinch welds or frame support points. Slowly lower the jack until the car rests completely on the stands. Shake the vehicle firmly with your hands from the fender to confirm absolute stability before getting underneath.",
                "warning": "NEVER crawl under a car supported only by a jack. If the vehicle wobbles, reposition your jack stands immediately."
            },
            {
                "step_number": 3,
                "title": "Locate Oil Drain Plug and Position Pan",
                "description": "Crawl underneath and locate the engine oil pan. Identify the oil drain bolt (located at the bottom or rear face of the oil pan). Slide your drain pan directly underneath, offsetting it slightly backward to anticipate the trajectory of the oil stream when the bolt is released.",
                "warning": "Make sure you are loosening the engine oil pan, not the transmission fluid pan or differential."
            },
            {
                "step_number": 4,
                "title": "Loosen and Remove Oil Drain Plug",
                "description": "Put on safety glasses and nitrile gloves. Fit the correct size box wrench or socket onto the drain plug and turn counterclockwise to break it loose. Once loose, unthread the bolt by hand while applying inward pressure toward the pan. When you reach the last thread, quickly pull the bolt away to let the oil stream drain into the catch pan. Allow the oil to drain for 10 to 15 minutes until it slows to a faint drip.",
                "warning": "Wear protective gloves and eye protection. Keep your face clear of the drain path."
            },
            {
                "step_number": 5,
                "title": "Install New Crush Washer and Reinstall Drain Plug",
                "description": "Wipe the drain plug clean and inspect its threads. Remove the old crushed washer and discard it. Slide a brand-new metal or copper crush washer onto the bolt. Clean the mating surface on the oil pan with a shop rag. Thread the drain bolt in by hand for several turns to prevent cross-threading. Tighten with your socket wrench to the vehicle's factory torque specification (typically 25–35 ft-lbs; consult your owner's manual).",
                "warning": "Do not overtighten or strip the aluminum threads of the oil pan."
            },
            {
                "step_number": 6,
                "title": "Locate and Remove Old Oil Filter",
                "description": "Reposition your drain pan beneath the oil filter. Fit your filter wrench onto the filter canister and loosen it counterclockwise. Once loose, unscrew the filter by hand, keeping it upright as much as possible because it will be filled with oil. Dump the contents into the drain pan. Inspect the old filter's mounting face to ensure the black rubber O-ring came off with it and is not stuck to the engine block.",
                "warning": "A 'double gasket' (leaving the old O-ring stuck to the engine) will cause catastrophic oil blowout and instant engine failure upon starting."
            },
            {
                "step_number": 7,
                "title": "Prep and Install New Oil Filter",
                "description": "Clean the engine filter mounting surface with a clean cloth. Dip your clean gloved finger into fresh engine oil and smear a thin, even coat over the rubber gasket of the new filter. If your filter mounts vertically, pre-fill it halfway with fresh oil. Screw the new filter onto the threaded stud by hand. Once the rubber gasket contacts the engine surface, hand-tighten an additional 3/4 to 1 full turn. Do NOT use a filter wrench to tighten.",
                "warning": "Never use tools to overtighten an oil filter. Hand-tight is sufficient and preserves the gasket seal."
            },
            {
                "step_number": 8,
                "title": "Fill Engine with Fresh Oil",
                "description": "Remove your tools and drain pan from under the car. Safely raise the car off the jack stands, remove the stands, and lower the vehicle back down to level ground. Open the hood, remove the oil filler cap on top of the engine, and place a clean funnel into the opening. Pour in the manufacturer-recommended oil volume (consult your manual for capacity and viscosity, e.g. 0W-20 or 5W-30), stopping half a quart short of capacity to avoid overfilling. Replace the oil cap securely.",
                "warning": "Overfilling engine oil can cause aeration and foaming, leading to oil starvation and seal damage."
            },
            {
                "step_number": 9,
                "title": "Verify Level, Inspect for Leaks & Reset Service Monitor",
                "description": "Start the engine and let it idle for 60 seconds. Confirm that the dashboard oil pressure warning light extinguishes within 3 seconds. Check underneath the vehicle for any leaks around the drain plug or filter. Turn off the engine, wait 3 minutes for oil to settle into the pan, pull out the oil dipstick, wipe it clean, reinsert fully, and pull it out again. Ensure the oil level is between the MIN and MAX marks. Add small increments if needed. Finally, reset your in-cabin oil life monitor according to your vehicle's handbook.",
                "warning": "If the oil light stays illuminated after 5 seconds, shut the engine off immediately and check oil level and filter installation."
            }
        ]
    },
    {
        "title": "Replace Engine Air Filter",
        "slug": "replace-engine-air-filter",
        "category": "Maintenance",
        "difficulty": "Beginner",
        "estimated_minutes": 15,
        "description": "A clean engine air filter ensures optimal combustion airflow, maintains fuel economy, and prevents abrasive airborne dirt and grit from entering the engine cylinders.",
        "required_tools": "New engine air filter matching vehicle OEM specifications, Flathead or Phillips screwdriver (if housing uses screws), Clean shop towel",
        "safety_warning": "Ensure the engine is completely shut off and cool. Take extreme care not to drop screws, clips, or loose debris into the open air intake tract leading to the throttle body, as foreign objects entering the intake can cause catastrophic engine damage.",
        "steps": [
            {
                "step_number": 1,
                "title": "Locate Air Filter Housing",
                "description": "Open your hood and locate the black plastic air filter box. It is typically positioned on either the driver or passenger side of the engine bay, connected to a wide accordion intake duct leading to the engine throttle body.",
                "warning": "Ensure ignition is switched off and key is removed."
            },
            {
                "step_number": 2,
                "title": "Open Housing Clips or Screws",
                "description": "Inspect the perimeter of the air box. Most vehicles use 2 to 4 metal spring clips that can be unlatched with your fingers. Others use Phillips-head screws or 8mm bolts. Unlatch all clips or loosen screws without removing screws completely if they are captive.",
                "warning": "Hold onto loose screws securely so they don't drop into the lower engine bay."
            },
            {
                "step_number": 3,
                "title": "Remove Old Air Filter and Inspect",
                "description": "Lift the upper lid of the air box slightly. Slide out the old pleated paper or synthetic air filter. Note the orientation of the pleats and perimeter rubber sealing edge. Inspect the filter by holding it up to the sun: if light cannot pass through and pleats are packed with dirt and debris, replacement is necessary.",
                "warning": "Do not allow dirt from the old filter to fall into the clean side of the intake housing."
            },
            {
                "step_number": 4,
                "title": "Clean Air Box Interior",
                "description": "Look inside the bottom tray of the air filter box. You will often find trapped leaves, pine needles, or sand. Use a clean shop towel (or a vacuum) to carefully remove all loose debris from the lower box. Do NOT wipe debris into the clean intake tube.",
                "warning": "Ensure the clean intake duct remains covered while vacuuming or cleaning."
            },
            {
                "step_number": 5,
                "title": "Seat New Air Filter",
                "description": "Place the new replacement air filter into the lower housing tray. Ensure the rubber perimeter seal fits snugly into the housing groove all the way around with no crimps, bends, or gaps.",
                "warning": "A poorly seated filter allows unfiltered dirty air to bypass directly into the engine."
            },
            {
                "step_number": 6,
                "title": "Close and Fasten Housing",
                "description": "Lower the air box cover, aligning the rear hinge tabs into their slots first. Press down firmly and re-fasten the metal clips or tighten screws evenly. Give the box a gentle tug to verify it is sealed airtight.",
                "warning": "Verify all clips are fully clamped so the lid cannot vibrate loose during driving."
            }
        ]
    },
    {
        "title": "Replace Cabin Air Filter",
        "slug": "replace-cabin-air-filter",
        "category": "Maintenance",
        "difficulty": "Beginner",
        "estimated_minutes": 20,
        "description": "The cabin air filter purifies the air entering your vehicle's heating, ventilation, and air conditioning (HVAC) system, removing pollen, dust, soot, and allergens from passenger compartment air.",
        "required_tools": "New vehicle-specific cabin air filter (HEPA or activated carbon recommended), Small flathead screwdriver (if retaining pins are used), Flashlight or work light",
        "safety_warning": "Work gently with plastic glove box tabs and damper arms. Forced plastic clips can snap easily in cold weather. Wear a dust mask if you suffer from severe dust or pollen allergies.",
        "steps": [
            {
                "step_number": 1,
                "title": "Empty and Disengage Glove Compartment",
                "description": "Open your passenger glove box and remove all contents. On the right exterior side, unhook the plastic damper cord or strut if equipped. Then gently push both sides of the glove box inward to allow the stop tabs to clear the dashboard frame, letting the glove box swing down toward the floorboard.",
                "warning": "Do not force plastic tabs. If stiff, apply gentle inward pressure on each side sequentially."
            },
            {
                "step_number": 2,
                "title": "Locate Cabin Filter Access Door",
                "description": "Shine a flashlight into the space behind the glove box. Locate the rectangular plastic access door in the blower motor housing duct.",
                "warning": "Be careful around wiring harnesses and avoid pulling any electrical connectors."
            },
            {
                "step_number": 3,
                "title": "Remove Access Door",
                "description": "Squeeze the retaining tabs on the left and right sides of the cover (or unclip the top latches) and pull the door straight off to expose the filter element.",
                "warning": "Set the access door aside safely so the locking tabs do not bend or crack."
            },
            {
                "step_number": 4,
                "title": "Slide Out Old Filter & Note Airflow Direction",
                "description": "Slide the old cabin filter straight out. IMPORTANT: Look closely at the printed airflow indicator arrow on the edge of the filter frame (usually pointing DOWN toward the blower motor). Note this direction carefully.",
                "warning": "Keep old filter level as you pull it out to avoid dumping trapped leaves onto the car carpet."
            },
            {
                "step_number": 5,
                "title": "Inspect Blower Housing & Clean",
                "description": "Shine your light into the empty cavity. Remove any dried leaves, twigs, or dirt from the top of the blower wheel using a shop towel or narrow vacuum nozzle.",
                "warning": "Ensure the climate blower fan is turned completely off."
            },
            {
                "step_number": 6,
                "title": "Insert New Filter and Reassemble",
                "description": "Orient your new cabin filter so its printed airflow arrows match the original direction. Slide the filter smoothly into the channel without crushing the pleats. Snap the access door back into place until it clicks. Lift the glove box, re-engage the side stops, and reattach the damper cord.",
                "warning": "Installing the filter upside down will restrict HVAC airflow and reduce heating/AC efficiency."
            }
        ]
    },
    {
        "title": "Replace Car Battery",
        "slug": "replace-car-battery",
        "category": "Electrical",
        "difficulty": "Beginner",
        "estimated_minutes": 30,
        "description": "Replace an aging or failing 12V automotive starting battery to restore reliable engine cranking and protect your vehicle's sensitive electrical components.",
        "required_tools": "New 12V automotive battery (correct group size and terminal orientation), 10mm socket or box wrench (or vehicle specific terminal size), Battery hold-down bracket wrench/socket, Wire terminal cleaning brush, Baking soda & water solution, Dielectric terminal protectant grease, Safety goggles, Heavy rubber or nitrile gloves",
        "safety_warning": "CRITICAL HAZARD: Automotive lead-acid batteries contain corrosive sulfuric acid and emit explosive hydrogen gas. Always wear eye protection and gloves. Always disconnect the NEGATIVE (-) terminal first and reconnect it LAST. Never allow a wrench to bridge the positive terminal to any bare metal car body.",
        "steps": [
            {
                "step_number": 1,
                "title": "Turn Off Ignition and Set Brake",
                "description": "Park on a flat surface, apply the parking brake firmly, and switch off the ignition. Remove the key and let all onboard computers shut down for 3 to 5 minutes. Turn off all lights, radios, and accessories.",
                "warning": "Removing battery while ignition is ON can damage sensitive engine control modules (ECUs)."
            },
            {
                "step_number": 2,
                "title": "Put on Safety Gear and Locate Battery",
                "description": "Put on wrap-around safety glasses and gloves. Pop the hood and identify the battery. Identify the positive terminal (marked with a '+' and red cover) and negative terminal (marked with a '-' and black cover).",
                "warning": "Corrosive acid residue can burn skin and eat through clothing."
            },
            {
                "step_number": 3,
                "title": "Disconnect the NEGATIVE (-) Terminal First",
                "description": "Loosen the nut on the black NEGATIVE (-) terminal clamp using a 10mm socket or wrench. Once loose, twist the clamp back and forth gently and lift it off the battery post. Tuck the negative cable far away from the battery so it cannot spring back and touch the terminal.",
                "warning": "ALWAYS disconnect NEGATIVE first. This removes ground potential, eliminating hazardous short-circuit sparks."
            },
            {
                "step_number": 4,
                "title": "Disconnect the POSITIVE (+) Terminal Second",
                "description": "Flip back the red protective cap on the POSITIVE (+) terminal. Loosen the clamp nut, twist the clamp free, and lift it off. Push the cable aside.",
                "warning": "Ensure the positive cable clamp does not touch any exposed metal frame or engine parts."
            },
            {
                "step_number": 5,
                "title": "Remove Battery Hold-Down Bracket",
                "description": "Unbolt the retaining bracket or bottom clamp that locks the battery into the battery tray. Set the bracket, bolts, and washers aside.",
                "warning": "Hold onto bolts carefully so they do not fall down into the engine belly pan."
            },
            {
                "step_number": 6,
                "title": "Lift Out Old Battery",
                "description": "Batteries weigh between 35 and 50 pounds. Use the built-in carrying handle (or grip firmly from opposite bottom corners) and lift straight up out of the engine bay keeping your back straight. Set the old battery upright on the ground.",
                "warning": "Never tip a standard flooded battery on its side as acid may leak from vent caps."
            },
            {
                "step_number": 7,
                "title": "Clean Battery Tray and Terminal Clamps",
                "description": "Inspect the tray and wire clamps for powdery white or greenish corrosion. Scrub the cable clamps with a wire terminal brush until shiny bare metal is exposed. Clean tray with baking soda and water if residue exists.",
                "warning": "Corroded connections create high electrical resistance and cause starting failures."
            },
            {
                "step_number": 8,
                "title": "Install New Battery and Secure Bracket",
                "description": "Lower the new battery into the tray, ensuring the positive and negative posts face the identical direction as the old battery. Reinstall the hold-down bracket and tighten the bolts until the battery is snug and cannot shift or slide when pushed by hand.",
                "warning": "A loose battery can bounce while driving, damaging internal plates or shorting against the hood."
            },
            {
                "step_number": 9,
                "title": "Connect POSITIVE (+) Terminal First",
                "description": "Remove the protective plastic transport cap from the positive terminal. Slide the red positive cable clamp over the post until fully seated at the base. Tighten the clamp nut firmly. Apply a protective coat of dielectric grease or battery terminal protector spray.",
                "warning": "Ensure clamp is fully seated down onto the tapered post before tightening."
            },
            {
                "step_number": 10,
                "title": "Connect NEGATIVE (-) Terminal Last & Test",
                "description": "Remove the transport cap from the negative post. Slide the black negative clamp onto the post (a tiny spark is normal as internal electronics wake up). Tighten the nut securely so the clamp cannot be twisted by hand. Close the hood, enter the vehicle, and start the engine to confirm solid cranking.",
                "warning": "Never connect cables in reverse polarity, which can instantly blow high-amperage main fuses and destroy vehicle electronics."
            }
        ]
    },
    {
        "title": "Replace Brake Pads",
        "slug": "replace-brake-pads",
        "category": "Brakes",
        "difficulty": "Intermediate",
        "estimated_minutes": 90,
        "description": "Step-by-step procedure for safely inspecting and replacing worn front or rear disc brake pads to maintain stopping power, avoid rotor damage, and eliminate brake squeal.",
        "required_tools": "New set of axle brake pads, Hydraulic floor jack and rated jack stands, Wheel chocks, Lug nut wrench or breaker bar with socket, Caliper slide pin socket/wrench (commonly 7mm hex, 12mm, or 14mm), C-clamp or caliper piston compressor tool, Brake caliper hanger wire or bungee cord, Brake parts cleaner spray, High-temperature ceramic brake grease, Wire brush, Torque wrench, Nitrile gloves, Dust mask",
        "safety_warning": "CRITICAL SAFETY WARNING: Brakes are the most critical safety system on your vehicle. If you lack mechanical experience or confidence, seek assistance from a certified professional. NEVER press the brake pedal while a caliper is dismounted. NEVER let a caliper dangle by the flexible rubber brake hose. Always torque wheel lug nuts in a criss-cross star pattern to specification.",
        "steps": [
            {
                "step_number": 1,
                "title": "Loosen Lug Nuts on Ground",
                "description": "Park on level concrete, set the parking brake, and chock the opposite wheels. With the vehicle still on the ground, use your lug wrench or breaker bar to break the wheel lug nuts loose by one half turn counterclockwise. Do not remove them yet.",
                "warning": "Attempting to loosen tight lug nuts while the car is raised on jack stands can dangerously shake the vehicle off its supports."
            },
            {
                "step_number": 2,
                "title": "Raise Vehicle, Support on Stands & Remove Wheel",
                "description": "Jack up the vehicle using approved structural lift points. Rest the car securely onto rated jack stands. Remove the loosened lug nuts and pull off the wheel to expose the brake rotor and caliper assembly.",
                "warning": "Always verify jack stand stability before working near the wheel wells."
            },
            {
                "step_number": 3,
                "title": "Clean Brake Assembly with Brake Cleaner",
                "description": "Generously spray down the caliper, rotor, and surrounding hardware with aerosol brake cleaner into a catch pan. Allow it to air dry.",
                "warning": "Never use compressed air on brake assemblies. Avoid inhaling brake dust particles."
            },
            {
                "step_number": 4,
                "title": "Remove Caliper Slide Pin Bolts",
                "description": "Locate the upper and lower caliper slide pin bolts (often concealed under small plastic dust caps on the backside of the caliper). Use the appropriate hex key or box wrench to remove both bolts.",
                "warning": "Inspect rubber slide pin dust boots for tears or cracks; replace if damaged."
            },
            {
                "step_number": 5,
                "title": "Dismount and Hang Caliper Securely",
                "description": "Gently wiggle the caliper free from the rotor. Immediately hook a metal coat hanger or mechanic's bungee cord through the caliper body and suspend it from the suspension coil spring.",
                "warning": "NEVER allow the heavy brake caliper to hang by the hydraulic rubber brake hose; doing so can cause internal hose rupture and total brake failure."
            },
            {
                "step_number": 6,
                "title": "Remove Old Pads and Hardware Clips",
                "description": "Slide the inner and outer brake pads out of the caliper mounting bracket. Pop off the stainless steel abutment clips (slide hardware). Note the location of the mechanical wear indicator squealer tab on the inner pad.",
                "warning": "Compare old pads against new pads to confirm identical backing plate geometry and dimensions."
            },
            {
                "step_number": 7,
                "title": "Clean Bracket & Install New Stainless Clips",
                "description": "Use a stiff wire brush to clean rust scale out of the pad sliding channels on the bracket. Snap in the brand-new stainless steel hardware clips included with your pad set. Apply a micro-thin layer of high-temperature ceramic brake grease onto the pad contact slide points.",
                "warning": "Do NOT get any grease or oil onto the friction surface of the brake pads or the rotor face."
            },
            {
                "step_number": 8,
                "title": "Compress Caliper Piston",
                "description": "Open your engine hood and remove the cap from the brake fluid master cylinder reservoir. Place one of the old brake pads flat across the circular caliper piston face. Use a large C-clamp or piston compression tool to slowly and steadily push the piston back until flush with the caliper housing, watching the fluid level in the master cylinder reservoir so it does not overflow.",
                "warning": "Rear calipers with integrated parking brakes often require a specialized rotational cube tool to twist and push the piston simultaneously."
            },
            {
                "step_number": 9,
                "title": "Install New Pads and Re-mount Caliper",
                "description": "Slide the new inner and outer brake pads into the bracket clips. Unhook the caliper, slide it over the new thicker pads, reinstall the slide pin bolts, and torque to manufacturer specification (typically 20–30 ft-lbs). Reinstall dust caps.",
                "warning": "Ensure the rubber slide pin boots are not pinched or twisted under the caliper ears."
            },
            {
                "step_number": 10,
                "title": "Reinstall Wheel and PUMP BRAKE PEDAL BEFORE DRIVING",
                "description": "Remount the wheel, hand-thread lug nuts, lower vehicle to the ground, and torque lug nuts in a star pattern to spec with a torque wrench. CRITICAL FINAL STEP: Before starting the engine or shifting into gear, depress the brake pedal firmly 4 to 5 times until it becomes solid and firm to seat the pads against the rotor.",
                "warning": "CRITICAL: If you do not pump the brake pedal before driving, you will have ZERO braking power the first time you step on the pedal!"
            }
        ]
    },
    {
        "title": "Replace Brake Discs",
        "slug": "replace-brake-discs",
        "category": "Brakes",
        "difficulty": "Intermediate",
        "estimated_minutes": 120,
        "description": "Comprehensive guide to removing grooved, warped, or undersized brake rotors and installing brand-new precision brake discs alongside new brake pads.",
        "required_tools": "Pair of new brake rotors, Heavy-duty breaker bar and socket set, Medium-strength threadlocker (Blue), Dead-blow mallet or heavy hammer, Stiff wire brush / drill wire wheel, Brake parts cleaner spray, Anti-seize compound, Caliper hanger wire, Floor jack & jack stands, Precision torque wrench",
        "safety_warning": "Brake rotors must always be replaced in pairs across the axle. Never replace just one side. Bracket mounting bolts are torqued extremely tight from the factory and require proper leverage. Wear safety goggles when cleaning rust scale.",
        "steps": [
            {
                "step_number": 1,
                "title": "Support Vehicle and Remove Caliper",
                "description": "Safely elevate and support the car on jack stands. Remove the wheel, remove the caliper slide bolts, and suspend the caliper securely from the suspension spring with a wire hanger.",
                "warning": "Never let caliper hang by rubber brake line."
            },
            {
                "step_number": 2,
                "title": "Remove Caliper Mounting Bracket",
                "description": "Locate the two large, heavy bolts on the back of the steering knuckle holding the caliper torque bracket in place. Use a 1/2-inch drive breaker bar and proper socket to break both bolts loose and remove the bracket.",
                "warning": "These bolts are tightened to high torque (often 70-100+ ft-lbs). Ensure your socket fits snugly to avoid rounding bolt heads."
            },
            {
                "step_number": 3,
                "title": "Remove Rotor Retaining Screws",
                "description": "Check if your rotor has 1 or 2 small countersunk Phillips or Torx screws on the face of the rotor hat holding it to the hub. If stuck, use an impact screwdriver with a hammer strike to break them loose without stripping.",
                "warning": "Stripping these soft screws requires drilling them out. Use an impact driver."
            },
            {
                "step_number": 4,
                "title": "Free and Remove Old Rotor",
                "description": "Pull the old rotor straight off the wheel studs. If seized by rust to the wheel hub center, strike the flat face between the wheel studs with a heavy dead-blow mallet, or thread 8mm bolts into the threaded removal holes on the rotor face until it pops loose.",
                "warning": "Wear eye protection. Rust and metal debris will fly loose when tapping."
            },
            {
                "step_number": 5,
                "title": "Thoroughly Clean Wheel Hub Mating Surface",
                "description": "Use a wire brush or wire cup wheel on a drill to scrub every trace of rust and corrosion off the flat face of the wheel hub. The hub face must be completely flat and clean down to bare metal. Wipe clean and apply an extremely light film of anti-seize around the center hub pilot ring only.",
                "warning": "Even 0.002 inches of rust grit trapped between hub and rotor causes severe brake pedal pulsation and steering wheel shudder."
            },
            {
                "step_number": 6,
                "title": "Degrease New Rotor",
                "description": "New brake rotors are shipped coated in cosmoline or protective oil to prevent rust during storage. Generously spray both sides of the new rotor with brake cleaner and wipe completely dry with clean lint-free paper towels until no oily residue remains.",
                "warning": "Failing to clean shipping oil off rotors will contaminate new brake pads immediately, ruining stopping power."
            },
            {
                "step_number": 7,
                "title": "Mount New Rotor on Hub",
                "description": "Slide the clean new rotor over the wheel studs flush against the hub face. Reinstall the retaining screw if equipped, or thread a lug nut hand-tight against a washer to hold the rotor flat while reassembling the bracket.",
                "warning": "Verify rotor seats completely flat against the scrubbed hub."
            },
            {
                "step_number": 8,
                "title": "Reinstall Caliper Bracket with Threadlocker",
                "description": "Clean the threads of the caliper bracket bolts. Apply 2 drops of blue medium-strength threadlocker to the threads. Fit the bracket over the new rotor and torque bolts to the vehicle manufacturer specification using a torque wrench.",
                "warning": "Caliper bracket bolts must be torqued to exact spec. Loose bracket bolts will cause catastrophic brake failure."
            },
            {
                "step_number": 9,
                "title": "Reassemble Pads, Caliper, and Test",
                "description": "Install new brake pads into the bracket, remount the caliper, torque slide pins, and mount the wheel. Torque lug nuts to spec, pump the brake pedal 4-5 times until firm, and perform a brake bedding procedure (5-6 moderate slowdowns from 45 mph to 15 mph with cooling periods).",
                "warning": "Avoid aggressive emergency braking for the first 100 miles while new pads and rotors bed into each other."
            }
        ]
    },
    {
        "title": "Replace Windshield Wipers",
        "slug": "replace-windshield-wipers",
        "category": "Maintenance",
        "difficulty": "Beginner",
        "estimated_minutes": 15,
        "description": "Quickly replace streaking, squeaking, or cracked windshield wiper blades to maintain crystal-clear visibility during rain, snow, and severe weather.",
        "required_tools": "Pair of vehicle-specific wiper blades (driver and passenger lengths often differ), Thick folded microfiber towel or piece of cardboard, Glass cleaner",
        "safety_warning": "CRITICAL HAZARD: Always place a thick folded towel or dense cardboard directly against the windshield glass underneath the wiper arm. The spring-loaded metal wiper arm can violently snap down onto the windshield if released without a blade, instantly cracking or shattering the glass.",
        "steps": [
            {
                "step_number": 1,
                "title": "Protect the Windshield Glass",
                "description": "Lay a thick folded bath towel, shop towel, or folded cardboard directly on the windshield beneath both wiper arms. This acts as a shock absorber in case an arm snaps down accidentally.",
                "warning": "Never skip this step. A snapped bare metal wiper arm can crack a \$500-\$1,200 windshield in a millisecond."
            },
            {
                "step_number": 2,
                "title": "Lift Wiper Arm into Service Position",
                "description": "Gently lift the driver-side wiper arm away from the glass until it clicks into its upright service position roughly 90 degrees from the windshield.",
                "warning": "If your car has hidden wipers recessed below the hood edge, activate 'Wiper Service Mode' via your vehicle's settings menu or ignition sequence."
            },
            {
                "step_number": 3,
                "title": "Release Old Wiper Blade",
                "description": "Locate the small locking tab or hinge lever where the wiper blade connects to the metal J-hook arm (or pinch tab on European style blades). Depress the tab with your thumb and slide the wiper blade downward toward the base of the arm until it unhooks.",
                "warning": "Hold onto the metal arm with one hand while manipulating the blade with the other."
            },
            {
                "step_number": 4,
                "title": "Remove Old Blade and Rest Arm",
                "description": "Carefully slide the unhooked blade free. While getting the new blade, gently lower the bare metal arm down to rest on the padded towel. Never leave the bare arm standing vertically unattended.",
                "warning": "Do not let the bare metal hook touch bare glass."
            },
            {
                "step_number": 5,
                "title": "Install New Wiper Blade",
                "description": "Lift the arm, position the new blade's adapter clip into the metal arm hook, and slide it upward firmly until you hear and feel a distinct 'click' locking it into place. Tug gently on the blade to confirm it cannot pull free.",
                "warning": "Ensure the plastic protective sleeve covering the rubber edge is removed after installation."
            },
            {
                "step_number": 6,
                "title": "Repeat for Passenger Side and Test",
                "description": "Repeat the exact process on the passenger side (confirming correct blade length). Remove towels, gently lower arms onto windshield, and test operation using windshield washer spray.",
                "warning": "Do not test dry wipers on dusty glass as it can scratch the windshield."
            }
        ]
    },
    {
        "title": "Change a Headlight Bulb",
        "slug": "change-headlight-bulb",
        "category": "Electrical",
        "difficulty": "Beginner",
        "estimated_minutes": 25,
        "description": "Replace burned-out halogen headlight bulbs to restore crisp nighttime driving illumination and maintain highway safety compliance.",
        "required_tools": "Replacement bulb matching vehicle code (e.g., H7, H11, 9005, 9006), Clean nitrile or cotton gloves, Screwdriver or clip pry tool (if splash shield removal is needed), Dielectric grease",
        "safety_warning": "Halogen bulbs operate under high pressure and become searingly hot in seconds. Allow bulbs to cool completely before touching. NEVER touch the clear quartz glass envelope of a halogen bulb with bare fingers; skin oils create concentrated hot spots that cause the bulb to overheat and shatter prematurely.",
        "steps": [
            {
                "step_number": 1,
                "title": "Turn Off Headlights and Ignition",
                "description": "Switch the headlight switch inside the cabin completely to OFF. Turn off the ignition, remove keys, and let the vehicle sit for 10 minutes to allow hot headlight bulbs to cool down.",
                "warning": "Touching a recently energized bulb can cause immediate skin burns."
            },
            {
                "step_number": 2,
                "title": "Open Hood and Access Bulb Rear",
                "description": "Pop the hood and prop it open. Look behind the headlight assembly on the side with the burned-out bulb. Locate the rear access port. If space is tight, you may need to unclip the air intake duct or washer fluid neck for hand clearance.",
                "warning": "Do not pull or pinch adjacent AC lines or radiator hoses."
            },
            {
                "step_number": 3,
                "title": "Remove Dust Cap / Weather Seal",
                "description": "Most modern headlights feature a round rubber or plastic weather seal cap on the back of the housing. Turn it counterclockwise 1/4 turn or peel back the rubber lip to expose the bulb socket.",
                "warning": "Keep dust caps clean and free of dirt so the housing interior stays moisture-free."
            },
            {
                "step_number": 4,
                "title": "Disconnect Electrical Harness",
                "description": "Locate the plastic electrical wiring plug connected to the bulb base. Press the release tab with your thumb and gently wiggle the connector downward and off the bulb prongs.",
                "warning": "Pull the plastic connector body, never pull on the wires directly."
            },
            {
                "step_number": 5,
                "title": "Unseat and Remove Old Bulb",
                "description": "Depending on vehicle design, either twist the plastic bulb base counterclockwise 1/4 turn to unlock it, or unhook the spring wire retaining clip by pressing and pushing sideways. Carefully withdraw the bulb straight out of the reflector housing.",
                "warning": "Note the orientation of the bulb's alignment tabs for easy insertion of the new bulb."
            },
            {
                "step_number": 6,
                "title": "Prepare New Bulb Wearing Clean Gloves",
                "description": "Put on clean nitrile or cotton gloves. Remove the new bulb from its packaging by handling ONLY the plastic or metal base flange. Inspect the glass to ensure it is pristine.",
                "warning": "If you accidentally touch the glass envelope, wipe it thoroughly with 90%+ isopropyl alcohol and a lint-free cloth before installation."
            },
            {
                "step_number": 7,
                "title": "Insert and Lock New Bulb into Housing",
                "description": "Insert the bulb into the headlight reflector, aligning its indexing tabs with the notches in the socket. Push in flush and twist 1/4 turn clockwise until seated, or swing the metal spring retaining clip back over the flange until it latches.",
                "warning": "Do not force the bulb. It will only seat flush when properly keyed into the indexing notches."
            },
            {
                "step_number": 8,
                "title": "Reconnect Plug, Seal Dust Cap & Test",
                "description": "Reattach the electrical harness connector until it audibly clicks into place. Re-seat the rubber or plastic dust cap securely. Turn on the vehicle headlights to confirm low and high beams operate with correct beam pattern before driving.",
                "warning": "An improperly seated weather seal allows rain and condensation to enter and permanently fog your headlight lens."
            }
        ]
    }
]


def seed_repairs():
    """Seed the database with the initial 8 repair guides and steps."""
    app = create_app()
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        print("Ensured all database tables exist.")

        created_repairs = 0
        created_steps = 0

        for r_data in SEED_REPAIRS:
            existing_repair = Repair.query.filter_by(slug=r_data["slug"]).first()
            if not existing_repair:
                repair = Repair(
                    title=r_data["title"],
                    slug=r_data["slug"],
                    category=r_data["category"],
                    difficulty=r_data["difficulty"],
                    estimated_minutes=r_data["estimated_minutes"],
                    description=r_data["description"],
                    required_tools=r_data["required_tools"],
                    safety_warning=r_data["safety_warning"]
                )
                db.session.add(repair)
                db.session.flush() # Populate repair.id
                created_repairs += 1
            else:
                repair = existing_repair
                # Update core fields if needed
                repair.title = r_data["title"]
                repair.category = r_data["category"]
                repair.difficulty = r_data["difficulty"]
                repair.estimated_minutes = r_data["estimated_minutes"]
                repair.description = r_data["description"]
                repair.required_tools = r_data["required_tools"]
                repair.safety_warning = r_data["safety_warning"]

            for s_data in r_data["steps"]:
                existing_step = RepairStep.query.filter_by(
                    repair_id=repair.id,
                    step_number=s_data["step_number"]
                ).first()

                if not existing_step:
                    step = RepairStep(
                        repair_id=repair.id,
                        step_number=s_data["step_number"],
                        title=s_data["title"],
                        description=s_data["description"],
                        warning=s_data.get("warning")
                    )
                    db.session.add(step)
                    created_steps += 1
                else:
                    existing_step.title = s_data["title"]
                    existing_step.description = s_data["description"]
                    existing_step.warning = s_data.get("warning")

        db.session.commit()
        print(f"Seed completed successfully! Added {created_repairs} new repairs, {created_steps} new steps. Total repairs in DB: {Repair.query.count()}.")


if __name__ == '__main__':
    seed_repairs()
