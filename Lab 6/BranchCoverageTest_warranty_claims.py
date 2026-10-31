"""
Lab 6 - Branch coverage tests for warranty_claims.py
Name: Aditi Mahesh Kumar Hubli
SRN : PES1UG24CS652

Every decision in warranty_claims.py is exercised for both its True and
False outcome, with boundary values where the condition uses <, <=, >, >=.

Run:
    coverage run --branch -m pytest BranchCoverageTest_warranty_claims.py
    coverage report -m
"""
import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# ---------- out_of_warranty_charge ----------
# line 5: plan not in COVERED_MONTHS  (True -> raise / False -> continue)
@pytest.mark.parametrize("plan", ["gold", "", "BASIC"])
def test_plan_not_known_raises(plan):
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge(plan, 10, "defect", False)


@pytest.mark.parametrize("plan, months", [("basic", 12), ("standard", 24), ("premium", 36)])
def test_plan_known_at_exact_cover_is_free(plan, months):
    assert out_of_warranty_charge(plan, months, "defect", False) == 0


# line 7: age_months < 0  (True / False, boundary -1 / 0)
def test_age_negative_raises():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_age_zero_is_valid():
    assert out_of_warranty_charge("basic", 0, "defect", False) == 0


# line 10: is_registered and plan != "premium"
def test_registered_non_premium_gets_bonus():
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0      # 12 + 6
    assert out_of_warranty_charge("basic", 19, "defect", True) == 100    # 1 month over


def test_not_registered_no_bonus():
    assert out_of_warranty_charge("basic", 13, "defect", False) == 100


def test_registered_premium_gets_no_bonus():
    assert out_of_warranty_charge("premium", 37, "defect", True) == 100  # still 36 cover


# line 13: excess <= 0  (True / False, boundary 0 / 1)
def test_excess_zero_returns_zero():
    assert out_of_warranty_charge("standard", 24, "accidental", False) == 0


def test_excess_one_is_charged():
    assert out_of_warranty_charge("standard", 25, "defect", False) == 100


# line 15: claim_type == "accidental"  (True / False)
def test_accidental_rate():
    assert out_of_warranty_charge("basic", 14, "accidental", False) == 2 * 200


def test_non_accidental_rate():
    assert out_of_warranty_charge("basic", 14, "defect", False) == 2 * 100


# line 19: excess > 12  (True / False, boundary 12 / 13)
def test_excess_twelve_no_surcharge():
    assert out_of_warranty_charge("basic", 24, "defect", False) == 12 * 100
    assert out_of_warranty_charge("basic", 24, "accidental", False) == 12 * 200


# line 21: accidental inside the surcharge block (True / False)
def test_excess_thirteen_defect_surcharge():
    assert out_of_warranty_charge("basic", 25, "defect", False) == 13 * 150


def test_excess_thirteen_accidental_surcharge():
    assert out_of_warranty_charge("basic", 25, "accidental", False) == 13 * 275


# ---------- claim_allowed ----------
# line 27: is_recall (True / False); line 28 result both ways at boundary 5 / 6
def test_recall_within_limit():
    assert claim_allowed(0, 5, True) is True


def test_recall_over_limit():
    assert claim_allowed(0, 6, True) is False


# line 29: days_since_last_claim < 30 (True / False, boundary 29 / 30)
def test_non_recall_too_soon():
    assert claim_allowed(29, 0, False) is False


def test_non_recall_exactly_thirty_days():
    assert claim_allowed(30, 0, False) is True


# line 31: claims_filed <= 2 (boundary 2 / 3)
def test_non_recall_at_claim_limit():
    assert claim_allowed(60, 2, False) is True


def test_non_recall_over_claim_limit():
    assert claim_allowed(60, 3, False) is False


# ---------- sla_status ----------
# line 35: is_hardware (True / False); line 38: is_priority (True / False)
# cutoff: hardware 48, software 24, +24 if priority
@pytest.mark.parametrize(
    "hours, hardware, priority, expected",
    [
        # hardware, not priority -> cutoff 48
        (48, True, False, "on_track"),
        (47, True, False, "at_risk"),
        (36, True, False, "at_risk"),
        (35, True, False, "critical"),
        # software, not priority -> cutoff 24
        (24, False, False, "on_track"),
        (23, False, False, "at_risk"),
        (12, False, False, "at_risk"),
        (11, False, False, "critical"),
        # hardware + priority -> cutoff 72
        (72, True, True, "on_track"),
        (71, True, True, "at_risk"),
        (60, True, True, "at_risk"),
        (59, True, True, "critical"),
        # software + priority -> cutoff 48
        (48, False, True, "on_track"),
        (36, False, True, "at_risk"),
        (35, False, True, "critical"),
    ],
)
def test_sla_status_all_branches(hours, hardware, priority, expected):
    assert sla_status(hours, hardware, priority) == expected