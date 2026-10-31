"""
Lab 6 - Code (line) coverage tests for warranty_claims.py
Name: Aditi Mahesh Kumar Hubli
SRN : PES1UG24CS652

Run:
    coverage run -m pytest CodeCoverageTest_warranty_claims.py
    coverage report -m
"""
import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# ---------------- out_of_warranty_charge ----------------
def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 10, "defect", False)


def test_negative_age_raises():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_registered_extension_makes_claim_free():
    # basic = 12 months + 6 registered bonus = 18 -> age 18 is covered
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0


def test_defect_out_of_warranty_small_excess():
    # basic, 14 months, excess 2, rate 100
    assert out_of_warranty_charge("basic", 14, "defect", False) == 200


def test_accidental_out_of_warranty_small_excess():
    # basic, 14 months, excess 2, rate 200
    assert out_of_warranty_charge("basic", 14, "accidental", False) == 400


def test_defect_large_excess_surcharge():
    # basic, 30 months, excess 18 (>12), rate 100 + 50
    assert out_of_warranty_charge("basic", 30, "defect", False) == 18 * 150


def test_accidental_large_excess_surcharge():
    # basic, 30 months, excess 18 (>12), rate 200 + 50 + 25
    assert out_of_warranty_charge("basic", 30, "accidental", False) == 18 * 275


# ---------------- claim_allowed ----------------
def test_claim_allowed():
    assert claim_allowed(60, 1, False) is True


def test_recall_claim():
    assert claim_allowed(0, 5, True) is True


def test_claim_too_soon():
    assert claim_allowed(10, 0, False) is False


def test_claim_limit_exceeded():
    assert claim_allowed(60, 3, False) is False


# ---------------- sla_status ----------------
def test_sla_on_track():
    assert sla_status(48, True, False) == "on_track"


def test_sla_at_risk():
    assert sla_status(40, True, False) == "at_risk"


def test_sla_critical_software_priority():
    # software (24) + priority (24) = 48 cutoff; 10h left -> critical
    assert sla_status(10, False, True) == "critical"