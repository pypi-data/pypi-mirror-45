import json
import re
from dataclasses import dataclass

from botocore.exceptions import ClientError
from more_itertools import first
from probator import get_aws_session, get_local_aws_session, ProbatorError
from probator.config import dbconfig
from probator.constants import ConfigOption
from probator.log import auditlog
from probator.plugins import BaseAuditor
from probator.plugins.types.accounts import AWSAccount
from probator.utils import get_template
from probator.wrappers import retry

BUCKET_SETUP = False


@dataclass
class SQSQueueInfo:
    name: str
    region: str
    account_id: str


def get_queue_info(arn):
    """Parse an SQS ARN and return a SQSQueueInfo object

    Args:
        arn (str): The ARN to parse

    Returns:
        :obj:SQSQueueInfo
    """
    m = re.match(r'^arn:aws:sqs:(?P<region>[a-z0-9\-]+):(?P<account_id>\d+):(?P<name>.*)$', arn, re.I)
    if m:
        return SQSQueueInfo(**m.groupdict())
    else:
        raise ProbatorError(f'Unable to parse queue ARN: {arn}')


class CloudTrailAuditor(BaseAuditor):
    """CloudTrail auditor

    Ensures that CloudTrail is enabled and logging to a central location and that SNS/SQS notifications are enabled
    and being sent to the correct queues for the CloudTrail Logs application
    """

    name = 'CloudTrail'
    ns = 'auditor_cloudtrail'
    interval = dbconfig.get('interval', ns, 60)
    options = (
        ConfigOption(name='enabled', default_value=False, type='bool', description='Enable the Cloudtrail auditor'),
        ConfigOption(name='interval', default_value=60, type='int', description='Run frequency in minutes'),
        ConfigOption(name='bucket_name', default_value='', type='string', description='Name of the S3 bucket to send CloudTrail logs to'),
        ConfigOption(name='bucket_region', default_value='us-west-2', type='string', description='Region to create S3 bucket in'),
        ConfigOption(name='cloudtrail_region', default_value='us-west-2', type='string', description='Region to create CloudTrail in'),
        ConfigOption(name='sns_topic_name', default_value='', type='string', description='SNS topic name for CloudTrail log delivery'),
        ConfigOption(name='sqs_queue_arn', default_value='', type='string', description='SQS Queue ARN'),
        ConfigOption(name='trail_name', default_value='Probator_Auditing', type='string', description='Name of trail to create'),
        ConfigOption(name='resource_tags', default_value=[], type='array', description='List of tags in key=value format to apply'),
        ConfigOption(
            name='s3_archive_days',
            default_value=31,
            type='int',
            description='Number of days before moving S3 files to deep archive. If empty or zero, disables the lifecycle configuration'
        ),
        ConfigOption(
            name='s3_kms_key_id',
            default_value='',
            type='string',
            description='KMS Key ID to use for SSE. Will use default AWS key if not present'
        )
    )

    def __init__(self):
        super().__init__()

        self.accounts = list(AWSAccount.get_all(include_disabled=False).values())
        self.queue_arn = dbconfig.get(key='sqs_queue_arn', namespace=self.ns)
        self.resource_tags = dbconfig.get(key='resource_tags', namespace=self.ns)
        self.s3_acl = get_template(template='cloudtrail_s3_bucket_policy.json')
        self.s3_bucket_name = dbconfig.get(key='bucket_name', namespace=self.ns)
        self.s3_bucket_region = dbconfig.get(key='bucket_region', namespace=self.ns, default='us-west-2')
        self.s3_kms_key_id = dbconfig.get(key='s3_kms_key_id', namespace=self.ns)
        self.s3_archive_days = dbconfig.get(key='s3_archive_days', namespace=self.ns)
        self.sns_topic_name = dbconfig.get(key='sns_topic_name', namespace=self.ns)

    def run(self, *args, **kwargs):
        """Entry point for the scheduler

        Args:
            *args: Optional arguments
            **kwargs: Optional keyword arguments

        Returns:
            None
        """
        self.validate_s3_bucket()
        self.validate_sqs_policy()

        for account in self.accounts:
            ct = CloudTrail(
                account=account,
                bucket_name=self.s3_bucket_name,
                bucket_region=self.s3_bucket_region,
                logger=self.log
            )
            ct.run()

    def validate_s3_bucket(self):
        global BUCKET_SETUP

        if not BUCKET_SETUP:
            self.create_s3_bucket()
            self.update_bucket_encryption()
            self.update_bucket_lifecycle()
            self.update_bucket_tags()

            BUCKET_SETUP = True

    def create_s3_bucket(self):
        """Creates the S3 bucket on the account specified as the destination account for log files

        Returns:
            `None`
        """
        s3 = get_local_aws_session().client('s3', region_name=self.s3_bucket_region)

        # Check to see if the bucket already exists and if we have access to it
        try:
            s3.head_bucket(Bucket=self.s3_bucket_name)
        except ClientError as ex:
            status_code = ex.response['ResponseMetadata']['HTTPStatusCode']

            # Bucket exists and we do not have access
            if status_code == 403:
                raise Exception(f'Bucket {self.s3_bucket_name} already exists but we do not have access to it and so cannot continue')

            # Bucket does not exist, lets create one
            elif status_code == 404:
                s3.create_bucket(
                    ACL='private',
                    Bucket=self.s3_bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.s3_bucket_region
                    },

                )

                auditlog(
                    event='cloudtrail.create_s3_bucket',
                    actor=self.ns,
                    data={
                        'bucketRegion': self.s3_bucket_region,
                        'bucketName': self.s3_bucket_name
                    }
                )

        try:
            bucket_acl = self.s3_acl.render(bucket_name=self.s3_bucket_name)
            s3.put_bucket_policy(Bucket=self.s3_bucket_name, Policy=bucket_acl)

        except Exception as ex:
            raise Warning('An error occurred while setting bucket policy: {}'.format(ex))

    def update_bucket_encryption(self):
        """Validate bucket encryption settings

        Returns:
            `None`
        """
        s3 = get_local_aws_session().client('s3', region_name=self.s3_bucket_region)
        config = {
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                    }
                },
            ]
        }

        if self.s3_kms_key_id:
            config['Rules'][0]['ApplyServerSideEncryptionByDefault']['KMSMasterKeyID'] = self.s3_kms_key_id

        s3.put_bucket_encryption(
            Bucket=self.s3_bucket_name,
            ServerSideEncryptionConfiguration=config
        )

    def update_bucket_tags(self):
        """Validate bucket tags

        Returns:
            `None`
        """
        if self.resource_tags:
            s3 = get_local_aws_session().client('s3', region_name=self.s3_bucket_region)
            s3.put_bucket_tagging(
                Bucket=self.s3_bucket_name,
                Tagging={
                    'TagSet': [{'Key': k, 'Value': v} for k, v in map(lambda x: x.split('=', maxsplit=1), self.resource_tags)]
                }
            )

    def update_bucket_lifecycle(self):
        if self.s3_archive_days:
            s3 = get_local_aws_session().client('s3', region_name=self.s3_bucket_region)
            s3.put_bucket_lifecycle_configuration(
                Bucket=self.s3_bucket_name,
                LifecycleConfiguration={
                    'Rules': [
                        {
                            'ID': 'cold-storage',
                            'Prefix': '',
                            'Status': 'Enabled',
                            'Transitions': [
                                {
                                    'Days': self.s3_archive_days,
                                    'StorageClass': 'DEEP_ARCHIVE'
                                }
                            ]
                        }
                    ]
                }
            )

    def validate_sqs_policy(self):
        """Given a list of accounts, ensures that the SQS policy allows all the accounts to write to the queue

        Returns:
            `None`
        """
        session = get_local_aws_session()

        queue_info = get_queue_info(self.dbconfig.get(key='sqs_queue_arn', namespace=self.ns))
        sqs = session.client('sqs', region_name=queue_info.region)
        sqs_queue_url = sqs.get_queue_url(QueueName=queue_info.name)
        queue_attributes = sqs.get_queue_attributes(QueueUrl=sqs_queue_url['QueueUrl'], AttributeNames=['Policy'])

        if 'Attributes' not in queue_attributes:
            # In case the queue is fresh and has not been configured at all
            policy = {
                'Version': '2012-10-17',
                'Id': f'{self.queue_arn}/SQSDefaultPolicy',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {
                            'AWS': '*'
                        },
                        'Action': 'sqs:*',
                        'Resource': f'{self.queue_arn}',
                        'Condition': {
                            'ForAnyValue:ArnEquals': {
                                'aws:SourceArn': []
                            }
                        }
                    }
                ]
            }
        else:
            policy = json.loads(queue_attributes['Attributes']['Policy'])

        for account in self.accounts:
            arn = f'arn:aws:sns:*:{account.account_number}:{self.sns_topic_name}'
            source_arns = policy['Statement'][0]['Condition']['ForAnyValue:ArnEquals'].get('aws:SourceArn')
            if type(source_arns) == str:
                source_arns = [source_arns]

            if arn not in source_arns:
                self.log.warning(f'SQS policy is missing condition for ARN {arn}')
                source_arns.append(arn)

            policy['Statement'][0]['Condition']['ForAnyValue:ArnEquals']['aws:SourceArn'] = source_arns

        sqs.set_queue_attributes(
            QueueUrl=sqs_queue_url['QueueUrl'],
            Attributes={
                'Policy': json.dumps(policy, indent=4)
            }
        )


class CloudTrail(object):
    """CloudTrail object"""
    ns = 'auditor_cloudtrail'

    def __init__(self, account, bucket_name, bucket_region, logger):
        self.account = account
        self.bucket_region = bucket_region
        self.bucket_name = bucket_name
        self.log = logger

        # Config settings
        self.trail_region = dbconfig.get(key='cloudtrail_region', namespace=self.ns, default='us-west-2')
        self.topic_name = dbconfig.get(key='sns_topic_name', namespace=self.ns)
        self.trail_name = dbconfig.get(key='trail_name', namespace=self.ns)
        self.sqs_queue = dbconfig.get(key='sqs_queue_arn', namespace=self.ns)

        self.session = get_aws_session(account)
        self.ct = self.session.client('cloudtrail', region_name=self.trail_region)

    @retry
    def run(self):
        """Configures and enables a CloudTrail trail and logging on a single AWS Account.

        Has the capability to create both single region and multi-region trails.

        Will automatically create SNS topics, subscribe to SQS queues and turn on logging for the account in question,
        as well as reverting any manual changes to the trails if applicable.

        Returns:
            None
        """
        self.log.debug('Checking trails for {}/{}'.format(
            self.account.account_name,
            self.trail_region
        ))

        trail = self.get_trail()

        if not trail:
            try:
                self.create_cloudtrail(region=self.trail_region)
                trail = self.get_trail()
            except ClientError as ex:
                rex = ex.response['Error']['Code']

                if 'MaximumNumberOfTrailsExceededException' in rex:
                    self.log.warning(f'Unable to create a trail in {self.account.account_name}: {ex}')
                    return

                raise
        else:
            if not trail['IsMultiRegionTrail']:
                self.ct.update_trail(
                    Name=trail['Name'],
                    IncludeGlobalServiceEvents=True,
                    IsMultiRegionTrail=True
                )
                auditlog(
                    event='cloudtrail.update_trail',
                    actor=self.ns,
                    data={
                        'trailName': trail['Name'],
                        'account': self.account.account_name,
                        'region': self.trail_region,
                        'changes': [
                            {
                                'setting': 'IsMultiRegionTrail',
                                'oldValue': False,
                                'newValue': True
                            }
                        ]
                    }
                )

        self.validate_trail_settings(self.trail_region, trail)

    def get_trail(self):
        """Return the desired trail from the API if present

        Returns:
            `dict`
        """
        trails = self.ct.describe_trails().get('trailList', [])
        return first(filter(lambda t: t['Name'] == self.trail_name, trails), None)

    def validate_trail_settings(self, aws_region, trail):
        """Validates logging, SNS and S3 settings for the global trail.

        Has the capability to:

        - start logging for the trail
        - create SNS topics & queues
        - configure or modify a S3 bucket for logging

        """
        self.log.debug(f'Validating trail {self.account.account_name}/{aws_region}/{trail["Name"]}')
        status = self.ct.get_trail_status(Name=trail['Name'])
        if not status['IsLogging']:
            self.log.warning(f'Logging is disabled for {self.account.account_name}/{aws_region}/{trail["Name"]}')
            self.start_logging(
                region=aws_region,
                trail_name=trail['Name']
            )

        if 'SnsTopicName' not in trail or not trail['SnsTopicName']:
            self.log.warning(f'SNS Notifications not enabled for {self.account.account_name}/{aws_region}/{trail["Name"]}')
            self.create_sns_topic(region=aws_region)
            self.enable_sns_notification(region=aws_region, trail_name=trail['Name'])

        if not self.validate_sns_topic_subscription(region=aws_region):
            self.log.warning(f'SNS Notification configured but not subscribed for {self.account.account_name}/{aws_region}/{trail["Name"]}')
            self.subscribe_sns_topic_to_sqs(region=aws_region)

        if trail['S3BucketName'] != self.bucket_name:
            self.log.warning(
                f'CloudTrail is logging to an incorrect bucket for {self.account.account_name}/{trail["S3BucketName"]}/{trail["Name"]}'
            )
            self.set_s3_bucket(
                region=aws_region,
                trail_name=trail['Name'],
                bucket_name=self.bucket_name
            )

        if not trail.get('S3KeyPrefix') or trail['S3KeyPrefix'] != self.account.account_name:
            self.log.warning(f'Missing or incorrect S3KeyPrefix for {self.account.account_name}/{aws_region}/{trail["Name"]}')
            self.set_s3_prefix(
                region=aws_region,
                trail_name=trail['Name']
            )

    # region helper functions
    def create_sns_topic(self, *, region):
        """Creates an SNS topic if needed. Returns the ARN if the created SNS topic

        Args:
            region (str): Region name

        Returns:
            `str`
        """
        sns = self.session.client('sns', region_name=region)

        self.log.info(f'Creating SNS topic for {self.account.account_name}/{region}')
        # Create the topic
        res = sns.create_topic(Name=self.topic_name)
        arn = res['TopicArn']

        # Allow CloudTrail to publish messages with a policy update
        tmpl = get_template('cloudtrail_sns_policy.json')
        policy = tmpl.render(region=region, account_id=self.account.account_number, topic_name=self.topic_name)
        sns.set_topic_attributes(TopicArn=arn, AttributeName='Policy', AttributeValue=policy)

        auditlog(
            event='cloudtrail.create_sns_topic',
            actor=self.ns,
            data={
                'account': self.account.account_name,
                'region': region
            }
        )

        return arn

    def validate_sns_topic_subscription(self, *, region):
        """Validates SQS subscription to the SNS topic. Returns `True` if subscribed or `False` if not subscribed
        or topic is missing

        Args:
            region (str): Name of AWS Region

        Returns:
            `bool`
        """
        sns = self.session.client('sns', region_name=region)
        arn = f'arn:aws:sns:{region}:{self.account.account_number}:{self.topic_name}'
        try:
            data = sns.list_subscriptions_by_topic(TopicArn=arn)
        except ClientError:
            self.log.exception(f'Failed to list subscriptions by topic for {self.account.account_name}/{region}')
            return False

        for sub in data['Subscriptions']:
            if sub['Endpoint'] == self.sqs_queue:
                if sub['SubscriptionArn'] == 'PendingConfirmation':
                    self.log.warning(f'Subscription pending confirmation for {self.account.account_name}/{region}')
                    return False
                return True

        return False

    def subscribe_sns_topic_to_sqs(self, *, region):
        """Subscribe SQS to the SNS topic. Returns the ARN of the SNS Topic subscribed

        Args:
            region (`str`): Name of the AWS region

        Returns:
            `str`
        """
        sns = self.session.resource('sns', region_name=region)
        topic = sns.Topic(f'arn:aws:sns:{region}:{self.account.account_number}:{self.topic_name}')

        topic.subscribe(Protocol='sqs', Endpoint=self.sqs_queue)

        auditlog(
            event='cloudtrail.subscribe_sns_topic_to_sqs',
            actor=self.ns,
            data={
                'account': self.account.account_name,
                'region': region
            }
        )

        return topic.attributes['TopicArn']

    def create_cloudtrail(self, *, region):
        """Creates a new CloudTrail Trail

        Args:
            region (str): Name of the AWS region

        Returns:
            `None`
        """
        ct = self.session.client('cloudtrail', region_name=region)

        # Creating the sns topic for the trail prior to creation
        self.create_sns_topic(region=region)

        ct.create_trail(
            Name=self.trail_name,
            S3BucketName=self.bucket_name,
            S3KeyPrefix=self.account.account_name,
            IsMultiRegionTrail=True,
            IncludeGlobalServiceEvents=True,
            SnsTopicName=self.topic_name
        )
        self.subscribe_sns_topic_to_sqs(region=region)

        auditlog(
            event='cloudtrail.create_cloudtrail',
            actor=self.ns,
            data={
                'account': self.account.account_name,
                'region': region
            }
        )
        self.log.info(f'Created CloudTrail for {self.account.account_name}/{region}')

    def enable_sns_notification(self, *, region, trail_name):
        """Enable SNS notifications for a Trail

        Args:
            region (`str`): Name of the AWS region
            trail_name (`str`): Name of the CloudTrail Trail

        Returns:
            `None`
        """
        ct = self.session.client('cloudtrail', region_name=region)
        ct.update_trail(Name=trail_name, SnsTopicName=self.topic_name)

        auditlog(
            event='cloudtrail.enable_sns_notification',
            actor=self.ns,
            data={
                'account': self.account.account_name,
                'region': region
            }
        )
        self.log.info(f'Enabled SNS notifications for {self.account.account_name}/{region}/{trail_name}')

    def start_logging(self, *, region, trail_name):
        """Turn on logging for a CloudTrail Trail

        Args:
            region (`str`): Name of the AWS region
            trail_name (`str`): Name of the CloudTrail Trail

        Returns:
            `None`
        """
        ct = self.session.client('cloudtrail', region_name=region)
        ct.start_logging(Name=trail_name)

        auditlog(
            event='cloudtrail.start_logging',
            actor=self.ns,
            data={
                'account': self.account.account_name,
                'region': region
            }
        )
        self.log.info(f'Enabled logging for {self.account.account_name}/{region}/{trail_name}')

    def set_s3_prefix(self, *, region, trail_name):
        """Sets the S3 prefix for a CloudTrail Trail

        Args:
            region (`str`): Name of the AWS region
            trail_name (`str`): Name of the CloudTrail Trail

        Returns:
            `None`
        """
        ct = self.session.client('cloudtrail', region_name=region)
        ct.update_trail(Name=trail_name, S3KeyPrefix=self.account.account_name)

        auditlog(
            event='cloudtrail.set_s3_prefix',
            actor=self.ns,
            data={
                'account': self.account.account_name,
                'region': region
            }
        )
        self.log.info(f'Updated S3KeyPrefix to {self.account.account_name} for {self.account.account_name}/{trail_name}')

    def set_s3_bucket(self, *, region, trail_name, bucket_name):
        """Sets the S3 bucket location for logfile delivery

        Args:
            region (`str`): Name of the AWS region
            trail_name (`str`): Name of the CloudTrail Trail
            bucket_name (`str`): Name of the S3 bucket to deliver log files to

        Returns:
            `None`
        """
        ct = self.session.client('cloudtrail', region_name=region)
        ct.update_trail(Name=trail_name, S3BucketName=bucket_name)

        auditlog(
            event='cloudtrail.set_s3_bucket',
            actor=self.ns,
            data={
                'account': self.account.account_name,
                'region': region
            }
        )
        self.log.info(f'Updated S3BucketName to {bucket_name} for {self.account.account_name}/{region}/{trail_name}')
    # endregion
