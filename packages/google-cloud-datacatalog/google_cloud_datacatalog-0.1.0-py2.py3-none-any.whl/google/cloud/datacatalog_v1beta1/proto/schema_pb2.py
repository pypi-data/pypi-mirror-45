# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/datacatalog_v1beta1/proto/schema.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/cloud/datacatalog_v1beta1/proto/schema.proto",
    package="google.cloud.datacatalog.v1beta1",
    syntax="proto3",
    serialized_options=_b(
        "\n\034com.google.cloud.datacatalogP\001ZKgoogle.golang.org/genproto/googleapis/cloud/datacatalog/v1beta1;datacatalog\370\001\001"
    ),
    serialized_pb=_b(
        '\n3google/cloud/datacatalog_v1beta1/proto/schema.proto\x12 google.cloud.datacatalog.v1beta1"I\n\x06Schema\x12?\n\x07\x63olumns\x18\x02 \x03(\x0b\x32..google.cloud.datacatalog.v1beta1.ColumnSchema"\x93\x01\n\x0c\x43olumnSchema\x12\x0e\n\x06\x63olumn\x18\x06 \x01(\t\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0c\n\x04mode\x18\x03 \x01(\t\x12\x42\n\nsubcolumns\x18\x07 \x03(\x0b\x32..google.cloud.datacatalog.v1beta1.ColumnSchemaBp\n\x1c\x63om.google.cloud.datacatalogP\x01ZKgoogle.golang.org/genproto/googleapis/cloud/datacatalog/v1beta1;datacatalog\xf8\x01\x01\x62\x06proto3'
    ),
)


_SCHEMA = _descriptor.Descriptor(
    name="Schema",
    full_name="google.cloud.datacatalog.v1beta1.Schema",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="columns",
            full_name="google.cloud.datacatalog.v1beta1.Schema.columns",
            index=0,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=89,
    serialized_end=162,
)


_COLUMNSCHEMA = _descriptor.Descriptor(
    name="ColumnSchema",
    full_name="google.cloud.datacatalog.v1beta1.ColumnSchema",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="column",
            full_name="google.cloud.datacatalog.v1beta1.ColumnSchema.column",
            index=0,
            number=6,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="type",
            full_name="google.cloud.datacatalog.v1beta1.ColumnSchema.type",
            index=1,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="description",
            full_name="google.cloud.datacatalog.v1beta1.ColumnSchema.description",
            index=2,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="mode",
            full_name="google.cloud.datacatalog.v1beta1.ColumnSchema.mode",
            index=3,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="subcolumns",
            full_name="google.cloud.datacatalog.v1beta1.ColumnSchema.subcolumns",
            index=4,
            number=7,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=165,
    serialized_end=312,
)

_SCHEMA.fields_by_name["columns"].message_type = _COLUMNSCHEMA
_COLUMNSCHEMA.fields_by_name["subcolumns"].message_type = _COLUMNSCHEMA
DESCRIPTOR.message_types_by_name["Schema"] = _SCHEMA
DESCRIPTOR.message_types_by_name["ColumnSchema"] = _COLUMNSCHEMA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Schema = _reflection.GeneratedProtocolMessageType(
    "Schema",
    (_message.Message,),
    dict(
        DESCRIPTOR=_SCHEMA,
        __module__="google.cloud.datacatalog_v1beta1.proto.schema_pb2",
        __doc__="""Represents a schema (e.g. BigQuery, GoogleSQL, Avro schema).
  
  
  Attributes:
      columns:
          Schema of columns. A maximum of 10,000 columns and sub-columns
          can be specified.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.datacatalog.v1beta1.Schema)
    ),
)
_sym_db.RegisterMessage(Schema)

ColumnSchema = _reflection.GeneratedProtocolMessageType(
    "ColumnSchema",
    (_message.Message,),
    dict(
        DESCRIPTOR=_COLUMNSCHEMA,
        __module__="google.cloud.datacatalog_v1beta1.proto.schema_pb2",
        __doc__="""Representation of a column within a schema. Columns could be nested
  inside other columns.
  
  
  Attributes:
      column:
          Required. Name of the column.
      type:
          Required. Type of the column.
      description:
          Description of the column.
      mode:
          A column's mode indicates whether the values in this column
          are required, nullable, etc. Only 'NULLABLE', 'REQUIRED' and
          'REPEATED' are supported, default mode is 'NULLABLE'.
      subcolumns:
          Schema of sub-columns.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.datacatalog.v1beta1.ColumnSchema)
    ),
)
_sym_db.RegisterMessage(ColumnSchema)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
