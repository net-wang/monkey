from unittest.mock import MagicMock

import pytest
from pydantic import Field

from common.agent_events import AbstractAgentEvent, AgentEventRegistry


def test_reject_invalid_classes():
    class T:
        pass

    registry = AgentEventRegistry()

    with pytest.raises(TypeError):
        registry.register(T)


def metaclass_factory(registry):
    class RegistratorMeta(type):
        def __new__(cls, name, bases, dct):
            x = super().__new__(cls, name, bases, dct)
            print(f"We call {registry} with {name} to register {x}")
            registry(name, x)
            return x
    return RegistratorMeta


def test_registration_2():
    reg1 = MagicMock()
    reg2 = MagicMock()

    meta1 = metaclass_factory(reg1)
    meta2 = metaclass_factory(reg2)

    class SomeEvent(metaclass=meta1):
        some_param: int = Field(default=435)

    class OtherEvent(metaclass=meta2):
        other_param: float = Field(default=123.456)

    call_args = reg1.call_args[0]
    assert call_args[0] == "SomeEvent"
    assert call_args[1] == SomeEvent

    call_args = reg2.call_args[0]
    assert call_args[0] == "OtherEvent"
    assert call_args[1] == OtherEvent


def test_registration():
    class SomeEvent(AbstractAgentEvent):
        some_param: int = Field(default=435)

    class OtherEvent(AbstractAgentEvent):
        other_param: float = Field(default=123.456)

    registry = AgentEventRegistry()

    registry.register(SomeEvent)
    registry.register(OtherEvent)

    assert registry[SomeEvent.__name__] == SomeEvent
    assert registry[OtherEvent.__name__] == OtherEvent


def test_key_error():
    registry = AgentEventRegistry()

    with pytest.raises(KeyError):
        registry["Nonexistant"]
