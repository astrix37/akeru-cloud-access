# Akeru Cloud Access

### About Akeru
Akeru the two faced lion was an egyptian god that protected gods and kings during his time in Egypt and will protect your 
access to the AWS cloud!

There are two main functions of this package:
* Create IAM roles / users with policies attached for users to log in as or as service roles
* Facilitate access to these IAM roles / users based on django user / group status. 

### Usage

#### Credentials
Akeru currently assumes that the credentials will be available via the environment through standard mechanisms offered 
by [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

Credentials are used in 3 key actions within the package: 
1. Assume a target role to generate temporary credentials.
2. Assume an account role used to create user keys
3. Create read template policy objects to create users/roles 

Such a system is not needed to support it's current setup, but will allow for expanding into a multi cloud environment 
where users and roles are created / assumed in accounts outside of the account this app runs in.
This is not a feature that Akeru is optimized for and is not yet enabled.

#### Policy Templates
Policies are mapped to users / roles on a 1-1 basis. Features like multiple policies or permission boundaries are not
supported by Akeru. Policies are stored in an S3 bucket and can be pointed to by specifying POLICY_BUCKET and POLICY_PREFIX
in your django settings file. There is no current support to modify the framework to allow for storing templates in
other locations (ie local file system or as IAM policies). 

#### User and Role access 
A policy template can be used create an 'AWSRole' object which specifies a number of parameters including but not
limited to whether it's a user or a role, role trust policy, if it's an EC2 or lambda service role.

Once you have created an 'AWSRole', you are now able to create an 'AccessRole' that provisions access to the underlying
'AWSRole'. This can be tied to a django user / group and users are then able to log in via the /access/ page. 

#### Settings
Required Settings
* ACCOUNT_ID (The account ID that this application is operating in / for)
* POLICY_BUCKET (The bucket that IAM policies are stored in)
* POLICY_PREFIX (The prefix that policies are stored under)
* DEFAULT_TRUST_POLICY (The default trust policy that is added to roles)
 
Optional Settings
* REMOTE_ACCESS_ROLE (akeru-cloud-access)
* ASSUMED_ROLE_TIMEOUT (60 * 60)
* FEDERATED_USER_TIMEOUT (60 * 60)

Recommended not to change 
* *EC2_TRUST_POLICY (policy provided when checking 'ec2' on AWSRole)*
* *LAMBDA_TRUST_POLICY (policy provided when checking 'lambda' on AWSRole)*

### Required Setup
#### Akeru Application Policy 
Create this IAM role and assign credentials to Akeru
```

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole",
                "s3:Get*"
                "s3:List*"
            ]
            "Resource": "*"
        }
    ]
}
``` 

#### Akeru Remote Policy 
Create this IAM role and allow the previous role to assume it. This will need to be the same as the default trust policy
specified below.
```

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:*"
            ],
            "Resource": "*"
        }
    ]
}
``` 

#### Default Trust Policy 
specify this in your settings
```
DEFAULT_TRUST_POLICY = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
            "arn:aws:iam::<ACCOUNT_ID>:role/<name_of_local_akeru_role>"
        ]
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}
"""
```