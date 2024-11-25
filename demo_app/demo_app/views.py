from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView, View
from django.urls import reverse, reverse_lazy

from demo_app import conduit_api


class AuthMixin:
    COOKIE_NAME = 'auth_token'

    login_url = reverse_lazy('signin')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        request.auth_token = request.COOKIES.get(self.COOKIE_NAME, None)

    def dispatch(self, request, *args, **kwargs):
        if not request.auth_token:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class IndexView(AuthMixin, RedirectView):
    pattern_name = 'workspaces'


class SigninView(TemplateView):
    template_name = 'views/signin.html'

    def get_context_data(self, **kwargs):
        return {
            'page_title': 'Signin',
        }

    def post(self, request, *args, **kwargs):
        token = request.POST.get('token', '').strip()

        response = redirect('workspaces')
        response.set_cookie(AuthMixin.COOKIE_NAME, token)

        return response


class SignoutView(View):
    def get(self, request, *args, **kwargs):
        response = redirect('signin')
        response.delete_cookie(AuthMixin.COOKIE_NAME)

        return response


class WorkspacesView(AuthMixin, TemplateView):
    template_name = 'views/workspaces.html'

    def get_context_data(self, **kwargs):
        workspaces = conduit_api.workspaces_list(self.request.auth_token)

        return {
            'page_title': 'Workspaces',
            'workspaces': workspaces,
        }


class WorkspaceCreateView(AuthMixin, TemplateView):
    template_name = 'views/workspace_create.html'

    def get_context_data(self, **kwargs):
        return {
            'page_title': 'Create Workspace',
            'nav_back': reverse('workspaces'),
        }

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        ext_id = request.POST['ext_id']

        conduit_api.workspaces_create(
            request.auth_token,
            name,
            ext_id,
        )

        return redirect('workspaces')


class DashboardsView(AuthMixin, TemplateView):
    template_name = 'views/dashboards.html'

    def get_context_data(self, workspace_id, workspace_token, **kwargs):
        org_dashboards = conduit_api.dashboards_list(self.request.auth_token)
        workspace_dashboards = conduit_api.dashboards_list(workspace_token)

        return {
            'page_title': 'Dashboards',
            'nav_back': reverse('workspaces'),
            'workspace_id': workspace_id,
            'workspace_token': workspace_token,
            'org_dashboards': org_dashboards,
            'workspace_dashboards': workspace_dashboards,
        }


class DashboardCloneView(AuthMixin, View):

    def post(self, request, workspace_id, workspace_token, dashboard_id, *args, **kwargs):
        conduit_api.dashboards_clone(request.auth_token, dashboard_id, workspace_id)

        return redirect('dashboards', workspace_id, workspace_token)


class DashboardView(AuthMixin, TemplateView):
    template_name = 'views/dashboard-view.html'

    def get_context_data(self, workspace_id, workspace_token, dashboard_id, **kwargs):
        data = conduit_api.dashboards_get_url(workspace_token, dashboard_id)

        return {
            'page_title': 'Dashboard',
            'nav_back': reverse('dashboards', args=[workspace_id, workspace_token]),
            'dashboard_url': data['url'],
        }