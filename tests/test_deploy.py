import json
from akeru.app_settings import \
    DEFAULT_TRUST_POLICY, EC2_TRUST_POLICY, LAMBDA_TRUST_POLICY
from akeru.deploy import get_trust_policy
from akeru.models import AWSRole
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase


class DeploymentTests(TestCase):

    def test_returns_default_trust(self):
        expected_trust = \
            DEFAULT_TRUST_POLICY.replace(
                "<custom_trusted_users>",
                json.dumps(settings.DEFAULT_TRUSTED_USERS)
            )
        role = AWSRole(name='xx', policy='xx')
        trust = get_trust_policy(role)
        self.assertTrue(trust == expected_trust)

    def test_returns_ec2_trust(self):
        expected_trust = EC2_TRUST_POLICY
        role = AWSRole(name='xx', policy='xx', ec2=True)
        trust = get_trust_policy(role)
        self.assertTrue(trust == expected_trust)

    def test_returns_lambda_trust(self):
        expected_trust = LAMBDA_TRUST_POLICY
        role = AWSRole(name='xx', policy='xx', aws_lambda=True)
        trust = get_trust_policy(role)
        self.assertTrue(trust == expected_trust)

    def test_returns_custom_trust(self):
        expected_trust = 'sdfdsf'
        role = AWSRole(name='xx', policy='xx', trust=expected_trust)
        trust = get_trust_policy(role)
        self.assertTrue(trust == expected_trust)


class ModelTests(TestCase):
    def test_cant_have_two_service_types(self):
        with self.assertRaises(ValidationError):
            role = AWSRole(name='xx', policy='xx', ec2=True, aws_lambda=True)
            role.clean()
