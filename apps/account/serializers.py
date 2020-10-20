from rest_framework.exceptions import PermissionDenied
from .models import Role, Account, Bookkeeping
from rest_framework import serializers
from sales.models import Client
from user.models import User
import re


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'remark', 'permissions']
        read_only_fields = ['id']

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError
        return data


class SubuserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    role_names = serializers.SerializerMethodField('get_role_names')

    class Meta:
        model = User
        fields = ['name', 'phone', 'username', 'create_date', 'roles', 'role_names']
        read_only_fields = ['create_date', 'roles', 'role_names']

    def validate(self, data):
        if not data.get('username') or not data.get('name') or not data.get('phone'):
            raise serializers.ValidationError

        if not re.match(r'^1[3456789]\d{9}$', data['phone']):
            raise serializers.ValidationError

        roles = self.context['request'].data.get('roles', [])
        if roles:
            exist_roles = self.context['request'].user.teams.roles.all().values_list('id', flat=True)
            if not set(roles).issubset(exist_roles):
                raise serializers.ValidationError

        return data

    def get_role_names(self, obj):
        return obj.roles.all().values_list('name', flat=True)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        read_only_fields = ['id']
        fields = ['number', 'name', 'account', 'holder', 'type', 'remark', 'is_active',
                  *read_only_fields]

    def validate(self, data):
        # 编号验证
        teams = self.context['request'].user.teams
        if Account.objects.filter(teams=teams, number=data['number']).exists():
            raise serializers.ValidationError({'number': '编号已存在'})
        return data


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        read_only_fields = ['id', 'number']
        fields = ['name', 'account', 'holder', 'type', 'remark', 'is_active', *read_only_fields]


class BookkeepingSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField('get_account_name')

    class Meta:
        model = Bookkeeping
        fields = ['id', 'create_datetime', 'account', 'account_name', 'amount',
                  'recorder', 'remark']
        read_only_fields = ['id', 'create_datetime', 'account_name', 'recorder']

    def validate(self, data):
        if not data.get('account') or data.get('amount') is None:
            raise serializers.ValidationError

        teams = self.context['request'].user.teams
        if data['account'].teams != teams:
            raise serializers.ValidationError

        return data

    def get_account_name(self, obj):
        return obj.account.name
