# Moto G sensors → the organism's field/sensory cell (Fable, 2026-06-16)

The Moto G isn't just another node — wired to its sensors (via **Termux:API**), it becomes the organism's
**sensory cell**: energy, motion, location, sight, sound. Biological framing made literal.

## Energy / metabolism (the best one — ties straight to the dashboard)
- **Battery = metabolism vital.** Feed `termux-battery-status` into the organism dashboard as the Moto
  cell's real energy level. Low battery → cell throttles to cheap-only or sleeps. Plugged in → full
  metabolism. The dashboard's "energy flow" section becomes literally true.
- **Charging + still + dark + on wifi = run the heavy loop.** The phone's own sensors decide the metabolic
  schedule: when it's charging on the nightstand, Badass Fable runs research cycles hard and pushes to
  GitHub; when it's in a pocket on a job, it goes quiet. Self-pacing 24/7 from real signals.

## Motion / presence
- **Accelerometer = activity rhythm.** Moving (driving to a fence job) vs still (charging) tells the cell
  when to work vs rest — no manual scheduling.
- **Light + proximity = "the organism notices you."** Pick up the phone → agent wakes and surfaces the
  day's findings / pending approvals. Put it down → it goes back to background.

## Field cell (ties to BidLocal / TradeApp / ProTrust)
- **GPS = job-site truth.** On a contractor site, geotag the job; "you're at a customer location — log
  this job?" The Moto becomes BidLocal's field-truth capture device.
- **Camera = proof photos.** Snap the fence/work → Badass Fable documents it as a ProTrust proof receipt.
- **Mic = voice field notes.** Speak the job details → transcribed + structured locally into a job card.
  Voice-first contractor capture, exactly the TradeApp thesis.

## Wildcards
- **Magnetometer/compass + GPS → OpenGoldSDR tie-in.** You already have the gold-prospecting repo — the
  phone's magnetometer is a real EM sensor for that project; the Moto cell could log field readings.
- **Notifications sensor.** `termux-notification-list` → the agent sees what's hitting your phone and can
  triage/summarize (gated, read-only).
- **Ambient → mood/context.** Light + motion + time → the agent picks tone/urgency (quiet at night).

## Mechanism + gates
- Termux:API package (`pkg install termux-api`) + the Termux:API app exposes all of the above as CLI
  commands the Moto loop calls.
- Privacy gates: camera/mic/location are sensitive — each is **opt-in per use, never always-on
  recording**, nothing leaves the phone without Jeff, and raw media stays local. The agent gets *signals*
  (battery %, moving y/n, at-a-saved-location y/n), not a surveillance feed.

## First build (cheap, high-signal)
1. `termux-battery-status` → organism dashboard energy vital + the charging-based loop scheduler.
   (Makes the dashboard's metabolism real AND gives the 24/7 loop a smart on/off trigger.)
2. Then GPS job-tagging + camera proof for the BidLocal field cell.
