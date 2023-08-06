from boto3.s3.transfer import TransferConfig
from boto3.resources.collection import ResourceCollection
from typing import IO
from typing import Union
from typing import List
from typing import Optional
from botocore.client import BaseClient
from typing import Callable
from typing import Dict
from datetime import datetime
from boto3.resources import base


class ServiceResource(base.ServiceResource):
    buckets: 'buckets'

    def Bucket(self, name: str = None) -> 'Bucket':
        pass

    def BucketAcl(self, bucket_name: str = None) -> 'BucketAcl':
        pass

    def BucketCors(self, bucket_name: str = None) -> 'BucketCors':
        pass

    def BucketLifecycle(self, bucket_name: str = None) -> 'BucketLifecycle':
        pass

    def BucketLifecycleConfiguration(self, bucket_name: str = None) -> 'BucketLifecycleConfiguration':
        pass

    def BucketLogging(self, bucket_name: str = None) -> 'BucketLogging':
        pass

    def BucketNotification(self, bucket_name: str = None) -> 'BucketNotification':
        pass

    def BucketPolicy(self, bucket_name: str = None) -> 'BucketPolicy':
        pass

    def BucketRequestPayment(self, bucket_name: str = None) -> 'BucketRequestPayment':
        pass

    def BucketTagging(self, bucket_name: str = None) -> 'BucketTagging':
        pass

    def BucketVersioning(self, bucket_name: str = None) -> 'BucketVersioning':
        pass

    def BucketWebsite(self, bucket_name: str = None) -> 'BucketWebsite':
        pass

    def MultipartUpload(self, bucket_name: str = None, object_key: str = None, id: str = None) -> 'MultipartUpload':
        pass

    def MultipartUploadPart(self, bucket_name: str = None, object_key: str = None, multipart_upload_id: str = None, part_number: str = None) -> 'MultipartUploadPart':
        pass

    def Object(self, bucket_name: str = None, key: str = None) -> 'Object':
        pass

    def ObjectAcl(self, bucket_name: str = None, object_key: str = None) -> 'ObjectAcl':
        pass

    def ObjectSummary(self, bucket_name: str = None, key: str = None) -> 'ObjectSummary':
        pass

    def ObjectVersion(self, bucket_name: str = None, object_key: str = None, id: str = None) -> 'ObjectVersion':
        pass

    def create_bucket(self, Bucket: str, ACL: str = None, CreateBucketConfiguration: Dict = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWrite: str = None, GrantWriteACP: str = None, ObjectLockEnabledForBucket: bool = None) -> 'Bucket':
        pass

    def get_available_subresources(self) -> List[str]:
        pass


class Bucket(base.ServiceResource):
    creation_date: datetime
    name: str
    multipart_uploads: 'multipart_uploads'
    object_versions: 'object_versions'
    objects: 'objects'

    def copy(self, CopySource: Dict = None, Key: str = None, ExtraArgs: Dict = None, Callback: Callable = None, SourceClient: BaseClient = None, Config: TransferConfig = None):
        pass

    def create(self, ACL: str = None, CreateBucketConfiguration: Dict = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWrite: str = None, GrantWriteACP: str = None, ObjectLockEnabledForBucket: bool = None) -> Dict:
        pass

    def delete(self):
        pass

    def delete_objects(self, Delete: Dict, MFA: str = None, RequestPayer: str = None, BypassGovernanceRetention: bool = None) -> Dict:
        pass

    def download_file(self, Key: str = None, Filename: str = None, ExtraArgs: Dict = None, Callback: Callable = None, Config: TransferConfig = None):
        pass

    def download_fileobj(self, Fileobj: IO = None, Key: str = None, ExtraArgs: Dict = None, Callback: Callable = None, Config: TransferConfig = None):
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put_object(self, Key: str, ACL: str = None, Body: Union[bytes, IO] = None, CacheControl: str = None, ContentDisposition: str = None, ContentEncoding: str = None, ContentLanguage: str = None, ContentLength: int = None, ContentMD5: str = None, ContentType: str = None, Expires: datetime = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWriteACP: str = None, Metadata: Dict = None, ServerSideEncryption: str = None, StorageClass: str = None, WebsiteRedirectLocation: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, SSEKMSKeyId: str = None, RequestPayer: str = None, Tagging: str = None, ObjectLockMode: str = None, ObjectLockRetainUntilDate: datetime = None, ObjectLockLegalHoldStatus: str = None) -> 'Object':
        pass

    def upload_file(self, Filename: str = None, Key: str = None, ExtraArgs: Dict = None, Callback: Callable = None, Config: TransferConfig = None):
        pass

    def upload_fileobj(self, Fileobj: IO = None, Key: str = None, ExtraArgs: Dict = None, Callback: Callable = None, Config: TransferConfig = None):
        pass

    def wait_until_exists(self):
        pass

    def wait_until_not_exists(self):
        pass


class BucketAcl(base.ServiceResource):
    owner: Dict
    grants: List
    bucket_name: str

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, ACL: str = None, AccessControlPolicy: Dict = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWrite: str = None, GrantWriteACP: str = None):
        pass

    def reload(self):
        pass


class BucketCors(base.ServiceResource):
    cors_rules: List
    bucket_name: str

    def delete(self):
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, CORSConfiguration: Dict):
        pass

    def reload(self):
        pass


class BucketLifecycle(base.ServiceResource):
    rules: List
    bucket_name: str

    def delete(self):
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, LifecycleConfiguration: Dict = None):
        pass

    def reload(self):
        pass


class BucketLifecycleConfiguration(base.ServiceResource):
    rules: List
    bucket_name: str

    def delete(self):
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, LifecycleConfiguration: Dict = None):
        pass

    def reload(self):
        pass


class BucketLogging(base.ServiceResource):
    logging_enabled: Dict
    bucket_name: str

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, BucketLoggingStatus: Dict):
        pass

    def reload(self):
        pass


class BucketNotification(base.ServiceResource):
    topic_configurations: List
    queue_configurations: List
    lambda_function_configurations: List
    bucket_name: str

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, NotificationConfiguration: Dict):
        pass

    def reload(self):
        pass


class BucketPolicy(base.ServiceResource):
    policy: str
    bucket_name: str

    def delete(self):
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, Policy: str, ConfirmRemoveSelfBucketAccess: bool = None):
        pass

    def reload(self):
        pass


class BucketRequestPayment(base.ServiceResource):
    payer: str
    bucket_name: str

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, RequestPaymentConfiguration: Dict):
        pass

    def reload(self):
        pass


class BucketTagging(base.ServiceResource):
    tag_set: List
    bucket_name: str

    def delete(self):
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, Tagging: Dict):
        pass

    def reload(self):
        pass


class BucketVersioning(base.ServiceResource):
    status: str
    mfa_delete: str
    bucket_name: str

    def enable(self, MFA: str = None):
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, VersioningConfiguration: Dict, MFA: str = None):
        pass

    def reload(self):
        pass

    def suspend(self, MFA: str = None):
        pass


class BucketWebsite(base.ServiceResource):
    redirect_all_requests_to: Dict
    index_document: Dict
    error_document: Dict
    routing_rules: List
    bucket_name: str

    def delete(self):
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, WebsiteConfiguration: Dict):
        pass

    def reload(self):
        pass


class MultipartUpload(base.ServiceResource):
    upload_id: str
    key: str
    initiated: datetime
    storage_class: str
    owner: Dict
    initiator: Dict
    bucket_name: str
    object_key: str
    id: str
    parts: 'parts'

    def abort(self, RequestPayer: str = None) -> Dict:
        pass

    def complete(self, MultipartUpload: Dict = None, RequestPayer: str = None) -> 'Object':
        pass

    def get_available_subresources(self) -> List[str]:
        pass


class MultipartUploadPart(base.ServiceResource):
    last_modified: datetime
    e_tag: str
    size: int
    bucket_name: str
    object_key: str
    multipart_upload_id: str
    part_number: str

    def copy_from(self, CopySource: Union[str, Dict], CopySourceIfMatch: str = None, CopySourceIfModifiedSince: datetime = None, CopySourceIfNoneMatch: str = None, CopySourceIfUnmodifiedSince: datetime = None, CopySourceRange: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, CopySourceSSECustomerAlgorithm: str = None, CopySourceSSECustomerKey: str = None, CopySourceSSECustomerKeyMD5: str = None, RequestPayer: str = None) -> Dict:
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def upload(self, Body: Union[bytes, IO] = None, ContentLength: int = None, ContentMD5: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None) -> Dict:
        pass


class Object(base.ServiceResource):
    delete_marker: bool
    accept_ranges: str
    expiration: str
    restore: str
    last_modified: datetime
    content_length: int
    e_tag: str
    missing_meta: int
    version_id: str
    cache_control: str
    content_disposition: str
    content_encoding: str
    content_language: str
    content_type: str
    expires: datetime
    website_redirect_location: str
    server_side_encryption: str
    metadata: Dict
    sse_customer_algorithm: str
    sse_customer_key_md5: str
    ssekms_key_id: str
    storage_class: str
    request_charged: str
    replication_status: str
    parts_count: int
    object_lock_mode: str
    object_lock_retain_until_date: datetime
    object_lock_legal_hold_status: str
    bucket_name: str
    key: str

    def copy(self, CopySource: Dict = None, ExtraArgs: Dict = None, Callback: Callable = None, SourceClient: BaseClient = None, Config: TransferConfig = None):
        pass

    def copy_from(self, CopySource: Union[str, Dict], ACL: str = None, CacheControl: str = None, ContentDisposition: str = None, ContentEncoding: str = None, ContentLanguage: str = None, ContentType: str = None, CopySourceIfMatch: str = None, CopySourceIfModifiedSince: datetime = None, CopySourceIfNoneMatch: str = None, CopySourceIfUnmodifiedSince: datetime = None, Expires: datetime = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWriteACP: str = None, Metadata: Dict = None, MetadataDirective: str = None, TaggingDirective: str = None, ServerSideEncryption: str = None, StorageClass: str = None, WebsiteRedirectLocation: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, SSEKMSKeyId: str = None, CopySourceSSECustomerAlgorithm: str = None, CopySourceSSECustomerKey: str = None, CopySourceSSECustomerKeyMD5: str = None, RequestPayer: str = None, Tagging: str = None, ObjectLockMode: str = None, ObjectLockRetainUntilDate: datetime = None, ObjectLockLegalHoldStatus: str = None) -> Dict:
        pass

    def delete(self, MFA: str = None, VersionId: str = None, RequestPayer: str = None, BypassGovernanceRetention: bool = None) -> Dict:
        pass

    def download_file(self, Filename: str = None, ExtraArgs: Dict = None, Callback: Callable = None, Config: TransferConfig = None):
        pass

    def download_fileobj(self, Fileobj: IO = None, ExtraArgs: Dict = None, Callback: Callable = None, Config: TransferConfig = None):
        pass

    def get(self, IfMatch: str = None, IfModifiedSince: datetime = None, IfNoneMatch: str = None, IfUnmodifiedSince: datetime = None, Range: str = None, ResponseCacheControl: str = None, ResponseContentDisposition: str = None, ResponseContentEncoding: str = None, ResponseContentLanguage: str = None, ResponseContentType: str = None, ResponseExpires: datetime = None, VersionId: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None, PartNumber: int = None) -> Dict:
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def initiate_multipart_upload(self, ACL: str = None, CacheControl: str = None, ContentDisposition: str = None, ContentEncoding: str = None, ContentLanguage: str = None, ContentType: str = None, Expires: datetime = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWriteACP: str = None, Metadata: Dict = None, ServerSideEncryption: str = None, StorageClass: str = None, WebsiteRedirectLocation: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, SSEKMSKeyId: str = None, RequestPayer: str = None, Tagging: str = None, ObjectLockMode: str = None, ObjectLockRetainUntilDate: datetime = None, ObjectLockLegalHoldStatus: str = None) -> 'MultipartUpload':
        pass

    def load(self):
        pass

    def put(self, ACL: str = None, Body: Union[bytes, IO] = None, CacheControl: str = None, ContentDisposition: str = None, ContentEncoding: str = None, ContentLanguage: str = None, ContentLength: int = None, ContentMD5: str = None, ContentType: str = None, Expires: datetime = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWriteACP: str = None, Metadata: Dict = None, ServerSideEncryption: str = None, StorageClass: str = None, WebsiteRedirectLocation: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, SSEKMSKeyId: str = None, RequestPayer: str = None, Tagging: str = None, ObjectLockMode: str = None, ObjectLockRetainUntilDate: datetime = None, ObjectLockLegalHoldStatus: str = None) -> Dict:
        pass

    def reload(self):
        pass

    def restore_object(self, VersionId: str = None, RestoreRequest: Dict = None, RequestPayer: str = None) -> Dict:
        pass

    def upload_file(self, Filename: str = None, ExtraArgs: Dict = None, Callback: Callable = None, Config: TransferConfig = None):
        pass

    def upload_fileobj(self, Fileobj: IO = None, ExtraArgs: Dict = None, Callback: Callable = None, Config: TransferConfig = None):
        pass

    def wait_until_exists(self, IfMatch: str = None, IfModifiedSince: datetime = None, IfNoneMatch: str = None, IfUnmodifiedSince: datetime = None, Range: str = None, VersionId: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None, PartNumber: int = None):
        pass

    def wait_until_not_exists(self, IfMatch: str = None, IfModifiedSince: datetime = None, IfNoneMatch: str = None, IfUnmodifiedSince: datetime = None, Range: str = None, VersionId: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None, PartNumber: int = None):
        pass


class ObjectAcl(base.ServiceResource):
    owner: Dict
    grants: List
    request_charged: str
    bucket_name: str
    object_key: str

    def get_available_subresources(self) -> List[str]:
        pass

    def load(self):
        pass

    def put(self, ACL: str = None, AccessControlPolicy: Dict = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWrite: str = None, GrantWriteACP: str = None, RequestPayer: str = None, VersionId: str = None) -> Dict:
        pass

    def reload(self):
        pass


class ObjectSummary(base.ServiceResource):
    last_modified: datetime
    e_tag: str
    size: int
    storage_class: str
    owner: Dict
    bucket_name: str
    key: str

    def copy_from(self, CopySource: Union[str, Dict], ACL: str = None, CacheControl: str = None, ContentDisposition: str = None, ContentEncoding: str = None, ContentLanguage: str = None, ContentType: str = None, CopySourceIfMatch: str = None, CopySourceIfModifiedSince: datetime = None, CopySourceIfNoneMatch: str = None, CopySourceIfUnmodifiedSince: datetime = None, Expires: datetime = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWriteACP: str = None, Metadata: Dict = None, MetadataDirective: str = None, TaggingDirective: str = None, ServerSideEncryption: str = None, StorageClass: str = None, WebsiteRedirectLocation: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, SSEKMSKeyId: str = None, CopySourceSSECustomerAlgorithm: str = None, CopySourceSSECustomerKey: str = None, CopySourceSSECustomerKeyMD5: str = None, RequestPayer: str = None, Tagging: str = None, ObjectLockMode: str = None, ObjectLockRetainUntilDate: datetime = None, ObjectLockLegalHoldStatus: str = None) -> Dict:
        pass

    def delete(self, MFA: str = None, VersionId: str = None, RequestPayer: str = None, BypassGovernanceRetention: bool = None) -> Dict:
        pass

    def get(self, IfMatch: str = None, IfModifiedSince: datetime = None, IfNoneMatch: str = None, IfUnmodifiedSince: datetime = None, Range: str = None, ResponseCacheControl: str = None, ResponseContentDisposition: str = None, ResponseContentEncoding: str = None, ResponseContentLanguage: str = None, ResponseContentType: str = None, ResponseExpires: datetime = None, VersionId: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None, PartNumber: int = None) -> Dict:
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def initiate_multipart_upload(self, ACL: str = None, CacheControl: str = None, ContentDisposition: str = None, ContentEncoding: str = None, ContentLanguage: str = None, ContentType: str = None, Expires: datetime = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWriteACP: str = None, Metadata: Dict = None, ServerSideEncryption: str = None, StorageClass: str = None, WebsiteRedirectLocation: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, SSEKMSKeyId: str = None, RequestPayer: str = None, Tagging: str = None, ObjectLockMode: str = None, ObjectLockRetainUntilDate: datetime = None, ObjectLockLegalHoldStatus: str = None) -> 'MultipartUpload':
        pass

    def load(self):
        pass

    def put(self, ACL: str = None, Body: Union[bytes, IO] = None, CacheControl: str = None, ContentDisposition: str = None, ContentEncoding: str = None, ContentLanguage: str = None, ContentLength: int = None, ContentMD5: str = None, ContentType: str = None, Expires: datetime = None, GrantFullControl: str = None, GrantRead: str = None, GrantReadACP: str = None, GrantWriteACP: str = None, Metadata: Dict = None, ServerSideEncryption: str = None, StorageClass: str = None, WebsiteRedirectLocation: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, SSEKMSKeyId: str = None, RequestPayer: str = None, Tagging: str = None, ObjectLockMode: str = None, ObjectLockRetainUntilDate: datetime = None, ObjectLockLegalHoldStatus: str = None) -> Dict:
        pass

    def restore_object(self, VersionId: str = None, RestoreRequest: Dict = None, RequestPayer: str = None) -> Dict:
        pass

    def wait_until_exists(self, IfMatch: str = None, IfModifiedSince: datetime = None, IfNoneMatch: str = None, IfUnmodifiedSince: datetime = None, Range: str = None, VersionId: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None, PartNumber: int = None):
        pass

    def wait_until_not_exists(self, IfMatch: str = None, IfModifiedSince: datetime = None, IfNoneMatch: str = None, IfUnmodifiedSince: datetime = None, Range: str = None, VersionId: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None, PartNumber: int = None):
        pass


class ObjectVersion(base.ServiceResource):
    e_tag: str
    size: int
    storage_class: str
    key: str
    version_id: str
    is_latest: bool
    last_modified: datetime
    owner: Dict
    bucket_name: str
    object_key: str
    id: str

    def delete(self, MFA: str = None, RequestPayer: str = None, BypassGovernanceRetention: bool = None) -> Dict:
        pass

    def get(self, IfMatch: str = None, IfModifiedSince: datetime = None, IfNoneMatch: str = None, IfUnmodifiedSince: datetime = None, Range: str = None, ResponseCacheControl: str = None, ResponseContentDisposition: str = None, ResponseContentEncoding: str = None, ResponseContentLanguage: str = None, ResponseContentType: str = None, ResponseExpires: datetime = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None, PartNumber: int = None) -> Dict:
        pass

    def get_available_subresources(self) -> List[str]:
        pass

    def head(self, IfMatch: str = None, IfModifiedSince: datetime = None, IfNoneMatch: str = None, IfUnmodifiedSince: datetime = None, Range: str = None, SSECustomerAlgorithm: str = None, SSECustomerKey: str = None, SSECustomerKeyMD5: str = None, RequestPayer: str = None, PartNumber: int = None) -> Dict:
        pass


class buckets(ResourceCollection):
    
    @classmethod
    def all(cls) -> List['Bucket']:
        pass

    
    @classmethod
    def filter(cls) -> List['Bucket']:
        pass

    
    @classmethod
    def iterator(cls) -> ResourceCollection:
        pass

    
    @classmethod
    def limit(cls) -> List['Bucket']:
        pass

    
    @classmethod
    def page_size(cls) -> List['Bucket']:
        pass

    
    @classmethod
    def pages(cls) -> List[base.ServiceResource]:
        pass
