import grpc
import tkinter as tk
from tkinter import messagebox
import student_pb2
import student_pb2_grpc

class StudentClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Points Manager")

        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = student_pb2_grpc.StudentServiceStub(self.channel)

        self.create_widgets()

    def create_widgets(self):
        # Add Point Frame
        self.add_point_frame = tk.Frame(self.root)
        self.add_point_frame.pack(pady=10)

        tk.Label(self.add_point_frame, text="Add Point").grid(row=0, column=0, columnspan=2)
        tk.Label(self.add_point_frame, text="Student ID:").grid(row=1, column=0)
        self.add_point_student_id_entry = tk.Entry(self.add_point_frame)
        self.add_point_student_id_entry.grid(row=1, column=1)
        tk.Label(self.add_point_frame, text="Points:").grid(row=2, column=0)
        self.add_point_entry = tk.Entry(self.add_point_frame)
        self.add_point_entry.grid(row=2, column=1)
        self.add_point_button = tk.Button(self.add_point_frame, text="Add Point", command=self.add_point)
        self.add_point_button.grid(row=3, column=0, columnspan=2)

        # Get Point Frame
        self.get_point_frame = tk.Frame(self.root)
        self.get_point_frame.pack(pady=10)

        tk.Label(self.get_point_frame, text="Get Total Point by ID").grid(row=0, column=0, columnspan=2)
        tk.Label(self.get_point_frame, text="Student ID:").grid(row=1, column=0)
        self.get_point_student_id_entry = tk.Entry(self.get_point_frame)
        self.get_point_student_id_entry.grid(row=1, column=1)
        self.get_point_button = tk.Button(self.get_point_frame, text="Get Point", command=self.get_point)
        self.get_point_button.grid(row=2, column=0, columnspan=2)

        # Update Point Frame
        self.update_point_frame = tk.Frame(self.root)
        self.update_point_frame.pack(pady=10)

        tk.Label(self.update_point_frame, text="Update Point").grid(row=0, column=0, columnspan=2)
        tk.Label(self.update_point_frame, text="Student ID:").grid(row=1, column=0)
        self.update_point_student_id_entry = tk.Entry(self.update_point_frame)
        self.update_point_student_id_entry.grid(row=1, column=1)
        tk.Label(self.update_point_frame, text="Additional Points:").grid(row=2, column=0)
        self.update_point_entry = tk.Entry(self.update_point_frame)
        self.update_point_entry.grid(row=2, column=1)
        self.update_point_button = tk.Button(self.update_point_frame, text="Update Point", command=self.update_point)
        self.update_point_button.grid(row=3, column=0, columnspan=2)

        # Delete Point Frame
        self.delete_point_frame = tk.Frame(self.root)
        self.delete_point_frame.pack(pady=10)

        tk.Label(self.delete_point_frame, text="Delete Point").grid(row=0, column=0, columnspan=2)
        tk.Label(self.delete_point_frame, text="Student ID:").grid(row=1, column=0)
        self.delete_point_student_id_entry = tk.Entry(self.delete_point_frame)
        self.delete_point_student_id_entry.grid(row=1, column=1)
        self.delete_point_button = tk.Button(self.delete_point_frame, text="Delete Point", command=self.delete_point)
        self.delete_point_button.grid(row=2, column=0, columnspan=2)

        # Get All Points Frame
        self.get_all_points_frame = tk.Frame(self.root)
        self.get_all_points_frame.pack(pady=10)

        self.get_all_points_button = tk.Button(self.get_all_points_frame, text="Get All Points", command=self.get_all_points)
        self.get_all_points_button.grid(row=0, column=0)

        self.get_all_points_text = tk.Text(self.get_all_points_frame, height=10, width=50)
        self.get_all_points_text.grid(row=1, column=0)

        # Add tags for red text
        self.get_all_points_text.tag_config('red', foreground='red')

    def add_point(self):
        student_id = self.add_point_student_id_entry.get()
        points = self.add_point_entry.get()
        if not student_id or not points:
            messagebox.showwarning("Input Error", "Please enter both Student ID and Points")
            return

        response = self.stub.AddPoint(student_pb2.AddPointRequest(student_id=student_id, points=int(points)))
        messagebox.showinfo("Add Point", response.message)

    def get_point(self):
        student_id = self.get_point_student_id_entry.get()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter Student ID")
            return

        response = self.stub.GetPoint(student_pb2.GetPointRequest(student_id=student_id))
        if response.points == -1:
            messagebox.showinfo("Get Point", "Student not found.")
        else:
            points_display = f"Total points: {response.points}"
            if response.points < 75:
                points_display = f"Total points: {response.points}"
                messagebox.showinfo("Get Point", points_display, icon='warning')
            else:
                messagebox.showinfo("Get Point", points_display)

    def update_point(self):
        student_id = self.update_point_student_id_entry.get()
        additional_points = self.update_point_entry.get()
        if not student_id or not additional_points:
            messagebox.showwarning("Input Error", "Please enter both Student ID and Additional Points")
            return

        # Check if student exists
        check_response = self.stub.GetPoint(student_pb2.GetPointRequest(student_id=student_id))
        if check_response.points == -1:
            consent = messagebox.askyesno("Student not found", "Student not found. Do you want to add this student?")
            if consent:
                self.add_point_student_id_entry.insert(0, student_id)
                self.add_point_entry.insert(0, additional_points)
                self.add_point()
            else:
                messagebox.showinfo("Operation Aborted", "Student not added.")
            return

        response = self.stub.UpdatePoint(student_pb2.UpdatePointRequest(student_id=student_id, points=int(additional_points)))
        if response.success:
            messagebox.showinfo("Update Point", response.message)
        else:
            messagebox.showwarning("Update Failed", "Failed to update points.")

    def delete_point(self):
        student_id = self.delete_point_student_id_entry.get()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter Student ID")
            return

        response = self.stub.DeletePoint(student_pb2.DeletePointRequest(student_id=student_id))
        messagebox.showinfo("Delete Point", response.message)

    def get_all_points(self):
        response = self.stub.GetAllPoints(student_pb2.GetAllPointsRequest())
        self.get_all_points_text.delete('1.0', tk.END)
        for student in response:
            if student.points < 75:
                self.get_all_points_text.insert(tk.END, f"Student ID: {student.student_id}, Points: {student.points}\n", 'red')
            else:
                self.get_all_points_text.insert(tk.END, f"Student ID: {student.student_id}, Points: {student.points}\n")

if __name__ == '__main__':
    root = tk.Tk()
    app = StudentClientApp(root)
    root.mainloop()
