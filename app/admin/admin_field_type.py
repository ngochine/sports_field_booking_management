from app.admin.admin_base import AdminView


class FieldTypeAdmin(AdminView):
    column_labels = {
        'name': 'Loại sân',
        'description': 'Mô tả'
    }
    column_list = ['name', 'description']
    column_searchable_list = ['name']
