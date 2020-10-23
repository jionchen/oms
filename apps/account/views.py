from django.core.exceptions import ValidationError
from .serializers import RoleSerializer, SubuserSerializer, AccountSerializer, BookkeepingSerializer
from .paginations import BookkeepingPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import RolePermission, SubuserPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, exceptions
from utils.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Sum
from apps.user.models import User
from .models import Account
import pendulum
from .serializers import AccountUpdateSerializer
from .paginations import AccountPagination
from utils.excel import export_excel, import_excel
from rest_framework.decorators import action
from rest_framework.status import HTTP_201_CREATED
from django.db import transaction
from .serializers import UserSerializer
from .paginations import UserPagination


class RoleViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, RolePermission]

    def get_queryset(self):
        return self.request.user.teams.roles.all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)


class SubusertViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = SubuserSerializer
    permission_classes = [IsAuthenticated, SubuserPermission]

    def get_queryset(self):
        return self.request.user.teams.users.filter(is_boss=False).order_by('create_date')

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        username = self.request.data.get('username')
        roles = self.request.data.get('roles', [])

        if password is None:
            raise exceptions.ValidationError

        if User.objects.filter(username=username).first():
            raise exceptions.ValidationError({'message': '账号已存在'})

        serializer.save(teams=self.request.user.teams, is_boss=False, password=password, roles=roles)

    def perform_update(self, serializer):
        username = self.request.data.get('username')
        roles = self.request.data.get('roles', [])

        if serializer.instance.username != username and User.objects.filter(username=username).first():
            raise exceptions.ValidationError({'message': '账号已存在'})

        serializer.instance.roles.set(roles)
        serializer.save()

    def partial_update(self, request, *args, **kwargs):  # 重置密码
        password = self.request.data.get('password')
        if password is None:
            raise exceptions.ValidationError

        instance = self.get_object()
        instance.set_password(password)
        instance.save()
        return Response(status=status.HTTP_200_OK)


class AccountViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = AccountSerializer
    pagination_class = AccountPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['is_active']
    search_fields = ['number', 'name', 'account', 'holder', 'remark']
    ordering_fields = ['number', 'name']
    ordering = ['number']
    field_mapping = (('number', '编号'), ('name', '名称'), ('account', '账号'), ('holder', '银行账户'),
                     ('type', '类型'), ('remark', '备注'), ('is_active', '状态'))

    def get_serializer_class(self):
        return AccountUpdateSerializer if self.request.method == 'PUT' else self.serializer_class

    def get_queryset(self):
        return self.request.user.teams.accounts.all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)

    @action(detail=False)
    def export_excel(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return export_excel(serializer.data, '账户列表', self.field_mapping)

    @action(detail=False)
    @transaction.atomic
    def import_excel(self, request, *args, **kwargs):
        Account.objects.bulk_create([Account(**item, teams=request.user.teams)
                                     for item in import_excel(self, self.field_mapping)])
        return Response(status=HTTP_201_CREATED)


class SellerViewSet(viewsets.ModelViewSet):
    """list"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = request.user.teams.users.all()
        roles = request.user.roles.all()
        if not roles:  # 没有设置角色默认拥有全部权限
            return Response(queryset.values_list('username', flat=True))

        for role in roles:
            if 'CHANGE_SELLER' in role.permissions:
                return Response(queryset.values_list('username', flat=True))

        return Response([request.user.username])


class BookkeepingViewSet(viewsets.ModelViewSet):
    """list, create, destroy"""
    serializer_class = BookkeepingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookkeepingPagination

    def get_queryset(self):
        return self.request.user.teams.bookkeeping_set.all().order_by('-create_datetime')

    def perform_create(self, serializer):
        teams = self.request.user.teams
        account_id = self.request.data.get('account')
        account = Account.objects.filter(teams=teams, id=account_id).first()
        if not account:
            raise ValidationError({'message': '账户不存在'})

        recorder = self.request.user
        serializer.save(teams=teams, account_name=account.name, recorder=recorder, recorder_name=recorder.name)


class StatisticalAccountViewSet(viewsets.ModelViewSet):
    """list"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        accoutns = self.request.query_params.get('accounts')
        accoutns = accoutns.split(',') if accoutns else []
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        end_date = pendulum.parse(end_date).add(days=1)

        bookkeeping_queryset = self.request.user.teams.bookkeeping_set.filter(
            account_id__in=accoutns)
        purchase_queryset = self.request.user.teams.purchase_order_set.filter(
            account_id__in=accoutns, is_undo=False)
        sales_queryset = self.request.user.teams.sales_order_set.filter(
            account_id__in=accoutns, is_undo=False)

        if start_date:
            bookkeeping_queryset = bookkeeping_queryset.filter(create_datetime__gte=start_date)
            purchase_queryset = purchase_queryset.filter(date__gte=start_date)
            sales_queryset = sales_queryset.filter(date__gte=start_date)

        if end_date:
            bookkeeping_queryset = bookkeeping_queryset.filter(create_datetime__lte=end_date)
            purchase_queryset = purchase_queryset.filter(date__lte=end_date)
            sales_queryset = sales_queryset.filter(date__lte=end_date)

        return bookkeeping_queryset, purchase_queryset, sales_queryset

    def list(self, request, *args, **kwargs):
        bookkeeping_queryset, purchase_queryset, sales_queryset = self.get_queryset()

        amount_list = bookkeeping_queryset.values_list('amount', flat=True)
        expenditure = purchase_queryset.aggregate(amount=Sum('amount')).get('amount', 0)
        revenue = sales_queryset.aggregate(amount=Sum('amount_received') - Sum('change_amount')).get('amount', 0)

        for amount in amount_list:
            if amount > 0:
                revenue += amount
            else:
                expenditure -= amount

        return Response({'revenue': revenue, 'expenditure': expenditure})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'name']
    ordering_fields = ['username']
    ordering = ['username']

    def get_queryset(self):
        return self.request.user.teams.users.all()
