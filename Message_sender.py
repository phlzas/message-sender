import pywhatkit as kit
import datetime
import tkinter as tk
from tkinter import ttk, StringVar, messagebox
import time
import threading

# Global stop flag
stop_flag = False

def send_message_with_logging(participant, message):
    """Send a message and return the status."""
    try:
        current_time = datetime.datetime.now()
        scheduled_time = current_time + datetime.timedelta(minutes=1, seconds=15)
        hour, minute = scheduled_time.hour, scheduled_time.minute

        kit.sendwhatmsg(participant, message, hour, minute, wait_time=27, tab_close=True, close_time=2)
        return f"Message sent to {participant}."
    except Exception as e:
        return f"Failed to send message to {participant}: {e}"

def start_sending(progress_bar, percent_var, result_label, participants, instructor, message, main_frame, progress_frame):
    """Simulate message sending with a progress bar and return to main screen."""
    global stop_flag
    total_tasks = len(participants) + (1 if instructor else 0)
    step = 100 / total_tasks

    results = []
    completed = 0
    for participant in participants:
        
        if stop_flag:  # Check if the operation should stop
            messagebox.showwarning("Stopped", "Operation was stopped by the user.")
            break

        participant = participant.strip()
        if participant:
            result = send_message_with_logging(participant, message)
            results.append(result)
            completed += 1
            progress_bar['value'] += step
            percent_var.set(f"{int((completed / total_tasks) * 100)}%")
            result_label.update()
            time.sleep(0.5)  # Simulate time delay for better user feedback

    if not stop_flag and instructor:
        result = send_message_with_logging(instructor, message)
        results.append(result)
        completed += 1
        progress_bar['value'] += step
        percent_var.set(f"{int((completed / total_tasks) * 100)}%")
        result_label.update()
        time.sleep(0.5)

    if not stop_flag:
        # Show results if not stopped
        messagebox.showinfo("Results", "\n".join(results))
    else:
        messagebox.showinfo("Stopped", "Messages sending process stopped.")

    # Reset and go back to main frame
    stop_flag = False
    progress_bar['value'] = 0
    percent_var.set("0%")
    main_frame.tkraise()

def send_messages():
    """Handle sending messages and transition to progress bar."""
    global stop_flag
    participants = participants_entry.get().split(',')
    instructor = instructor_entry.get().strip()
    message = message_entry.get("1.0", tk.END).strip()

    if not message:
        messagebox.showerror("Error", "Message cannot be empty.")
        return

    # Transition to progress frame
    progress_frame.tkraise()

    # Start sending messages in a separate thread
    stop_flag = False
    threading.Thread(target=start_sending, args=(progress_bar, percent_var, progress_label, participants, instructor, message, main_frame, progress_frame)).start()

def stop_operation():
    """Stop the ongoing operation."""
    global stop_flag
    stop_flag = True

# Main UI setup
root = tk.Tk()
root.title("WhatsApp Message Sender")

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

tk.Label(main_frame, text="Participants (comma-separated):").pack(pady=5)
participants_entry = tk.Entry(main_frame, width=50)
participants_entry.pack(pady=5)

tk.Label(main_frame, text="Instructor's phone number:").pack(pady=5)
instructor_entry = tk.Entry(main_frame, width=50)
instructor_entry.pack(pady=5)

tk.Label(main_frame, text="Message:").pack(pady=5)
message_entry = tk.Text(main_frame, height=5, width=50)
message_entry.pack(pady=5)

send_button = tk.Button(main_frame, text="Send Messages", command=send_messages)
send_button.pack(pady=10)

# Progress frame
progress_frame = tk.Frame(root)
progress_frame.pack(fill="both", expand=True)

percent_var = StringVar(value="0%")
progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

percent_label = tk.Label(progress_frame, textvariable=percent_var)
percent_label.pack(pady=5)

progress_label = tk.Label(progress_frame, text="Sending messages...")
progress_label.pack(pady=5)

stop_button = tk.Button(progress_frame, text="Stop", command=stop_operation)
stop_button.pack(pady=10)

# Start with the main frame
main_frame.tkraise()

root.mainloop()
