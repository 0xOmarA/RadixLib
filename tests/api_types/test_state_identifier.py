from radixlib.api_types.identifiers import StateIdentifier
import dateparser
import unittest

class TestStateIdentifier(unittest.TestCase):
    """ Unit tests for the StateIdentifier class """

    def test_all_missing(self):
        """ Testing the case where a state identifier is passed with all missing arguments """

        # Creating the state identifier
        state_identifier: StateIdentifier = StateIdentifier()

        self.assertEqual(state_identifier.to_dict(), {})

    def test_only_version(self):
        """ Testing the case where only a version is given. """

        # Creating the state identifier
        state_identifier: StateIdentifier = StateIdentifier(
            version = 123922
        )

        self.assertEqual(state_identifier.to_dict(), {"version": 123922})

    def test_only_timestamp(self):
        """ Testing the case where only a timestamp is given. """

        # Creating the state identifier
        state_identifier: StateIdentifier = StateIdentifier(
            timestamp = dateparser.parse('2022-02-01T11:28:53.707Z')
        )

        self.assertEqual(state_identifier.to_dict(), {"timestamp": "2022-02-01T11:28:53.707Z"})

    def test_only_epoch(self):
        """ Testing the case where only an epoch is given. """

        # Creating the state identifier
        state_identifier: StateIdentifier = StateIdentifier(
            epoch = 322,
        )

        self.assertEqual(state_identifier.to_dict(), {"epoch": 322})

    def test_only_epoch_and_round(self):
        """ Testing the case where only an epoch and round are given. """

        # Creating the state identifier
        state_identifier: StateIdentifier = StateIdentifier(
            epoch = 322,
            round = 12
        )

        self.assertEqual(state_identifier.to_dict(), {"epoch": 322, "round": 12})

    def test_only_round_given(self):
        """ Testing the case where only a round is given """

        try:
            # Creating the state identifier
            StateIdentifier(
                round = 12
            )
            self.assertTrue(True is False)
        except:
            self.assertTrue(True is True)

    def test_only_timestamp_and_epoch(self):
        """ Testing the case where only a timestamp and an epoch """

        try:
            # Creating the state identifier
            StateIdentifier(
                timestamp = dateparser.parse('2022-02-01T11:28:53.707Z'),
                round = 12,
            )
            self.assertTrue(True is False)
        except:
            self.assertTrue(True is True)