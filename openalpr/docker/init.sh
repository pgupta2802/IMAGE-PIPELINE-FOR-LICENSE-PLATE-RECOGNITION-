#!/bin/bash

S3_FILE_PATH=$1

# exit if argument is not provided
if [ -z "$S3_FILE_PATH" ]; then
  echo "Error: init.sh missing <s3_file_path>"
  exit 1
fi

# copy file from s3 bucket to container
if ! aws s3 cp "s3://openalpr-image-upload/images/$S3_FILE_PATH" "/data/$S3_FILE_PATH"; then
  echo "Error: init.sh failed to download file from S3"
  exit 1
fi

# run openalpr
if ! alpr -j -n 1 "/data/$S3_FILE_PATH" > "/data/result.json"; then
  echo "Error: init.sh openalpr failed"
  exit 1
fi

# copy back result to s3
if ! aws s3 cp "/data/result.json" "s3://openalpr-image-upload/result/$S3_FILE_PATH"; then
  echo "Error: init.sh failed to upload result to S3"
  exit 1
fi

echo "init.sh done"