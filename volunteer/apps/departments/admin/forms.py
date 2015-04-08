from betterforms.forms import BetterModelForm

from volunteer.apps.departments.models import (
    Department,
    Role,
)


class AdminDepartmentForm(BetterModelForm):
    class Meta:
        model = Department
        fields = (
            'name',
            'description',
        )


class AdminRoleForm(BetterModelForm):
    class Meta:
        model = Role
        fields = (
            'name',
            'description',
        )
