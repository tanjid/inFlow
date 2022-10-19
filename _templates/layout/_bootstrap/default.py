from django.conf import settings
from pprint import pprint
from _keenthemes.libs.theme import KTTheme

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in _keenthemes/__init__.py
"""
class KTBootstrapDefault:

    def init(context):
        # Init default layout
        KTBootstrapDefault.initDarkSidebarLayout(context)

        #KTBootstrapDefault.initLightSidebarLayout(context)

        #KTBootstrapDefault.initDarkHeaderLayout(context)

        #KTBootstrapDefault.initLightHeaderLayout(context)

        # Init global assets for default layout
        KTBootstrapDefault.initAssets(context)

        return context

    def initAssets(context):
        # Include global vendors
        KTTheme.addVendors(['datatables', 'fullcalendar'])

        # Include global javascript files
        KTTheme.addJavascriptFile('js/widgets.bundle.js')
        KTTheme.addJavascriptFile('js/custom/apps/chat/chat.js')
        KTTheme.addJavascriptFile('js/custom/utilities/modals/upgrade-plan.js')
        KTTheme.addJavascriptFile('js/custom/utilities/modals/create-app.js')
        KTTheme.addJavascriptFile('js/custom/utilities/modals/users-search.js')
        KTTheme.addJavascriptFile('js/custom/utilities/modals/new-target.js')

        return context

    def initDarkSidebarLayout(context):
        KTTheme.addHtmlAttribute('body', 'data-kt-app-layout', 'dark-sidebar')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-header-fixed', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-fixed', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-hoverable', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-push-header', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-push-toolbar', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-push-footer', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-toolbar-enabled', 'true')

        KTTheme.addHtmlClass('body', 'app-default')

        return context

    def initLightSidebarLayout(context):
        KTTheme.addHtmlAttribute('body', 'data-kt-app-layout', 'light-sidebar')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-header-fixed', 'false')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-fixed', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-hoverable', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-push-header', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-push-toolbar', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-sidebar-push-footer', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-toolbar-enabled', 'true')

        KTTheme.addHtmlClass('body', 'app-default')

        return context

    def initDarkHeaderLayout(context):
        KTTheme.addHtmlAttribute('body', 'data-kt-app-layout', 'dark-header')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-header-fixed', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-toolbar-enabled', 'true')

        KTTheme.addHtmlClass('body', 'app-default')

        return context

    def initLightHeaderLayout(context):
        KTTheme.addHtmlAttribute('body', 'data-kt-app-layout', 'light-header')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-header-fixed', 'true')
        KTTheme.addHtmlAttribute('body', 'data-kt-app-toolbar-enabled', 'true')

        KTTheme.addHtmlClass('body', 'app-default')

        return context