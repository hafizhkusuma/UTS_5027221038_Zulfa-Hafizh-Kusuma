import grpc
import student_pb2
import student_pb2_grpc
from colorama import Fore, Style, init

# Initialize colorama
init()

def add_point(stub, student_id=None, points=None):
    if not student_id:
        student_id = input("Enter student ID: ")
    if not points:
        points = int(input("Enter points to add: "))
    response = stub.AddPoint(student_pb2.AddPointRequest(student_id=student_id, points=points))
    print("AddPoint response:", response.message)

def get_point(stub):
    student_id = input("Enter student ID: ")
    response = stub.GetPoint(student_pb2.GetPointRequest(student_id=student_id))
    if response.points < 75 and response.points != -1:
        print(f"Total points: {Fore.RED}{response.points}{Style.RESET_ALL}")
    elif response.points == -1:
        print("Student not found.")
    else:
        print("Total points:", response.points)

def update_point(stub):
    student_id = input("Enter student ID: ")
    
    # Check if student exists
    check_response = stub.GetPoint(student_pb2.GetPointRequest(student_id=student_id))
    if check_response.points == -1:
        print("Student not found.")
        consent = input("Do you want to add this student? (y/n): ").strip().lower()
        if consent == 'y':
            add_point(stub, student_id)
        else:
            print("Student not added. Operation aborted.")
        return

    additional_points = int(input("Enter additional points: "))
    response = stub.UpdatePoint(student_pb2.UpdatePointRequest(student_id=student_id, points=additional_points))
    if response.success:
        print("UpdatePoint response:", response.message)
    else:
        print("Failed to update points.")

def delete_point(stub):
    student_id = input("Enter student ID: ")
    response = stub.DeletePoint(student_pb2.DeletePointRequest(student_id=student_id))
    print("DeletePoint response:", response.message)

def get_all_points(stub):
    response = stub.GetAllPoints(student_pb2.GetAllPointsRequest())
    for student in response:
        if student.points < 75:
            print(f"Student ID: {student.student_id}, Points: {Fore.RED}{student.points}{Style.RESET_ALL}")
        else:
            print(f"Student ID: {student.student_id}, Points: {student.points}")

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = student_pb2_grpc.StudentServiceStub(channel)

    while True:
        print("1. Add Point")
        print("2. Get Total Point by ID")
        print("3. Update Point")
        print("4. Delete Point")
        print("5. Get All Points")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_point(stub)
        elif choice == "2":
            get_point(stub)
        elif choice == "3":
            update_point(stub)
        elif choice == "4":
            delete_point(stub)
        elif choice == "5":
            get_all_points(stub)
        elif choice == "6":
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    run()
