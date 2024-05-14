import grpc
from concurrent import futures
import time
import pymongo
import student_pb2
import student_pb2_grpc

class StudentService(student_pb2_grpc.StudentServiceServicer):

    def __init__(self):
        # Koneksi MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["student_database"]
        self.collection = self.db["students"]

    def AddPoint(self, request, context):
        student_id = request.student_id
        points = request.points

        # Konversi data protobuf ke JSON
        data = {
            "_id": student_id,
            "points": points
        }

        # Simpan data ke MongoDB
        self.collection.update_one({"_id": student_id}, {"$set": data}, upsert=True)

        return student_pb2.AddPointResponse(success=True, message="Points added successfully")

    def GetPoint(self, request, context):
        student_id = request.student_id

        # Dapatkan data dari MongoDB
        student_data = self.collection.find_one({"_id": student_id})

        if student_data:
            points = student_data.get("points", 0)
            return student_pb2.GetPointResponse(points=points)
        else:
            return student_pb2.GetPointResponse(points=-1)  # Indikasi bahwa data tidak ditemukan

    def UpdatePoint(self, request, context):
        student_id = request.student_id
        points = request.points

        # Dapatkan data dari MongoDB
        student_data = self.collection.find_one({"_id": student_id})

        if not student_data:
            return student_pb2.UpdatePointResponse(success=False, message="Student not found")

        # Update poin
        student_data["points"] += points

        # Simpan data ke MongoDB
        self.collection.update_one({"_id": student_id}, {"$set": student_data}, upsert=True)

        return student_pb2.UpdatePointResponse(success=True, message="Points updated successfully")

    def DeletePoint(self, request, context):
        student_id = request.student_id

        # Hapus data dari MongoDB
        self.collection.delete_one({"_id": student_id})

        return student_pb2.DeletePointResponse(success=True, message="Points deleted successfully")

    def GetAllPoints(self, request, context):
        # Dapatkan semua data dari MongoDB
        all_students = self.collection.find()
        for student in all_students:
            yield student_pb2.GetAllPointsResponse(student_id=student["_id"], points=student["points"])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_pb2_grpc.add_StudentServiceServicer_to_server(StudentService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at :50051")
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
