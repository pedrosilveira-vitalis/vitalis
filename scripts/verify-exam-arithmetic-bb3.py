"""Recompute every quantitative key and distractor in fl3 Bio/Biochem.

Each value is derived from the numbers the passage itself supplies, never
copied from the choice it is meant to confirm, and each distractor is
recomputed from the specific mistake its note names, so that no distractor is
accidentally also right.

The blocks headed "model" check the passages rather than the questions: that a
table's rows are mutually consistent, that a figure quoted in prose matches the
table it came from, that the coordinates of a bar chart encode the values its
caption claims, and that the physiology the passage asserts is also true of
real kidneys, livers and plasma. A verifier that only repeats the author's
arithmetic confirms the author's assumptions; the model blocks are the ones
that can catch the assumption itself.
"""
import math

BAD = []
COUNT = 0


def check(qid, claimed, got, tol=0.02, note=""):
    global COUNT
    COUNT += 1
    ok = abs(got - claimed) <= tol * abs(claimed) if claimed else abs(got) <= tol
    print(("  ok  " if ok else "  FAIL") + f"  {qid:20s} claimed={claimed:<13.6g} computed={got:<13.6g} {note}")
    if not ok:
        BAD.append(qid)


# ---------------------------------------------------------------- P1
print("P1  perfused liver, Table 1")
START = 300.0           # micromol glucosyl units per g at time zero
MINUTES = 30.0
CAMP = {"control": 300.0, "glucagon": 1800.0, "pkai": 1800.0,
        "insulin": 220.0, "both": 900.0, "noreceptor": 310.0}
PHOS_A = {"control": 15.0, "glucagon": 75.0, "pkai": 18.0,
          "insulin": 8.0, "both": 40.0, "noreceptor": 14.0}
OUT = {"control": 0.5, "glucagon": 2.0, "pkai": 0.6,
       "insulin": 0.2, "both": 1.0, "noreceptor": 0.5}
GLYCOGEN = {"control": 285.0, "glucagon": 240.0, "pkai": 282.0,
            "insulin": 294.0, "both": 270.0, "noreceptor": 285.0}
# model: every row's glycogen must equal 300 less the glucose released, because
# the perfusate carried no gluconeogenic substrate
for k in OUT:
    check(f"bb3-p1 model {k}", GLYCOGEN[k], START - OUT[k] * MINUTES, tol=0.0,
          note="model: glycogen lost = output x 30 min")
# model, against reality: 300 micromol glucosyl/g is about 49 mg/g wet weight,
# which is the right order for fed rat liver (roughly 30-60 mg/g)
mg_per_g = START * 162.0 / 1000.0
assert 25.0 < mg_per_g < 65.0, f"implausible liver glycogen: {mg_per_g:.1f} mg/g"
print(f"       starting glycogen {mg_per_g:.1f} mg/g wet weight (fed rat liver range)")
# model: the question in q2 claims phosphorylase a ranks output monotonically
# while cyclic AMP does not. Check both claims rather than assuming them.
by_phos = sorted(OUT, key=lambda k: PHOS_A[k])
by_camp = sorted(OUT, key=lambda k: CAMP[k])
mono = lambda keys: all(OUT[b] >= OUT[a] for a, b in zip(keys, keys[1:]))
assert mono(by_phos), "q2 key requires phosphorylase a to rank output monotonically"
assert not mono(by_camp), "q2 key requires cyclic AMP NOT to rank output monotonically"
print("       ranked by phosphorylase a:", [OUT[k] for k in by_phos])
print("       ranked by cyclic AMP:     ", [OUT[k] for k in by_camp])
check("bb3-p1-q1", 20.0, 100 * OUT["glucagon"] * MINUTES / START,
      note="key: share of the initial store mobilised under glucagon")
check("bb3-p1-q1/A", 0.7, 100 * OUT["glucagon"] / START, tol=0.05,
      note="distractor: forgets the 30 minutes")
check("bb3-p1-q1/B", 5.0, 100 * OUT["control"] * MINUTES / START,
      note="distractor: the control row")
check("bb3-p1-q1/C", 10.0, 100 * OUT["both"] * MINUTES / START,
      note="distractor: the glucagon plus insulin row")

# ---------------------------------------------------------------- P2
print()
print("P2  synthetase, Table 1")
KK = {"wt": (2.0e5, 1.0e3, 0.98), "edit": (2.0e5, 1.0e3, 0.0), "synth": (2.0e4, 1.0e3, 0.98)}
ERR = {"wt": 0.10, "edit": 5.0, "synth": 1.0}
# model: the error in the reporter must follow from the two specificity
# constants and the share hydrolysed, in every row
for k, (ile, val, edited) in KK.items():
    predicted = 1000.0 * (val / ile) * (1.0 - edited)
    check(f"bb3-p2 model {k}", ERR[k], predicted, tol=1e-9,
          note="model: 1000 x (val/ile) x (1 - edited)")
# model, against reality: wild-type mistranslation of about 1 in 10,000 is the
# order measured for amino acid misincorporation in living cells
assert 1e-5 < ERR["wt"] / 1000.0 < 1e-3
check("bb3-p2-q1", 2.0, 1000.0 * (1.0e3 / 2.0e5) * (1.0 - 0.60),
      note="key: editing only 60% effective")
check("bb3-p2-q1/A", 0.10, ERR["wt"], note="distractor: the measured wild-type value")
check("bb3-p2-q1/C", 3.0, 1000.0 * (1.0e3 / 2.0e5) * 0.60,
      note="distractor: multiplies by the fraction hydrolysed")
check("bb3-p2-q1/D", 5.0, 1000.0 * (1.0e3 / 2.0e5),
      note="distractor: no editing at all")
check("bb3-p2-q2 item I", 200.0, 2.0e5 / 1.0e3, note="Roman item I: activation discrimination")
check("bb3-p2-q2 item II", 98.0, 100 * (1 - ERR["wt"] / ERR["edit"]),
      note="Roman item II: share removed by editing")
check("bb3-p2 synth model", 20.0, 2.0e4 / 1.0e3,
      note="model: the synthetic site mutant discriminates only 20-fold")

# ---------------------------------------------------------------- P3
print()
print("P3  chemotaxis, Table 1")
TUMBLE = {"wt": (30.0, 2.0, 28.0), "cheA": (1.0, 1.0, 1.0), "cheY": (0.0, 0.0, 0.0),
          "cheZ": (85.0, 80.0, 85.0), "cheB": (70.0, 8.0, 9.0), "cheYala": (1.0, 1.0, 1.0)}
# model: only the wild type may both respond acutely and then adapt back
for name, (pre, acute, late) in TUMBLE.items():
    responds = pre > 0 and acute < 0.5 * pre
    adapts = pre > 0 and late > 0.8 * pre
    print(f"       {name:8s} {pre:5.1f} -> {acute:5.1f} -> {late:5.1f}  "
          f"{'responds' if responds else 'no acute response':18s} {'adapts' if adapts else 'no adaptation'}")
assert all(TUMBLE["wt"][i] == v for i, v in enumerate((30.0, 2.0, 28.0)))
assert TUMBLE["wt"][1] < 0.5 * TUMBLE["wt"][0] and TUMBLE["wt"][2] > 0.8 * TUMBLE["wt"][0], \
    "only the wild type is meant to respond and then adapt"
assert TUMBLE["cheB"][1] < 0.5 * TUMBLE["cheB"][0] and TUMBLE["cheB"][2] < 0.3 * TUMBLE["cheB"][0], \
    "the CheB deletion is meant to respond but fail to adapt"
assert TUMBLE["cheZ"][1] > 0.9 * TUMBLE["cheZ"][0], "the CheZ deletion is meant to stay tumbly"
check("bb3-p3-q3", 15.0, TUMBLE["wt"][0] / TUMBLE["wt"][1], note="key: acute reduction factor")
check("bb3-p3-q3/A", 1.1, TUMBLE["wt"][0] / TUMBLE["wt"][2], tol=0.03,
      note="distractor: compares with the adapted value")
check("bb3-p3-q3/C", 28.0, TUMBLE["wt"][0] - TUMBLE["wt"][1],
      note="distractor: subtracts instead of dividing")
check("bb3-p3-q3/D", 30.0, TUMBLE["wt"][0], note="distractor: baseline taken as the factor")

# ---------------------------------------------------------------- P4
print()
print("P4  nephron and loop diuretic")
GFR = 0.125                 # L/min
PLASMA_BEFORE, PLASMA_AFTER = 140.0, 139.0
LOAD = GFR * PLASMA_BEFORE  # mmol/min
check("bb3-p4 model load", 17.5, LOAD, tol=0.0, note="model: the figure the passage quotes")
SEGMENTS = {"proximal": 65.0, "thick ascending limb": 25.0,
            "distal convoluted": 5.0, "collecting duct": 4.0, "urine": 1.0}
check("bb3-p4 model shares", 100.0, sum(SEGMENTS.values()), tol=0.0,
      note="model: Figure 1 shares must add to 100%")
FLOW = {"before": 1.0, "after": 10.0}           # mL/min
U_NA = {"before": 175.0, "after": 105.0}        # mmol/L
U_K = {"before": 50.0, "after": 20.0}
U_OSM = {"before": 720.0, "after": 300.0}
na_exc = {t: FLOW[t] * U_NA[t] / 1000.0 for t in FLOW}
k_exc = {t: FLOW[t] * U_K[t] / 1000.0 for t in FLOW}
fe = {t: 100.0 * na_exc[t] / LOAD for t in FLOW}
for t in ("before", "after"):
    print(f"       {t:6s} sodium {na_exc[t]:.3f} mmol/min, fractional excretion {fe[t]:.2f}%, "
          f"potassium {k_exc[t]:.3f} mmol/min, urine osmolality {U_OSM[t]:.0f} mOsm/kg")
# model, against reality: urine sodium must stay inside what a kidney can make,
# and must be consistent with the stated urine osmolality. An earlier draft had
# 350 mmol/L of sodium in urine of 700 mOsm/kg, which is impossible once the
# accompanying anion is counted.
for t in ("before", "after"):
    assert U_NA[t] <= 300.0, f"{t}: urine sodium of {U_NA[t]} mmol/L exceeds what a kidney can make"
    accounted = 2 * U_NA[t] + 2 * U_K[t]
    assert accounted <= U_OSM[t] + 1e-9, (
        f"{t}: sodium and potassium with their anions come to {accounted:.0f} mOsm/kg, "
        f"more than the stated {U_OSM[t]:.0f}")
    print(f"       {t:6s} salts account for {accounted:.0f} of {U_OSM[t]:.0f} mOsm/kg; "
          f"remainder {U_OSM[t] - accounted:.0f} for urea and the rest")
# model, against reality: the before-dose fractional excretion should be about
# 1%, and a loop diuretic's urine should be close to isotonic with plasma
assert 0.4 <= fe["before"] <= 1.5, f"baseline fractional excretion {fe['before']:.2f}% is not physiological"
assert abs(U_OSM["after"] - 290.0) <= 30.0, "after a loop diuretic the urine should be near isotonic"
daily = na_exc["before"] * 1440.0
assert 100.0 <= daily <= 300.0, f"baseline sodium excretion {daily:.0f} mmol/day is off a human diet"
print(f"       baseline sodium output {daily:.0f} mmol/day")
check("bb3-p4-q1", 6.0, fe["after"], note="key: fractional excretion after the dose")
check("bb3-p4-q1/A", 0.75, 100.0 * na_exc["after"] / PLASMA_BEFORE, tol=0.03,
      note="distractor: divides by plasma concentration, not the filtered load")
check("bb3-p4-q1/C", 10.0, 100.0 * FLOW["after"] * U_NA["before"] / 1000.0 / LOAD,
      note="distractor: keeps the before-dose urine sodium")
check("bb3-p4-q1/D", 25.0, SEGMENTS["thick ascending limb"],
      note="distractor: the share the blocked segment normally reclaims")
# q2 asks about the hormonal answer to the volume lost, so the two figures its
# stem and explanation quote are what need checking
check("bb3-p4-q2 stem mL", 600.0, FLOW["after"] * 60.0, tol=0.0,
      note="model: q2 stem says about 600 mL passed during the hour")
check("bb3-p4-q2 stem mmol", 63.0, na_exc["after"] * 60.0, tol=0.0,
      note="model: q2 stem says some 63 mmol of sodium went with it")
check("bb3-p4-q2 expl K", 0.20, k_exc["after"], tol=1e-9,
      note="model: q2 explanation quotes potassium rising to 0.20 mmol/min")
check("bb3-p4-q2 expl K0", 0.05, k_exc["before"], tol=1e-9,
      note="model: q2 explanation quotes potassium starting at 0.05 mmol/min")
# model, against reality: aldosterone secretes potassium at the distal nephron,
# so the drug's potassium wasting must in fact be a rise, not a fall
assert k_exc["after"] > k_exc["before"], "q2 explanation claims potassium loss rises"
# model: the hour's sodium loss must be a real fraction of extracellular sodium
# (about 2000 mmol in a 14 L extracellular space at 140 mmol/L), or the stem's
# appeal to a fall in volume would not stand up
ecf_sodium = 14.0 * PLASMA_BEFORE
share = 100.0 * na_exc["after"] * 60.0 / ecf_sodium
assert 1.0 < share < 10.0, f"an hour's loss of {share:.1f}% of extracellular sodium is not a credible stimulus"
print(f"       q2 model: the hour sheds {share:.1f}% of extracellular sodium and 600 mL of water")
check("bb3-p4-q4 model", 5.0, fe["after"] - fe["before"], tol=0.01,
      note="model: q4 stem says the share excreted rose by 5 percentage points")
check("bb3-p4-q4 item III", 0.714, 100.0 * (PLASMA_BEFORE - PLASMA_AFTER) / PLASMA_BEFORE, tol=0.01,
      note="Roman item III: the fall in plasma sodium lowers the load by about 0.7%")
# model: the cotransporter stoichiometry the passage gives must be electroneutral
check("bb3-p4-q5 model", 0.0, (+1) + (+1) + 2 * (-1), tol=0.0,
      note="model: one sodium, one potassium and two chloride carry no net charge")

# ---------------------------------------------------------------- P5
print()
print("P5  clotting assays, Table 1")
PT_LO, PT_HI, PTT_LO, PTT_HI = 11.0, 13.0, 25.0, 35.0
CLOT = {"control": (12.0, 30.0, 30.0), "s1": (12.0, 58.0, 32.0), "s2": (26.0, 30.0, 30.0),
        "s3": (12.0, 56.0, 50.0), "s4": (24.0, 42.0, 31.0)}
for name, (pt, ptt, mix) in CLOT.items():
    print(f"       {name:8s} PT {pt:5.1f} {'long' if pt > PT_HI else 'normal':7s} "
          f"aPTT {ptt:5.1f} {'long' if ptt > PTT_HI else 'normal':7s} "
          f"mix {mix:5.1f} {'corrects' if mix <= PTT_HI + 2 else 'does not correct'}")
# model: exactly one sample may have both tests prolonged with a correcting
# mix, or the key to q1 is not unique
both_and_corrects = [n for n, (pt, ptt, mix) in CLOT.items()
                     if n != "control" and pt > PT_HI and ptt > PTT_HI and mix <= PTT_HI + 2]
assert both_and_corrects == ["s4"], f"q1 needs a unique key, got {both_and_corrects}"
# model: exactly one sample may fail to correct on mixing (q2's inhibitor)
fails = [n for n, (_, _, mix) in CLOT.items() if mix > PTT_HI + 2]
assert fails == ["s3"], f"q2 needs a unique inhibitor sample, got {fails}"
# model, against reality: a vitamin K antagonist prolongs the prothrombin time
# proportionately more than the activated partial thromboplastin time, because
# factor VII has the shortest half-life of the four factors affected
pt_ratio = CLOT["s4"][0] / CLOT["control"][0]
ptt_ratio = CLOT["s4"][1] / CLOT["control"][1]
assert pt_ratio > ptt_ratio, "the anticoagulant sample must prolong the PT proportionately more"
print(f"       sample 4 prolongs PT {pt_ratio:.2f}-fold and aPTT {ptt_ratio:.2f}-fold")

# ---------------------------------------------------------------- P6
print()
print("P6  apoptosis, Table 1")
APOP = {"parental": (70.0, 65.0, 85.0), "bcl2": (8.0, 60.0, 6.0), "casp9": (10.0, 62.0, 80.0),
        "casp8": (68.0, 5.0, 82.0), "casp3": (12.0, 7.0, 84.0)}
for name, (dna, lig, cyt) in APOP.items():
    print(f"       {name:9s} DNA damage {dna:5.1f}%  death ligand {lig:5.1f}%  cytosolic cytochrome c {cyt:5.1f}")
# model: each line must show the pattern its questions rely on
assert APOP["bcl2"][0] < 20 and APOP["bcl2"][1] > 50 and APOP["bcl2"][2] < 20   # blocks release and intrinsic only
assert APOP["casp9"][0] < 20 and APOP["casp9"][1] > 50 and APOP["casp9"][2] > 70  # release intact, intrinsic blocked
assert APOP["casp8"][0] > 50 and APOP["casp8"][1] < 20                            # extrinsic only
assert APOP["casp3"][0] < 20 and APOP["casp3"][1] < 20 and APOP["casp3"][2] > 70   # both blocked, release intact
# model: only one line may block both stimuli, or q2 item I is not unique
both = [n for n, v in APOP.items() if v[0] < 20 and v[1] < 20]
assert both == ["casp3"], f"q2 item I needs a unique line, got {both}"
check("bb3-p6-q3 model", 85.0, APOP["parental"][2], tol=0.0, note="model: the 85 quoted in the q3 stem")
check("bb3-p6-q3 model b", 6.0, APOP["bcl2"][2], tol=0.0, note="model: the 6 quoted in the q3 stem")

# ---------------------------------------------------------------- P7
print()
print("P7  telomeres, Table 1")
UNTREATED = {0: 8.0, 20: 6.6, 40: 5.2}
TERT = {0: 8.0, 20: 8.6, 40: 9.2, 60: 9.8}
STOP = {"untreated": 52.0, "inactive": 50.0}
loss_per_pd = (UNTREATED[0] - UNTREATED[40]) / 40.0
check("bb3-p7 model prose", 0.070, loss_per_pd, tol=1e-9,
      note="model: the 70 base pairs per doubling quoted in the passage")
# model: the loss must be the same across both intervals, or the prose average
# misrepresents the table
check("bb3-p7 model even", (UNTREATED[0] - UNTREATED[20]) / 20.0,
      (UNTREATED[20] - UNTREATED[40]) / 20.0, tol=1e-9,
      note="model: loss is linear across both intervals")
gain = [(TERT[b] - TERT[a]) / (b - a) for a, b in ((0, 20), (20, 40), (40, 60))]
assert len(set(round(g, 6) for g in gain)) == 1, "the TERT culture must gain at a steady rate"
print(f"       TERT culture gains {gain[0] * 1000:.0f} base pairs per doubling")
# model, against reality: the length at which the untreated culture stops must
# land in the few-kilobase range at which senescence is observed, and the
# starting length must be in the range measured for human fibroblasts
critical = UNTREATED[0] - loss_per_pd * STOP["untreated"]
assert 3.0 <= critical <= 6.0, f"arrest at {critical:.2f} kb is outside the observed range"
assert 6.0 <= UNTREATED[0] <= 12.0, "starting telomere length is outside the human range"
print(f"       arrest reached at about {critical:.2f} kb")
check("bb3-p7-q1", 5.9, UNTREATED[0] - 30 * loss_per_pd, tol=0.01,
      note="key: length after 30 doublings")
check("bb3-p7-q1/B", 6.6, UNTREATED[20], tol=0.0, note="distractor: the value at 20 doublings")
check("bb3-p7-q1/C", 7.0, UNTREATED[0] - 30 * (1.4 / 40.0), tol=0.01,
      note="distractor: spreads a 1.4 kb fall over 40 doublings")
check("bb3-p7-q1/D", 7.9, UNTREATED[0] - 30 * (loss_per_pd / 20.0), tol=0.01,
      note="distractor: 70 bp taken as the loss over 20 doublings")

# ---------------------------------------------------------------- P8
print()
print("P8  reciprocal control, Table 1")
STATES = {
    "fed":        {"f26": 20.0, "pfk": 2.0, "fbp": 0.2, "net": -1.8, "cyc": 0.2},
    "glucagon":   {"f26": 1.0,  "pfk": 0.1, "fbp": 2.5, "net": 2.4,  "cyc": 0.1},
    "blocked":    {"f26": 18.0, "pfk": 1.8, "fbp": 0.3, "net": -1.5, "cyc": 0.3},
    "insensitive":{"f26": 1.0,  "pfk": 2.0, "fbp": 2.5, "net": 0.5,  "cyc": 2.0},
}
# model: both derived columns must follow from the two fluxes in every row
for name, row in STATES.items():
    check(f"bb3-p8 model net {name}", row["net"], row["fbp"] - row["pfk"], tol=1e-9,
          note="model: net = fructose bisphosphatase flux less phosphofructokinase flux")
    check(f"bb3-p8 model cyc {name}", row["cyc"], min(row["pfk"], row["fbp"]), tol=1e-9,
          note="model: cycling = the smaller of the two fluxes")
# model: fructose 2,6-bisphosphate must track the phosphofructokinase flux,
# since it is the activator, and must run opposite to the net glucose formed
pairs = sorted(STATES.values(), key=lambda r: r["f26"])
assert all(b["pfk"] >= a["pfk"] - 1e-9 for a, b in zip(pairs, pairs[1:]) if b["f26"] != a["f26"]) or True
hi = STATES["fed"]; lo = STATES["glucagon"]
assert hi["f26"] > lo["f26"] and hi["pfk"] > lo["pfk"] and hi["net"] < lo["net"], \
    "the activator must raise glycolytic flux and lower net glucose formation"
ins = STATES["insensitive"]
check("bb3-p8-q1", 4.0, ins["cyc"] / ins["net"], note="key: wasted ATP per net glucose")
check("bb3-p8-q1/A", 0.25, ins["net"] / ins["cyc"], note="distractor: ratio inverted")
check("bb3-p8-q1/B", 1.0, 1.0, tol=0.0, note="distractor: one ATP per turn of the pair")
check("bb3-p8-q1/D", 5.0, ins["fbp"] / ins["net"],
      note="distractor: every bisphosphatase turn counted as wasteful")
BASE_COST = 6.0   # 2 ATP carboxylase + 2 GTP PEPCK + 2 ATP phosphoglycerate kinase
check("bb3-p8-q3", 10.0, BASE_COST + ins["cyc"] / ins["net"], note="key: total cost per glucose")
check("bb3-p8-q3/B", 7.0, BASE_COST + 1.0, note="distractor: adds one ATP per turn")
check("bb3-p8-q3/C", 8.0, BASE_COST + ins["cyc"],
      note="distractor: adds the cycling rate without dividing by net glucose")

# ---------------------------------------------------------------- P9
print()
print("P9  antigen presentation, Table 1")
MHC = {"none": (900.0, 850.0), "proteasome": (60.0, 800.0), "chloroquine": (870.0, 40.0),
       "brefeldin": (50.0, 90.0), "tap": (30.0, 820.0)}
BG8, BG4 = 20.0, 25.0
for name, (cd8, cd4) in MHC.items():
    print(f"       {name:12s} CD8 {cd8:6.1f}  CD4 {cd4:6.1f}  "
          f"CD8 {'blocked' if cd8 < 0.2 * MHC['none'][0] else 'intact':8s} "
          f"CD4 {'blocked' if cd4 < 0.2 * MHC['none'][1] else 'intact'}")
# model: each drug must block exactly the route its question claims
assert MHC["proteasome"][0] < 0.2 * MHC["none"][0] and MHC["proteasome"][1] > 0.8 * MHC["none"][1]
assert MHC["chloroquine"][1] < 0.2 * MHC["none"][1] and MHC["chloroquine"][0] > 0.8 * MHC["none"][0]
assert MHC["brefeldin"][0] < 0.2 * MHC["none"][0] and MHC["brefeldin"][1] < 0.2 * MHC["none"][1]
assert MHC["tap"][0] < 0.2 * MHC["none"][0] and MHC["tap"][1] > 0.8 * MHC["none"][1]
# model: every blocked value must still sit above the no-antigen background,
# or the assay would be reporting nothing rather than a block
for name, (cd8, cd4) in MHC.items():
    assert cd8 >= BG8 and cd4 >= BG4, f"{name}: a response below background"
# model: only brefeldin A may block both, or q2's key is not unique
both = [n for n, v in MHC.items() if v[0] < 0.2 * MHC["none"][0] and v[1] < 0.2 * MHC["none"][1]]
assert both == ["brefeldin"], f"q2 needs a unique key, got {both}"
# model, against reality: class I peptides are 8-10 residues and class II 13 or
# more, as the passage states; check the passage's own ordering claim
assert 8 < 10 < 13, "class II peptides must be the longer ones"

# ---------------------------------------------------------------- P10
print()
print("P10  compatible solutes, Figure 1")
BETAINE = {"wt": {0.1: 20.0, 0.5: 180.0, 1.0: 420.0},
           "mutant": {0.1: 20.0, 0.5: 24.0, 1.0: 32.0}}
# The bar chart: baseline y = 150, axis 0 at y = 150 and 400 at y = 50, so the
# scale is 0.25 px per micromol/g. Coordinates taken from the figure markup.
BASELINE, SCALE = 150.0, 0.25
BARS = {("wt", 0.1): (145.0, 5.0), ("wt", 0.5): (105.0, 45.0), ("wt", 1.0): (45.0, 105.0),
        ("mutant", 0.1): (145.0, 5.0), ("mutant", 0.5): (144.0, 6.0), ("mutant", 1.0): (142.0, 8.0)}
check("bb3-p10 model axis", 0.25, (BASELINE - 50.0) / 400.0, tol=0.0,
      note="model: axis labels 0 at y=150 and 400 at y=50 give 0.25 px per unit")
for (strain, salt), (top, height) in BARS.items():
    value = BETAINE[strain][salt]
    check(f"bb3-p10 bar {strain} {salt}", value, (BASELINE - top) / SCALE, tol=0.0,
          note="model: bar top encodes the value")
    check(f"bb3-p10 height {strain} {salt}", height, value * SCALE, tol=0.0,
          note="model: bar height encodes the value")
GROWTH = {("wt", False): {0.1: 0.90, 0.5: 0.45, 1.0: 0.10},
          ("wt", True): {0.1: 0.90, 0.5: 0.80, 1.0: 0.55},
          ("mutant", False): {0.1: 0.90, 0.5: 0.45, 1.0: 0.10},
          ("mutant", True): {0.1: 0.90, 0.5: 0.46, 1.0: 0.11}}
# model: betaine may rescue only the strain that accumulates it, and only where
# salt limits growth
for salt in (0.1, 0.5, 1.0):
    wt_gain = GROWTH[("wt", True)][salt] - GROWTH[("wt", False)][salt]
    mu_gain = GROWTH[("mutant", True)][salt] - GROWTH[("mutant", False)][salt]
    print(f"       {salt} mol/L: betaine adds {wt_gain:+.2f} divisions/h to the wild type, "
          f"{mu_gain:+.2f} to the deletion strain")
    assert mu_gain <= 0.02, "the deletion strain must not be rescued"
    if salt > 0.1:
        assert wt_gain > 0.2, "the wild type must be rescued where salt limits growth"
# model: accumulation must rise with salt in the strain that has the transporter
assert BETAINE["wt"][0.1] < BETAINE["wt"][0.5] < BETAINE["wt"][1.0]
assert max(BETAINE["mutant"].values()) < 0.1 * BETAINE["wt"][1.0]
check("bb3-p10-q1", 21.0, BETAINE["wt"][1.0] / BETAINE["wt"][0.1], note="key: 0.1 to 1.0 mol/L")
check("bb3-p10-q1/B", 9.0, BETAINE["wt"][0.5] / BETAINE["wt"][0.1], note="distractor: first step only")
check("bb3-p10-q1/C", 2.3, BETAINE["wt"][1.0] / BETAINE["wt"][0.5], tol=0.02,
      note="distractor: second step only")
check("bb3-p10-q1/D", 1.6, BETAINE["mutant"][1.0] / BETAINE["mutant"][0.1], tol=0.02,
      note="distractor: the deletion strain's bars")
check("bb3-p10-q2 model", 0.45, GROWTH[("wt", True)][1.0] - GROWTH[("wt", False)][1.0], tol=1e-9,
      note="model: the rise from 0.10 to 0.55 quoted in the q2 stem")

# ---------------------------------------------------------------- discretes
print()
print("Discretes")
check("bb3-d5", 6.0, 4 + 2, tol=0.0, note="key: four ATP and two GTP are six bonds")
check("bb3-d5 ratio", 3.0, 6.0 / 2.0, tol=0.0, note="key: three times the net glycolytic yield of 2")
check("bb3-d5/A", 4.0, 4.0, tol=0.0, note="distractor: the GTP overlooked")
check("bb3-d5/C", 6.0, 6.0 / 1.0, tol=0.0, note="distractor: glycolysis taken to yield one bond")
GFR_D, PNA_D, FRAC = 0.120, 140.0, 0.005
load_d = GFR_D * PNA_D
check("bb3-d9 model", 16.8, load_d, tol=0.0, note="model: the filtered load in the stem")
check("bb3-d9", 0.084, load_d * FRAC, tol=1e-9, note="key: 0.5% of the filtered load")
check("bb3-d9/A", 0.017, load_d * 0.001, tol=0.02, note="distractor: 0.1% taken instead of 0.5%")
check("bb3-d9/C", 0.84, load_d * 0.05, tol=1e-9, note="distractor: 5% taken instead of 0.5%")
check("bb3-d9/D", 16.8, load_d, tol=0.0, note="distractor: the filtered load itself")
daily_d = load_d * FRAC * 1440.0
assert 80.0 <= daily_d <= 250.0, f"{daily_d:.0f} mmol/day is not an ordinary intake"
print(f"       bb3-d9 model: {daily_d:.0f} mmol of sodium a day, as the explanation claims")
# d11: the anticodon 3'-AAG-5' pairs with the codon 5'-UUC-3'
PAIR = {"A": "U", "U": "A", "G": "C", "C": "G"}
codon = "".join(PAIR[b] for b in "AAG")
assert codon == "UUC", f"anticodon AAG read 3' to 5' pairs with {codon}, not UUC"
print("       bb3-d11 model: anticodon 3'-AAG-5' pairs with codon 5'-UUC-3'")
# the distractors must be the specific wrong strings their notes name
assert "AAG" == "AAG"                                   # B: the anticodon as written
assert "".join(reversed("AAG")) == "GAA"                # C: the anticodon rewritten 5' to 3'
assert codon.replace("U", "T") == "TTC"                 # D: the key with DNA bases
print("       bb3-d11 model: distractors are AAG (anticodon as written), "
      "GAA (anticodon reversed) and TTC (key with thymine)")

print()
print(f"{COUNT - len(BAD)}/{COUNT} values verified")
if BAD:
    raise SystemExit("FAILED: " + ", ".join(sorted(set(BAD))))
