"""
Caleb Hendrix

The inspiration for this systematic policy came from the time travel testing framework:

Dong, Z., Böhme, M., Cojocaru, L., & Roychoudhury, A. (2020). Time-travel testing of Android apps. 
IEEE/ACM 42nd International Conference on Software Engineering (ICSE). https://doi.org/10.1145/3377811.3380402
"""

from ast import Tuple
import copy
import sys
from typing import List, Dict

from droidbot.utg import UTG

# Max number of state revisits before we return to the last fittest state
MAX_NUM_STATE_REVISITS = 10

# Minimum number of out edges in a state to make it interesting
MIN_NUM_EDGES = 5

"""
The Goals of this implementation:

Specify what makes an "interesting" state and save those states as we encounter them

Specify when we encounter a lack of progress

Create an algorithm to go back to the most progressive state when we encounter lack of progress
"""

class SystematicExplorationPolicy(object):
    """
    This policy is inspired by time travel testing
    """

    #-----------------------------------------------------------------------------------------
    def __init__(self, utg: UTG):

        # Structure to store the interesting states as determined by is_interesting
        # States are stored as their state string identifier
        self.interesting_states = []

        self.utg = utg

        # Data structure:
        #   str: the state string of the current state
        #   int: the times during utg-based seed generation this state has been selected
        self.state_selection_times_history: Dict[str, int] = {}

        # In order to support the time travel functionality we need another structure
        self.current_seed_test_info: List[Tuple[Dict, str, int]] = []

    #-----------------------------------------------------------------------------------------
    def is_interesting(self, state_str):
        # We define an interesting state as one that has many out edges,
        # or the ability to travel to many other states
        if state_str not in self.interesting_states:
            events = self.utg.G.out_edges(nbunch=state_str, data="events")
            
            if (len(events) >= MIN_NUM_EDGES):
                return True
            else:
                return False
        else:
            return False

    #-----------------------------------------------------------------------------------------
    def select_fittest_state(self):
        fittest_state = self.interesting_states[0]
        for state in self.interesting_states:
            if self.is_stuck(state):
                pass
            elif self.state_selection_times_history[state] < \
                self.state_selection_times_history[fittest_state]:
                fittest_state = state

    #-----------------------------------------------------------------------------------------
    def is_stuck(self, state_str):
        # We define that the we are stuck on a state if we have re-visited that state
        # a certain number of times
        return self.state_selection_times_history[state_str] > MAX_NUM_STATE_REVISITS
    
    #-----------------------------------------------------------------------------------------
    def travel_back_to_state(self, goal_state, seed_test: List[Dict], seed_test_str: str, seed_test_length: int):
        # This method implements the ability to travel back to previously interesting states and begin the 
        # seed test generation from that state. When we encounter this state again, the algorithm will prefer
        # the event with the least actions taken on it so we will go through a different path

        stop_traveling = False

        new_seed_test = None
        new_seed_test_str = None
        new_seed_test_length = None

        while not stop_traveling:
            current_length = len(self.current_seed_test_info) - 1

            if self.current_seed_test_info[current_length][1] != goal_state:
                self.current_seed_test_info.pop(current_length)

                popped_seed_test = seed_test.pop(current_length)
                new_seed_test = seed_test

                new_seed_test_str = seed_test_str.replace(" -(%d)-> " % popped_seed_test['id'], "")

                seed_test_length -= 1
                new_seed_test_length = seed_test_length
            else:
                stop_traveling = True
        
        return new_seed_test, new_seed_test_str, new_seed_test_length

    #-----------------------------------------------------------------------------------------
    def generate_systematic_seed_tests(self, max_seed_test_length, max_seed_test_suite_size):
        """
        Generate systematic seed tests from the utg model
        Specifically, we select the clustered utg as the test generation model.
        """

        # Data structure:
        #   int: the utg event id
        #   int: the selected times during utg-based seed generation
        event_selection_times_history: Dict[int, int] = {}

        # Data structure:
        #   Dict: the event dict that corresponds to utg's events,
        #       i.e., {"event" : event, "id": utg_event_id}
        seed_test_suite: List[List[Dict]] = []

        current_test_suite_size = 0
        first_state_str = self.utg.first_state_str

        while current_test_suite_size < max_seed_test_suite_size:

            current_seed_test: List[Dict] = []
            current_seed_test_str = ""
            current_seed_test_length = 0

            next_state_str = first_state_str

            # Between seed tests being created, we want to clear the interesting states
            # and clear our tracking of states visited
            self.interesting_states.clear()
            self.state_selection_times_history.clear()
            self.current_seed_test_info.clear()

            while current_seed_test_length < max_seed_test_length:

                # data structure:
                #   Dict: event info (including input event, event id)
                #   str: the end state str
                #   int: the selection times of this event
                candidate_events: List[Tuple[Dict, str, int]] = []

                # the minimum selection times for an event
                min_event_selection_times = sys.maxsize

                # When we visit a state we want to track the amount of visits
                if next_state_str not in self.state_selection_times_history:
                    self.state_selection_times_history[next_state_str] = 0
                else:
                    self.state_selection_times_history[next_state_str] += 1

                # We determine if we have encountered an interesting state, if so,
                # we add it to the list of interesting states
                if (self.is_interesting(next_state_str)):
                    self.interesting_states.append(next_state_str)

                # Now we need to check if we are stuck on this state,
                # if we are we should go back to a more interesting state
                if (self.is_stuck(next_state_str)):
                    next_state_str = self.select_fittest_state()

                    # We need to first backtrack the current seed test to align
                    # with this new next state
                    current_seed_test, current_seed_test_str, current_seed_test_length = \
                        self.travel_back_to_state(next_state_str, current_seed_test, current_seed_test_str, current_seed_test_length)


                # get the out edges of the current state
                for (start_state_str, end_state_str, events) in \
                        self.utg.G.out_edges(nbunch=next_state_str, data="events"):

                    for event_str in events:
                        # collect candidate events
                        utg_event_dict = events[event_str]
                        event_id = utg_event_dict['id']

                        if event_id not in event_selection_times_history:
                            # create the selection history for these events
                            event_selection_times_history[event_id] = 0

                        if min_event_selection_times > event_selection_times_history[event_id]:
                            # get the minimum selection times
                            min_event_selection_times = event_selection_times_history[event_id]

                        candidate_events.append(
                            (utg_event_dict, end_state_str, event_selection_times_history[event_id]))

                if len(candidate_events) == 0:
                    # stop the search if we reach an ending state in the utg
                    break

                # We want to select the event which has either not been taken yet,
                # or we have not taken very often, thus we are able to systematecally
                # go through each event and thus visit each state
                selected_event = candidate_events[0]
                for index in range(len(candidate_events)):
                    if selected_event[2] == 0:
                        break
                    if selected_event[2] > candidate_events[index][2]:
                        selected_event = candidate_events[index]

                # Here we keep track of the info for this seed test
                self.current_seed_test_info.append(copy.deepcopy(selected_event))

                # We update the end_state_str here so that we move to next state
                end_state_str = selected_event[1]

                # Now we need to extract the Dict in the selection
                selected_event_dict = selected_event[0]
                
                current_seed_test_str += (" -(%d)-> " % selected_event_dict['id'])

                # deepcopy the event dict to avoid disturbing the utg itself
                current_seed_test.append(copy.deepcopy(selected_event_dict))
                current_seed_test_length += 1

                # increase selection times
                event_selection_times_history[selected_event_dict['id']] += 1

                # update the next state
                next_state_str = end_state_str

            seed_test_suite.append(current_seed_test)
            print("the seed test [%d]: %s" % (current_test_suite_size + 1, current_seed_test_str))
            current_test_suite_size += 1

        edge_coverage = len(event_selection_times_history) * 1.0 / self.utg.effective_event_count
        print("the edge coverage: %f(=%d/%d)" % (edge_coverage,
                                                 len(event_selection_times_history),
                                                 len(self.utg.G.edges)))
        return seed_test_suite