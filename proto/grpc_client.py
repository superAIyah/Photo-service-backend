import PhotoService_pb2
import PhotoService_pb2_grpc
from time import localtime, strftime
import grpc

class grpc_client():
    def __init__(self):
        channel = grpc.insecure_channel('localhost:9009')
        self.stub = PhotoService_pb2_grpc.PhotoStub(channel)
        
    def get_photo_request(self, uuid):
        request = PhotoService_pb2.PhotoRequest(uuid=uuid)
        response = self.stub.requestPhoto(request)
        print(f'[Get response] uuid:{ uuid }')
        return response
        
    def add_photo_request(self, uuid, image):        
        request = PhotoService_pb2.AddPhotoRequest(uuid=uuid, image=image)
        response = self.stub.addPhoto(request)
        print(f'[Add response] uuid:{ uuid } { response }')
        return response
    
    def remove_photo_request(self, uuid):        
        request = PhotoService_pb2.RemovePhotoRequest(uuid=uuid)
        response = self.stub.removePhoto(request)
        print(f'[Remove response] uuid:{ uuid } { response }')
        return response