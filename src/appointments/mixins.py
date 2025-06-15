from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class ProtectedViewMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active:
            return redirect('/users/login/?next=%s' % request.path)
        return super().dispatch(request, *args, **kwargs)


class SaveProfileMixin:
    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class ProtectedObjectMixin:
    def dispatch(self, request, *args, **kwargs):
        profile_id = None
        if hasattr(self.get_object(), 'profile_id'):
            profile_id = self.get_object().profile_id
        else:
            profile_id = self.get_object().client.profile_id
        if profile_id != self.request.user.profile.pk:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
