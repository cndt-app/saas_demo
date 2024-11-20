from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('workspaces/', views.WorkspacesView.as_view(), name='workspaces'),
    path('workspaces/create/', views.WorkspaceCreateView.as_view(), name='workspaces-create'),
    path('dashboards/<int:workspace_id>/<str:workspace_token>/', views.DashboardsView.as_view(), name='dashboards'),
    path('dashboards/<int:workspace_id>/<str:workspace_token>/clone/<int:dashboard_id>/', views.DashboardCloneView.as_view(), name='dashboards-clone'),
    path('dashboards/<int:workspace_id>/<str:workspace_token>/<int:dashboard_id>/', views.DashboardView.as_view(), name='dashboard-view'),
]
