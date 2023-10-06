class Process:
    def __init__(self, pid, arrival_time, execution_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.resume_time = 0
        self.turn_around_time = 0
        self.utilization_time = 0
        self.instructions_executed = 0
        self.interrupt_count = 0 
        self.status='RUNNING'
   


    def execute(self, quantum_size):
      
        if self.remaining_time > quantum_size:
            self.remaining_time -= quantum_size
            self.instructions_executed += quantum_size
            return quantum_size
        else:
            time_executed = self.remaining_time
            self.instructions_executed += self.remaining_time  
            self.remaining_time = 0
            return time_executed
        
    def increment_interrupt_count(self):
        self.interrupt_count += 1

  
    




def main():
    min_processes = 3
    max_processes = 5
    min_execution_time = 1
    max_execution_time = 10
    max_quantum_size = 3
    gantt_chart = []
    status_transitions=[]
    blocked_processes = []
    
 

    # Input number of processes from the user
    num_processes = int(input(f"How many processes do you want to create ({min_processes} to {max_processes}): "))
    if num_processes < min_processes or num_processes > max_processes:
        print("Invalid number of processes.")
        return

    # Input arrival and execution times for each process
    processes = []
    for i in range(num_processes):
        arrival_time = i * 3  # Arrival time of the first process is 0, subsequent processes arrive every 3 units.
        execution_time = int(input(f"Enter execution time for process P{i + 1} ({min_execution_time} to {max_execution_time}): "))
        if execution_time < min_execution_time or execution_time > max_execution_time:
            print(f"Invalid execution time for process P{i + 1}.")
            return
        processes.append(Process(i + 1, arrival_time, execution_time))

    # Input quantum size from the user
    quantum_size = int(input(f"Enter quantum size ({min_execution_time} to {max_quantum_size}): "))
    if quantum_size < min_execution_time or quantum_size > max_quantum_size:
        print("Invalid quantum size.")
        return
        
    current_time = 0
    ready_queue = processes.copy()
    finish_time = 0
    index=0

    while ready_queue:
           
                current_process = ready_queue.pop(0)
             # Add to the list of blocked processes
               
                # Calculate the number of instructions to be executed in this quantum
                instructions_to_execute = min(quantum_size, current_process.remaining_time)

                # Execute the current process with the calculated number of instructions
                execution_time = current_process.execute(instructions_to_execute)

                # Update the current time and finish time
                current_time += execution_time
                finish_time = max(finish_time, current_time)

                # Store the current time as the process's resume time before checking completion
                current_process.resume_time = current_time

                # Calculate the number of instructions executed during this execution
                instructions_executed = current_process.execution_time - current_process.remaining_time
                gantt_chart.extend([current_process.pid] * instructions_to_execute)
            
                status_transitions.append(('RUNNING', current_process))  # Append Running status
                if current_process.pid == 2:
                     status_transitions.append(('BLOCKED', current_process))
                     blocked_process = current_process
                     gantt_chart.extend(['X'] * quantum_size)
                    
                else:
           
                    if current_process.remaining_time == 0:
                        current_process.turn_around_time = current_time - current_process.arrival_time
                        status_transitions.append(('COMPLETE', current_process))  # Append Complete status
                    else:
                        status_transitions.append(('PENDING', current_process))  # Append Pending status
                        ready_queue.append(current_process)
                        current_process.increment_interrupt_count()
                      
                        
                    # Store the number of instructions executed within the process object
                if(instructions_executed % quantum_size==0):
                    current_process.instructions_executed = instructions_executed/quantum_size
                else:
                        current_process.instructions_executed = instructions_executed/quantum_size+0.5 
                    
                

                    # Calculate utilization time for each process (execution time / finish time)
                for process in processes:
                    process.utilization_time = process.execution_time / finish_time
                
                print("\nGantt Chart:")
                for i in range(0, len(gantt_chart), quantum_size):
                            print("+------", end='')
                print("+")
                for i in range(0, len(gantt_chart), quantum_size):
                            print("|P ", gantt_chart[i], " ", end='')
                print("|")
                for i in range(0, len(gantt_chart), quantum_size):
                            print("+------", end='')
                print("+")
             
                
               


    while blocked_process and blocked_process.remaining_time > 0:
                execution_time = blocked_process.execute(blocked_process.remaining_time)
                current_time += execution_time
                status_transitions.append(('RUNNING', blocked_process))
                if blocked_process.remaining_time == 0:
                    status_transitions.append(('COMPLETE', blocked_process))  # Append Complete status
                else:
                    status_transitions.append(('PENDING', blocked_process)) 
        
                        


    for status, process in status_transitions:
     print_process_info(process, status, quantum_size, finish_time)


def print_process_info(process, status, quantum_size, finish_time):
    print("\nProcess Control Information:")
    print(f"Process ID: P{process.pid}")
    print(f"Quantum Size: {quantum_size}")
    print(f"Arrival Time: {process.arrival_time}")
    print(f"ExecutionTime: {process.execution_time}")
    print(f"Process Status Word: {status}")
    if status=="BLOCKED":
        print(f"Resources: I/O Requirement")
    else:
         print(f"Resources:?")
    print(f"Process Resume Time Address: {process.resume_time}")
    print(f"No of instructions: {process.instructions_executed}")
    print(f"Turn Around Time: {process.turn_around_time}")
    print(f"Utilization Time: {process.utilization_time:.2f}")
    print(f"Interrupt Count: {process.interrupt_count}")
    print(f"Scheduling Algo: Round Robin")
    print(f"Finish Time: {finish_time}")





if __name__ == "__main__":
    main()
































