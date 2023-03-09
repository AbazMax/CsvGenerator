from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='schemas'),
    path('creating_schema', views.creating_schema, name='creating_schema'),
    path('editing_schema/<int:pk>', views.editing_schema, name='editing_schema'),
    path('data_req/<int:pk>', views.data_req, name='data_req'),
    path('edit_req', views.edit_req, name='edit_req'),
    path('save_schema', views.save_schema, name='save_schema'),
    path('delete_schema/<int:id>', views.del_schema, name='delete_schema'),
    path('data_sets/<int:pk>', views.data_sets_view, name='data_sets'),
    path('gen_data', views.gen_data, name='gen_data'),
]