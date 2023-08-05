# probator-auditor-cloudtrail

Please open issues in the [Probator](https://gitlab.com/probator/probator/issues/new?labels=auditor-cloudtrail) repository

## Description

This auditor ensures that CloudTrail:

* Is enabled globally on multi-region
* Logs to a central location
* Has SNS/SQS notifications enabled and being sent to the correct queues
* Regional trails (of our chosen name) are not enabled

## Configuration Options

| Option name           | Default Value | Type      | Description                                                               |
|-----------------------|---------------|-----------|---------------------------------------------------------------------------|
| bucket\_name          | *None*        | string    | Name of the S3 bucket to send CloudTrail logs to                          |
| bucket\_region        | us-west-2     | string    | Region to create S3 bucket in                                             |
| cloudtrail\_region    | us-west-2     | string    | Region to create CloudTrail in                                            |
| enabled               | False         | bool      | Enable the CloudTrail auditor                                             |
| interval              | 60            | int       | Run frequency in minutes                                                  |
| resource\_tags        | *None*        | list      | List of tags, in `key=value` format. Empty value disabled tag management  |
| s3\_archive\_days     | 31            | int       | Days after which files go to cold storage. Empty or `0` value to disable  |
| s3\_kms\_key\_id      | *None*        | string    | KMS Key ID for S3 SSE encryption. If empty, uses the default AWS KMS Key  |
| sns\_topic\_name      | *None*        | string    | SNS topic name for CloudTrail log delivery                                |
| sqs\_queue\_arn       | *None*        | string    | ARN of the SQS queue receiving log notifications                          |
| trail\_name           | us-west-2     | string    | Name of the trail to create                                               |


Based on the work by Riot Games' [Cloud Inquisitor](https://github.com/RiotGames/cloud-inquisitor)
