import pytest

from covid.domain.model import Actor

@pytest.fixture
def actor():
    return Actor("Daniel Radcliffe")

def test_actor(actor):
    assert repr(actor) == "<Actor Daniel Radcliffe>"

def test_init():
    actor1 = Actor("Harry Potter")
    assert repr(actor1) == "<Actor Harry Potter>"

def test_actor_none():
    actor2 = Actor("")
    assert actor2.actor_full_name is None
    actor3 = Actor(42)
    assert actor3.actor_full_name is None

def test_actor_same():
    actor1 = Actor("Harry Potter")
    assert actor1 == actor1

def test_actor_diff():
    actor1 = Actor("Harry Potter")
    actor4 = Actor("Ronald Weasley")
    assert actor1 != actor4

def test_actor_val():
    actor1 = Actor("Harry Potter")
    actor4 = Actor("Ronald Weasley")
    assert actor1 < actor4

def test_actor_hash():
    actor4 = Actor("Ronald Weasley")
    assert hash(actor4) == hash(actor4)

def test_co_actors():
    actor1 = Actor("Harry Potter")
    actor4 = Actor("Ronald Weasley")
    coactor = actor1.check_if_this_actor_worked_with(actor4)
    assert coactor == 0
    addingCoactor = actor1.add_actor_colleague(actor4)
    coactor = actor1.check_if_this_actor_worked_with(actor4)
    assert coactor == 1
    