import pytest  # type: ignore
from pytest_mock import MockerFixture
from unittest.mock import Mock
from modules.event_system.event_system import EventSystem

TEST_EVENT_NAME = "test_event_name"
TEST_DEPENDENCY_EVENT_NAME = "test_dependency_event_name"
TEST_ISOLATED_EVENT_NAME = "test_isolated_event_name"


def test_trigger_event_which_is_not_registered(mocker: MockerFixture):
    warningMock = mocker.patch("utils.logger.logger.warning")
    EventSystem.TriggerEvent(TEST_EVENT_NAME)
    warningMock.assert_called_once()


def test_non_registered_event_will_be_not_triggered_when_event_is_triggered():
    callback = Mock()
    EventSystem.TriggerEvent(TEST_EVENT_NAME)
    assert callback.called == 0


def test_register_event_will_be_triggered_when_event_is_triggered():
    callback = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback)
    EventSystem.TriggerEvent(TEST_EVENT_NAME)
    assert callback.called == 1


def test_multiple_callbacks_will_be_triggered_when_event_is_triggered():
    callback1 = Mock()
    callback2 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback2)
    EventSystem.TriggerEvent(TEST_EVENT_NAME)
    assert callback1.called == 1
    assert callback2.called == 1


def test_only_registered_callback_will_be_triggered_when_event_is_triggered():
    callback1 = Mock()
    callback2 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.TriggerEvent(TEST_EVENT_NAME)
    assert callback1.called == 1
    assert callback2.called == 0


def test_the_depedency_event_will_be_triggered_when_the_top_event_is_triggered():
    callback1 = Mock()
    callback2 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.RegisterEvent(TEST_DEPENDENCY_EVENT_NAME, callback2)

    EventSystem.AttachEvent(TEST_EVENT_NAME, TEST_DEPENDENCY_EVENT_NAME)

    EventSystem.TriggerEvent(TEST_EVENT_NAME)

    assert callback1.called == 1
    assert callback2.called == 1


def test_the_circular_dependency_will_be_logged_when_the_event_is_triggered():
    callback1 = Mock()
    callback2 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.RegisterEvent(TEST_DEPENDENCY_EVENT_NAME, callback2)

    EventSystem.AttachEvent(TEST_EVENT_NAME, TEST_DEPENDENCY_EVENT_NAME)
    EventSystem.AttachEvent(TEST_DEPENDENCY_EVENT_NAME, TEST_EVENT_NAME)

    EventSystem.TriggerEvent(TEST_EVENT_NAME)

    assert callback1.called == 1
    assert callback2.called == 1


def test_the_circular_dependency_with_an_isolated_event():
    callback1 = Mock()
    callback2 = Mock()
    callback3 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.RegisterEvent(TEST_DEPENDENCY_EVENT_NAME, callback2)
    EventSystem.RegisterEvent(TEST_ISOLATED_EVENT_NAME, callback3)

    EventSystem.AttachEvent(TEST_EVENT_NAME, TEST_DEPENDENCY_EVENT_NAME)

    EventSystem.TriggerEvent(TEST_DEPENDENCY_EVENT_NAME)

    assert callback1.called == 1
    assert callback2.called == 1
    assert callback3.called == 0


def test_attach_multiple_events_to_the_same_event():
    callback1 = Mock()
    callback2 = Mock()
    callback3 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.RegisterEvent(TEST_DEPENDENCY_EVENT_NAME, callback2)
    EventSystem.RegisterEvent(TEST_ISOLATED_EVENT_NAME, callback3)

    EventSystem.AttachEvent(
        TEST_EVENT_NAME,
        TEST_DEPENDENCY_EVENT_NAME,
        TEST_ISOLATED_EVENT_NAME,
    )

    EventSystem.TriggerEvent(TEST_EVENT_NAME)

    assert callback1.called == 1
    assert callback2.called == 1
    assert callback3.called == 1


def test_attach_multiple_events_so_when_modify_non_root_event_will_trigger_all_the_events():
    callback1 = Mock()
    callback2 = Mock()
    callback3 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.RegisterEvent(TEST_DEPENDENCY_EVENT_NAME, callback2)
    EventSystem.RegisterEvent(TEST_ISOLATED_EVENT_NAME, callback3)

    EventSystem.AttachEvent(
        TEST_EVENT_NAME,
        TEST_DEPENDENCY_EVENT_NAME,
        TEST_ISOLATED_EVENT_NAME,
    )

    EventSystem.TriggerEvent(TEST_DEPENDENCY_EVENT_NAME)

    assert callback1.called == 1
    assert callback2.called == 1
    assert callback3.called == 1


def test_complex_callback_dependency():
    callback1 = Mock()
    callback2 = Mock()
    callback3 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.RegisterEvent(TEST_DEPENDENCY_EVENT_NAME, callback2)
    EventSystem.RegisterEvent(TEST_ISOLATED_EVENT_NAME, callback3)

    EventSystem.AttachEvent(TEST_EVENT_NAME, TEST_DEPENDENCY_EVENT_NAME)
    EventSystem.AttachEvent(TEST_DEPENDENCY_EVENT_NAME, TEST_ISOLATED_EVENT_NAME)
    EventSystem.AttachEvent(TEST_ISOLATED_EVENT_NAME, TEST_EVENT_NAME)

    EventSystem.TriggerEvent(TEST_EVENT_NAME)

    assert callback1.called == 1
    assert callback2.called == 1
    assert callback3.called == 1


def test_multiple_callback_with_the_same_event_name():
    callback1 = Mock()
    callback2 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback2)

    EventSystem.TriggerEvent(TEST_EVENT_NAME)

    assert callback1.called == 1
    assert callback2.called == 1


def test_dependency_without_callback_is_also_triggered():
    callback1 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)

    EventSystem.AttachEvent(TEST_EVENT_NAME, TEST_DEPENDENCY_EVENT_NAME)

    EventSystem.TriggerEvent(TEST_DEPENDENCY_EVENT_NAME)

    assert callback1.called == 1


def test_call_the_event_with_arguments():
    callback1 = Mock()
    EventSystem.RegisterEvent(TEST_EVENT_NAME, callback1)

    EventSystem.TriggerEvent(TEST_EVENT_NAME, "test_argument1", "test_argument2")

    assert callback1.called == 1
    assert callback1.call_args.args == ("test_argument1", "test_argument2")
