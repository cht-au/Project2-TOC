from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")
        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        PARENT_INDEX = -1
        INIT_TRANSITION = -1
        initial_config = ["", self.start_state, input_string, PARENT_INDEX, INIT_TRANSITION]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False
        accepting_node = None

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            for index, (left, state, right, p, t) in enumerate(current_level):
                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                # print([left, state, right])
                if state == self.accept_state:
                    accepted = True
                    accepting_node = (left, state, right)
                    break
                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    # print("\nRejected Path:")
                    # self.print_trace_path((left, state, right, p, t), tree)
                    continue

                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                # 5. If no explicit transition exists, treat as implicit Reject.
                read_symbol = right[0] if right else '_'
                if state not in self.transitions:
                    next_level.append([left, self.reject_state, right, index, -1])
                    continue # don't try to find transition for this

                valid_transitions = []
                for transition_index, transition in enumerate(self.transitions[state]):
                    if transition['read'][0] == read_symbol:
                        valid_transitions.append((transition_index, transition))
                if not valid_transitions:
                    next_level.append([left, self.reject_state, right, index, -1])
                    continue

                all_rejected = False # at least one valid transition possible


                # 6. Generate children configurations and append to next_level[cite: 148].
                for transition_index, transition in valid_transitions:
                    new_state = transition['next']
                    write_sym = transition['write'][0]
                    move_dir = transition['move'][0]

                    if right:
                        updated_right = write_sym + right[1:]
                    else: # if blank
                        updated_right = write_sym
                    
                    # move head
                    if move_dir == 'R':
                        new_left = left + updated_right[0]
                        new_right = updated_right[1:] if len(updated_right) > 1 else ""
                    elif move_dir == 'L':
                        if left: # if left is not blank to make sure we don't go out of bounds
                            head_symbol = left[-1] # immedient left of current state or head_symbol of new state
                            new_left = left[:-1]
                        else: # left is blank
                            head_symbol = "_"
                            new_left = ""
                        new_right = head_symbol + updated_right
                    
                    next_level.append([new_left, new_state, new_right,index,transition_index])
            if accepted:
                # print(tree)
                break
            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f'String rejected in depth {len(tree) - 1}')
                self.print_depth_and_trans(tree)
                return

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
        
        if accepted:
            final_node = next(node for node in tree[-1] if node[0] == accepting_node[0] and node[1] == accepting_node[1] and node[2] == accepting_node[2])
            self.print_depth_and_trans(tree)
            self.print_trace_path(final_node, tree)


    def print_trace_path(self, final_node, tree):
        path = []
        node = final_node
        level = len(tree) - 1  # start at last level

        while True:
            path.append(node)
            parent_index = node[3]
            if parent_index == -1:
                break  # reached root
            level -= 1
            node = tree[level][parent_index]

        print(f"String accepted in {len(tree) - 1} transitions")
        path.reverse()
        for depth, (left, state, right, parent, trans) in enumerate(path):
            print(f"Depth {depth}: '{left}', '{state}', '{right}'")

    def print_depth_and_trans(self, tree):     
        # count number of transitions
        total_transitions = sum(len(level) for level in tree)

        print(f"Tree Depth: {len(tree) - 1}")
        print(f"Transitions simulated: {total_transitions}")