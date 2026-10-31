# Lab 6: Code and Branch Coverage

**SRN:** PES1UG24CS579

**Application:** Vending machine

**Source:** [Assigned repository](https://github.com/SETAPESU26/L6_L7_30_vending_machine), commit `b6d19b3`.

**Fork and coverage commits:** [Personal repository](https://github.com/zahoormzm/L6_L7_30_vending_machine).

Line stage: `4275456`. Branch stage: `1b06655`.

The application handles item selection, coin change and purchases. It is
unchanged from the assigned version. Only tests, configuration and evidence
have been added for Lab 6; no Lab 7 work is included.

## Results

| Suite | Tests | Statements covered | Branches covered |
| --- | --- | --- | --- |
| Original starter | 2 | 13/30 (43%) | See initial branch report |
| Code coverage stage | 18 | 29/30 (96.67%, displayed as 97%) | Not measured in line-only run |
| Branch coverage stage | 37 | 30/30 (100%) | 18/18 (100%) |

The fork's 57 tests pass together (including two original starter tests).
The 55 stage tests supplied here pass together. The original branch-enabled report displays
40% combined coverage; that column combines statements and branches and
is not a standalone branch percentage.

## Run

From this `Lab6` directory, using Python 3.12 or another supported Python 3:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
```

`pytest.ini` enables discovery of both required capitalised test filenames.
Each coverage command below explicitly measures only `vending_machine.py`.
Test files are not included in the coverage denominator. Separate data files
prevent the two stages from overwriting each other.

## Code coverage

```bash
python -m coverage run --data-file=.coverage.line --source=vending_machine -m pytest CodeCoverageTest_vending_machine.py
python -m coverage report --data-file=.coverage.line -m --fail-under=90
```

The first stage covers all selection outcomes, exact and impossible change,
purchase failures, successful purchases and stock updates. Its only missing
statement is line 17, the exception raised for a negative change amount.
Eighteen assertions-based cases pass and line coverage exceeds 90%.

## Branch coverage

```bash
python -m coverage run --branch --data-file=.coverage.branch --source=vending_machine -m pytest BranchCoverageTest_vending_machine.py
python -m coverage report --data-file=.coverage.branch -m --fail-under=90
```

The second suite runs independently. It adds the negative-amount exception,
price boundaries for each item, guard precedence, coin-loop behaviour,
unrepresentable remainders, and repeated purchases until stock is exhausted.
It checks return values and stock mutation, not merely code execution.
The JSON report in the fork confirms 18 covered and zero missing branches.

Line coverage measures executed statements. Branch coverage also measures
alternative control-flow exits. Neither proves all possible paths, all input
combinations or complete correctness. These tests exercise the provided
contract; they do not invent validation rules for unsupported input types.

## Deliverables

- [Code coverage tests](CodeCoverageTest_vending_machine.py)
- [Branch coverage tests](BranchCoverageTest_vending_machine.py)
- [Code coverage report](reports/code_coverage.txt)
- [Code coverage screenshot](screenshots/code_coverage.png)
- [Branch coverage report](reports/branch_coverage.txt)
- [Saved test and initial coverage output](reports)
