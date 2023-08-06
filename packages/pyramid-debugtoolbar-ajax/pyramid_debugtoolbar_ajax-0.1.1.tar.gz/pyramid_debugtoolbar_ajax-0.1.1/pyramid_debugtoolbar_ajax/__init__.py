from .panels.ajax import AjaxDebugPanel


__VERSION__ = '0.1.1'


def includeme(config):
    config.registry.settings['debugtoolbar.extra_panels'].append(AjaxDebugPanel)
    if 'mako.directories' not in config.registry.settings:
        config.registry.settings['mako.directories'] = []
