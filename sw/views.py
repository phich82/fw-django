from django.views import generic

from sw.commons.helpers import _, __, t, trans

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    print('trans => ', trans('common.test'), trans('test'), trans('common.common'))
    print(_('Add New %(action)s') % {'action': 'CRUD'})
    print('__ => ', __('test'), t('test', 'ja'), t('sub', 'ja', {'error': 'danger'}))
