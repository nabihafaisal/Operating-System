
class Process:
    def __init__(self, process_id, arrival_time, execution_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def sjf_scheduling(processes):
    current_time = 0
    execution_order = []
    ready_queue = []

    while processes or ready_queue:
        # Add arriving processes to the ready queue
        for process in processes:
            if process.arrival_time <= current_time:
                ready_queue.append(process)
                processes.remove(process)

        if not ready_queue:
            current_time += 1
            continue

        # Sort the ready queue based on remaining execution time
        ready_queue.sort(key=lambda x: x.remaining_time)

        current_process = ready_queue.pop(0)

        # Record execution order
        execution_order.append((current_process.process_id, current_time))

        # Update start time and completion time
        current_process.start_time = current_time
        current_process.completion_time = current_time + current_process.remaining_time

        # Update remaining execution time
        current_time += current_process.remaining_time
        current_process.remaining_time = 0

    return execution_order

if __name__ == "__main__":
    num_processes = int(input("Enter the number of processes (3 to 5): "))
    
    if num_processes < 3 or num_processes > 5:
        print("Number of processes must be between 3 and 5.")
        exit()

    processes = []
    for i in range(num_processes):
        arrival_time = int(input(f"Enter arrival time for Process {i + 1}: "))
        execution_time = int(input(f"Enter execution time for Process {i + 1} (<= 10): "))
        
        if execution_time > 10:
            print("Execution time must be <= 10.")
            exit()

        processes.append(Process(i + 1, arrival_time, execution_time))

    execution_order = sjf_scheduling(processes)
    
    # Print Gantt Chart
    print("\nGantt Chart:")
    for i in range(len(execution_order) - 1):
        process_id, start_time = execution_order[i]
        next_start_time = execution_order[i + 1][1]
        print(f"| P{process_id} ({start_time}-{next_start_time})", end=" ")
        
    if execution_order:
            last_process_id, last_start_time = execution_order[-1]
            last_process = next((p for p in processes if p.process_id == last_process_id), None)
            if last_process:
                print(f"| P{last_process_id} ({last_start_time}-{last_start_time + last_process.execution_time})", end=" |")
            else:
                print(f"| P{last_process_id} ({last_start_time}-", end=" ")
        
            # Handle any remaining processes that arrive after the last completed one
    while processes:
        processes.sort(key=lambda x: x.arrival_time)
        next_process = processes.pop(0)
        current_time = max(current_time, next_process.arrival_time)
        print(f"{current_time + next_process.execution_time})", end=" |\n")