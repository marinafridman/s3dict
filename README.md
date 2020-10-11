# s3dict
Class for python interface with AWS. Adapted from the [s3dict](https://github.com/RhetTbull/s3dict) class by RhetTbull.

* Allows storing, retrieving and deleting from an s3 bucket programatically. 
* Allows access to the list of keys or key-value pairs in s3 bucket, and permits filtering by prefix strings.

See example.py for a demonstration of how to instantiate the class and use methods. 

Requires AWS access info, including
* AWS bucket name
* AWS access key ID
* AWS secret key

This information should be provided in a user-generated file called 'credentials.csv'. See example_credentials.csv for format.
