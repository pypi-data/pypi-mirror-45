from .panels.csrf_multi_scheme import CSRFMultiSchemeDebugPanel

def includeme(config):
    """
    Pyramid API hook
    """
    config.registry.settings['debugtoolbar.panels'].append(CSRFMultiSchemeDebugPanel)

    if 'mako.directories' not in config.registry.settings:
        config.registry.settings['mako.directories'] = []
