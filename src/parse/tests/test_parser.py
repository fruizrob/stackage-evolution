import subprocess
import os
import json
import re

def run_parser(case_path):
    path_list = [os.path.join(os.path.dirname(__file__), 'inputs/test.cabal'), case_path]

    complated_process = subprocess.run(
        os.path.join(os.path.dirname(__file__), '../PackageInfoJSON'),
        stdout=subprocess.PIPE,
        input="\n".join(path_list),
        text=True
    )

    result = re.findall(r'(?=\{).+?(?<=\})', complated_process.stdout)
    return json.loads(result[0])['calls']


def test_case1():
    filename = os.path.join(os.path.dirname(__file__), "inputs/case1.txt")
    calls = run_parser(filename)

    assert 'modify' in calls

def test_case2():
    filename = os.path.join(os.path.dirname(__file__), "inputs/case2.txt")
    calls = run_parser(filename)

    assert 'runState' in calls

def test_case3_1():
    filename = os.path.join(os.path.dirname(__file__), "inputs/case3.txt")
    calls = run_parser(filename)

    assert 'runState' in calls

def test_case3_2():
    filename = os.path.join(os.path.dirname(__file__), "inputs/case3.txt")
    calls = run_parser(filename)

    assert 'execStateT' in calls

def test_case4():
    filename = os.path.join(os.path.dirname(__file__), "inputs/case4.txt")
    calls = run_parser(filename)

    assert 'callCC' in calls
    
def test_case5():
    filename = os.path.join(os.path.dirname(__file__), "inputs/case5.txt")
    calls = run_parser(filename)

    assert 'runListT' in calls
    