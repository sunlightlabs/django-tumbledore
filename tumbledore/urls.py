from django.conf.urls.defaults import *

urlpatterns = patterns('tumbledore.views',
    url(r'^tumblelog/widget/(?P<widget_id>[\d]+).js$', 'widget', name='tumble_widget'),
    url(r'^(?P<mount_point>[\d\w\/_\-]*)/post/(?P<slug>[\w\d_\-]+)/$', 'post', name='tumble_post'),
    url(r'^(?P<mount_point>[\d\w\/_\-]*)/$', 'index', name='tumble_index'),
)
