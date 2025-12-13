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
        initial_config = ["", self.start_state, input_string]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False

        #finding what the accepted and rejected states are:
        accept_state = self.accept_state
        reject_state = self.reject_state
        states = self.states
        trans = self.transitions
        #for key, items in trans.items():
         #   print(f"{key}: {items}")

        #Turing machine configuration
        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = [] # each config gets [left, state, right, [parent index, parent depth], transition]
            all_rejected = True

            # 1. Iterate through every config in current_level.
            for index, config in enumerate(current_level):
                state = ""
                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                for item in config:
                    if item in states: state = item # find state that it is in:
                    if state == accept_state:
                        print("Success!")
                        accepted=True
                        all_rejected=False
                        self.print_trace_path(config, tree)
                        break
                    elif state == reject_state: break # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if accepted: break # outer for loop breaks to while
            
                # find valid transitions:
                if state in trans:
                    past = config[0]
                    next = config[2]
                    if len(config[2])==0: next_input = ''
                    else: next_input = config[2][0] #look at next input
                    s_transitions = trans[state]
                    for t in s_transitions:
                       
                        if next_input in t['read']:
                             # moving right
                            if t['move'][0] == 'R':
                                new_left = past + t['write'][0]
                                if not next[1:]:
                                    new_right = '_'
                                else:
                                    new_right = next[1:]
                                next_level.append([new_left, t['next'], new_right, [index, depth], t]) #Generate children configurations and append to next_level[cite: 148].
                            #moving left
                            elif t['move'][0] =='L':
                                if not past:
                                    new_left = ''
                                    new_right = '_'+ t['write'][0] + next
                                else:
                                    new_left = past[:-1]
                                    new_right = past[-1] + t['write'][0] + next[:1]
                                next_level.append([new_left, t['next'], new_right, [index, depth], t]) #Generate children configurations and append to next_level[cite: 148].
                else: break # no transisiton off of the state so treat as reject 


            # Placeholder for logic:
            # need to record maximum depth of rejected state:
            deepest = depth+1
            if not next_level and all_rejected:
                # Handle "String rejected" output [cite: 258]
                print("String Rejected!")
                print(f"Longest Path: {deepest}")
                break
            #print(next_level)
            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]

    def print_trace_path(self, final_node, tree):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        path = []
        curr_node = final_node
        while len(curr_node) == 5:
            # append node to path:
            tree_index = curr_node[3][1]
            curr_depth = tree_index+1
            depth_index = curr_node[3][0]
            
            path.append({
            'level': curr_depth,
            'w_left': curr_node[0],  # Element 0: w_left
            'state': curr_node[1],   # Element 1: state
            'w_right': curr_node[2], # Element 2: w_right
            })
            #print(path)
            #print(curr_node[-1])
            curr_node = tree[tree_index][depth_index]
            
        
        #add root node:
        path.append({
            'level': 0,
            'w_left': curr_node[0],  # Element 0: w_left
            'state': curr_node[1],   # Element 1: state
            'w_right': curr_node[2], # Element 2: w_right
            })
        
        path.reverse() #sort from root to the end
        
        for node in path:
            print(f"{node['w_left']}{node['state']}{node['w_right']}")

        #print(path)
        