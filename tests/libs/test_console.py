from akeru.models import AWSRole, AccessRole
from akeru.libs.console import generate_session
from django.contrib.auth.models import User, Group
from django.test import TestCase
from unittest.mock import patch, MagicMock


class AccessTests(TestCase):

    # Role | Direct
    @patch('akeru.libs.console.get_user_session')
    @patch('akeru.libs.console.get_role_session')
    def test_role_direct_gets_role_session(self, mock_role, mock_user):
        user = User(username='abc')
        user.save()
        role = AWSRole(name='xx', policy='xx', user=False)
        role.save()
        access = AccessRole(user=user, role=role)
        access.save()
        generate_session(user, False, 'xx')
        self.assertTrue(mock_role.called)
        self.assertTrue(not mock_user.called)

    # User | Direct
    @patch('akeru.libs.console.get_user_session')
    @patch('akeru.libs.console.get_role_session')
    @patch('boto3.client')
    def test_user_direct_gets_user_session(self, mock_boto, mock_role_sess,
                                           mock_user_sess):
        mock_iam = MagicMock()
        mock_iam.create_access_key.return_value = {
            'AccessKey': {'AccessKeyId': '', 'SecretAccessKey': ''}
        }
        mock_boto.return_value = mock_iam

        user = User(username='abc')
        user.save()
        role = AWSRole(name='xx', policy='xx', user=True)
        role.save()
        access = AccessRole(user=user, role=role)
        access.save()
        generate_session(user, True, 'xx')
        self.assertTrue(not mock_role_sess.called)
        self.assertTrue(mock_user_sess.called)

    # Role | Group
    @patch('akeru.libs.console.get_user_session')
    @patch('akeru.libs.console.get_role_session')
    def test_role_group_gets_role_session(self, mock_role_sess,
                                          mock_user_sess):
        user = User(username='abc')
        user.save()
        group = Group(name='testg')
        group.save()
        group.user_set.add(user)
        role = AWSRole(name='xx', policy='xx', user=False)
        role.save()
        access = AccessRole(group=group, role=role)
        access.save()
        generate_session(user, False, 'xx')
        self.assertTrue(mock_role_sess.called)
        self.assertTrue(not mock_user_sess.called)

    # User | Group
    @patch('akeru.libs.console.get_user_session')
    @patch('akeru.libs.console.get_role_session')
    @patch('boto3.client')
    def test_user_group_gets_role_session(self, mock_boto,
                                          mock_role_sess, mock_user_sess):
        mock_iam = MagicMock()
        mock_iam.create_access_key.return_value = {
            'AccessKey': {'AccessKeyId': '', 'SecretAccessKey': ''}
        }
        mock_boto.return_value = mock_iam

        user = User(username='abc')
        user.save()
        group = Group(name='testg')
        group.save()
        group.user_set.add(user)
        role = AWSRole(name='xx', policy='xx', user=True)
        role.save()
        access = AccessRole(group=group, role=role)
        access.save()
        generate_session(user, True, 'xx')
        self.assertTrue(not mock_role_sess.called)
        self.assertTrue(mock_user_sess.called)
