#!/usr/bin/env python3
# Spend Cell — the "agents that SPEND" organ for the Hermes hackathon.
# Every charge passes the SAME brakes the model calls do (KILLSWITCH + per-lane daily budget),
# then writes a real ledger row. Stripe TEST mode only. No live money. Gated, receipted, reversible.
#
#   python3 spend_cell.py charge 4.20 "NVIDIA NIM credits (test)"   # agent buys a service
#   python3 spend_cell.py earn   9.99 "GrokGo intel subscription"   # revenue in (payment link / test charge)
#
# Reads STRIPE_API_KEY from ~/.config/secrets/stripe-jeffw58325.env (sk_test_...).
import os, sys, time, sqlite3, pathlib, json
ROOT = pathlib.Path(os.environ.get("GROKGO_ROOT", str(pathlib.Path.home() / "grokgo")))
LEDGER = ROOT / "ledger.db"
KILLSWITCH = ROOT / "KILLSWITCH"
ENV = pathlib.Path.home() / ".config/secrets/stripe-jeffw58325.env"
SPEND_LANE = "spend"
DAILY_CAP_USD = 50.0  # hard ceiling for the spend lane, even in test mode

def _key():
    if not ENV.exists():
        sys.exit("no stripe key — create ~/.config/secrets/stripe-jeffw58325.env with STRIPE_API_KEY=sk_test_...")
    for line in ENV.read_text().splitlines():
        if line.startswith("STRIPE_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("STRIPE_API_KEY not found in env file")

def _spent_today(lane):
    c = sqlite3.connect(LEDGER)
    midnight = time.time() - (time.time() % 86400)
    r = c.execute("SELECT COALESCE(SUM(ABS(cost_usd)),0) FROM calls WHERE lane=? AND ts>=?",
                  (lane, midnight)).fetchone()[0]
    c.close()
    return r or 0.0

def _ledger(task_id, ttype, amount_usd, status):
    c = sqlite3.connect(LEDGER)
    c.execute("INSERT INTO calls VALUES (?,?,?,?,?,?,?,?,?,?)",
              (time.time(), SPEND_LANE, task_id, ttype, "stripe", "stripe-test",
               0, 0, amount_usd, status))
    c.commit(); c.close()

def _gate(amount):
    # the same brake philosophy as model calls: killswitch + daily budget
    if KILLSWITCH.exists():
        return False, "KILLSWITCH present — all spend halted"
    spent = _spent_today(SPEND_LANE)
    if spent + abs(amount) > DAILY_CAP_USD:
        return False, f"daily spend cap hit (${spent:.2f}+${abs(amount):.2f} > ${DAILY_CAP_USD})"
    return True, "ok"

def run(direction, amount, memo):
    import stripe
    amount = float(amount)
    ok, why = _gate(amount)
    if not ok:
        print(f"[spend] BLOCKED: {why}")
        _ledger(f"{direction}-blocked-{int(time.time())}", f"spend.{direction}", 0, "blocked")
        sys.exit(1)
    stripe.api_key = _key()
    cents = int(round(amount * 100))
    tid = f"{direction}-{int(time.time())}"
    try:
        if direction == "charge":  # agent SPENDS — money out
            pi = stripe.PaymentIntent.create(
                amount=cents, currency="usd",
                payment_method="pm_card_visa",  # Stripe test card
                confirm=True, description=memo,
                automatic_payment_methods={"enabled": True, "allow_redirects": "never"})
            signed = -amount  # money out (negative)
        else:  # earn — money IN (test charge representing revenue)
            pi = stripe.PaymentIntent.create(
                amount=cents, currency="usd",
                payment_method="pm_card_visa", confirm=True,
                description=f"REVENUE: {memo}",
                automatic_payment_methods={"enabled": True, "allow_redirects": "never"})
            signed = amount  # money in (positive)
        _ledger(tid, f"spend.{direction}", signed, pi.status)
        print(json.dumps({"ok": True, "direction": direction, "amount_usd": amount,
                          "stripe_status": pi.status, "payment_intent": pi.id,
                          "ledger": "written", "memo": memo}))
    except Exception as e:
        _ledger(tid, f"spend.{direction}", 0, "error")
        print(json.dumps({"ok": False, "error": str(e)[:200]}))
        sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: spend_cell.py [charge|earn] <amount_usd> [memo]")
    run(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "grokgo hackathon demo")
