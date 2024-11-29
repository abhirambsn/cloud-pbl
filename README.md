# File Manager App

This is a basic file manager app with user authentication, file uploads to S3, and deployment on EC2.

## Setup

1. Deploy the database (PostgreSQL) and configure RDS.
```bash
aws rds create-db-subnet-group \
    --db-subnet-group-name localstack-db-subnet-group \
    --db-subnet-group-description "DB Subnet Group for LocalStack" \
    --subnet-ids subnet-11111111 subnet-22222222 \
    --endpoint-url http://localhost:4566 \
    --profile local


aws rds create-db-cluster \
    --db-cluster-identifier localstack-rds-cluster \
    --engine aurora-postgresql \
    --master-username admin \
    --master-user-password MySecurePassword123 \
    --db-subnet-group-name localstack-db-subnet-group \
    --backup-retention-period 1 \
    --endpoint-url http://localhost:4566 \
    --profile local

aws rds create-db-instance \
    --db-instance-identifier localstack-rds-instance \
    --db-cluster-identifier localstack-rds-cluster \
    --engine aurora-postgresql \
    --db-instance-class db.t3.medium \
    --endpoint-url http://localhost:4566 \
    --profile local

aws rds describe-db-clusters \
    --db-cluster-identifier localstack-rds-cluster \
    --query "DBClusters[0].Endpoint" \
    --endpoint-url http://localhost:4566 \
    --profile local
```
2. Set up S3 for file storage.
```bash
aws s3api create-bucket \
    --bucket file-manager-bucket \
    --endpoint-url http://localhost:4566 \
    --profile local

aws s3api list-buckets \
    --endpoint-url http://localhost:4566 \
    --profile local

aws s3api put-bucket-policy \
    --bucket file-manager-bucket \
    --policy file://bucket-policy.json \
    --endpoint-url http://localhost:4566 \
    --profile local
```
3. Deploy the app using EC2.
```bash
aws ec2 create-key-pair \
    --key-name local-key-pair \
    --query "KeyMaterial" \
    --output text \
    --endpoint-url http://localhost:4566 \
    --profile local > local-key-pair.pem

chmod 400 local-key-pair.pem

aws ec2 create-security-group \
    --group-name local-security-group \
    --description "Security group for LocalStack EC2" \
    --endpoint-url http://localhost:4566 \
    --profile local

aws ec2 authorize-security-group-ingress \
    --group-name local-security-group \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0 \
    --endpoint-url http://localhost:4566 \
    --profile local

aws ec2 authorize-security-group-ingress \
    --group-name local-security-group \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0 \
    --endpoint-url http://localhost:4566 \
    --profile local

aws ec2 run-instances \
    --image-id ami-df5de72bdb3b \
    --count 1 \
    --instance-type t2.micro \
    --key-name local-key-pair \
    --security-groups local-security-group \
    --endpoint-url http://localhost:4566 \
    --profile local

aws ec2 describe-instances \
    --endpoint-url http://localhost:4566 \
    --profile local
    
# To Stop / Terminate

aws ec2 stop-instances \
    --instance-ids <instance-id> \
    --endpoint-url http://localhost:4566 \
    --profile local

aws ec2 terminate-instances \
    --instance-ids <instance-id> \
    --endpoint-url http://localhost:4566 \
    --profile local
```

## Features

- User registration and login.
- File upload and management.
- S3 integration for object storage.
