#!/usr/bin/python
import boto.ec2


class Connection:
    def __init__(self):
        ''' Connection Instance '''
        self.region = 'us-west-2'
        self.key_id = 'AKIAJ4NPEM7LESTMM5TQ'
        self.access_key = 'Q2u63EHJXinn8y29DKs/OTmgxfj9H0z/yPbt6fBS'

    def ec2Connection(self):
        ''' Create and return an EC2 Connection '''
        conn = boto.ec2.connect_to_region(self.region,self.key_id,self.access_key)
        return conn


class EC2Instance(Connection):
    def create_instance(self):
        self.conn.run_instances(
            'ami-f87c9080',
            key_name='devops',
            instance_type='t2.small',
            security_groups=['launch-wizard-1'])
        print 'Creating Instance'


connInt = EC2Instance()

connInt.create_instance()

