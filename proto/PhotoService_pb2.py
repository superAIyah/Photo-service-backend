# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PhotoService.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12PhotoService.proto\x12\x15\x63om.photoService.grpc\"\x1c\n\x0cPhotoRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\".\n\x0f\x41\x64\x64PhotoRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\x0c\"\"\n\x12RemovePhotoRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"\x1e\n\rPhotoResponse\x12\r\n\x05image\x18\x01 \x01(\x0c\"/\n\x10\x41\x64\x64PhotoResponse\x12\x0e\n\x06status\x18\x01 \x01(\x08\x12\x0b\n\x03url\x18\x02 \x01(\t\"%\n\x13RemovePhotoResponse\x12\x0e\n\x06status\x18\x01 \x01(\x08\x32\xa5\x02\n\x05Photo\x12Y\n\x0crequestPhoto\x12#.com.photoService.grpc.PhotoRequest\x1a$.com.photoService.grpc.PhotoResponse\x12[\n\x08\x61\x64\x64Photo\x12&.com.photoService.grpc.AddPhotoRequest\x1a\'.com.photoService.grpc.AddPhotoResponse\x12\x64\n\x0bremovePhoto\x12).com.photoService.grpc.RemovePhotoRequest\x1a*.com.photoService.grpc.RemovePhotoResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'PhotoService_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PHOTOREQUEST._serialized_start=45
  _PHOTOREQUEST._serialized_end=73
  _ADDPHOTOREQUEST._serialized_start=75
  _ADDPHOTOREQUEST._serialized_end=121
  _REMOVEPHOTOREQUEST._serialized_start=123
  _REMOVEPHOTOREQUEST._serialized_end=157
  _PHOTORESPONSE._serialized_start=159
  _PHOTORESPONSE._serialized_end=189
  _ADDPHOTORESPONSE._serialized_start=191
  _ADDPHOTORESPONSE._serialized_end=238
  _REMOVEPHOTORESPONSE._serialized_start=240
  _REMOVEPHOTORESPONSE._serialized_end=277
  _PHOTO._serialized_start=280
  _PHOTO._serialized_end=573
# @@protoc_insertion_point(module_scope)