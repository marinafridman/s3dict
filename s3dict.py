import boto3
import traceback


class S3Dict(object):
    """
    S3Dict is a python3 class for accessing S3 with an interface similar to a python `dict`.
    
        
    """
    
    def __init__(self, bucket_name=None, access_key_id=None, access_secret_key=None, autosave=False): 
        """ initialize class """ 
        # check whether credentials are all present
        if (bucket_name == None or access_key_id == None or access_secret_key == None):
            raise ValueError("bucket_name, access_key_id and access_secret_key must be specified")
            
        # save credentials as attributes    
        self.__BUCKET_NAME = bucket_name
        self.__AWS_ACCESS_KEY_ID = access_key_id 
        self.__AWS_SECRET_ACCESS_KEY = access_secret_key
        
        # open connection to s3
        self.__S3 = boto3.resource("s3", 
                             aws_access_key_id=access_key_id, 
                             aws_secret_access_key=access_secret_key) 
                             
        # save list of objects currently in bucket as attribute                    
        self.objs = self.__S3.Bucket(self.__BUCKET_NAME).objects.all()

    def __getitem__(self, key):
        """ takes in key (str), retrieves item from bucket """
        obj = self.__S3.Object(self.__BUCKET_NAME, key).get()["Body"].read()
        return obj
        

    def __setitem__(self, key, value):
        """ takes in key (str) and value (BytesIO), saves item to bucket """
        try:
            # add object to bucket
            self.__S3.Bucket(self.__BUCKET_NAME).put_object(Key=key, Body=value)
            
        except Exception as e:
            raise Exception(f"Error saving item to {self.__S3}: {e} {traceback.print_exc}")
        
        # update objects list
        self.objs = self.__S3.Bucket(self.__BUCKET_NAME).objects.all()

    def __delitem__(self, key):
        """ takes in key (str), deletes item from bucket """
        try:
            # delete object from bucket
            self.__S3.Object(self.__BUCKET_NAME, key).delete()     
        except Exception as e:
            raise Exception(f"Error deleting item from {self.__s3}: {e} {traceback.print_exc}")
            
        # update objects list
        self.objs = self.__S3.Bucket(self.__BUCKET_NAME).objects.all()
        

    def __contains__(self, key): 
        """ takes in key (str), checks whether key is present in bucket """
        keys = list(map(lambda x: x.key, self.objs))
        return key in keys

    def get(self, key):
        """ takes in key (str), checks whether key is in bucket, if so, 
        retrieves item from bucket, otherwise raises ValueError """
        if self.__contains__(key):
            return self.__getitem__(key)
        else:
            raise ValueError("No object with that key exists.")

    def put(self, key, value):
        """ takes in key (str) and value (BytesIO), adds to bucket """
        self.__setitem__(key, value)

    def pop(self, key):
        """ takes in key (str), checks whether key is in bucket, if so, 
        returns item from bucket and deletes from bucket, 
        otherwise raises ValueError """
        if self.__contains__(key):
            obj = self.__getitem__(key)
            self.__delitem__(key)
            return obj
        else:
            raise ValueError("No object with that key exists.")

    def keys(self, prefix=''):
        """ takes optional prefix (str). returns list of all keys in bucket.
        if prefix is provided, only keys that start with prefix are returned"""
        keys = list(map(lambda x: x.key, self.objs))
        keys = list(filter(lambda x: x.startswith(prefix), keys))
        return keys

    def items(self, prefix=''):
        """ takes optional prefix (str). returns list of tuples of all key-value pairs in bucket.
        if prefix is provided, only keys that start with prefix are returned """
        tups = list(map(lambda x: (x.key,self.__getitem__(x.key)) if x.key.startswith(prefix) else None, self.objs))
        return [x for x in tups if x is not None]
