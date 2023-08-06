# local
from .panels import SqlalchemyCsvDebugPanel


__VERSION__ = '0.2.1'


# ==============================================================================


def includeme(config):
    """
    an earlier version used things like this
        altconfig = config.with_package('pyramid_debugtoolbar')
        altconfig.add_route('debugtoolbar_api_sqlalchemy.sqlalchemy_csv', '/_debug_toolbar-api/{request_id}/sqlalchemy.csv')
        altconfig.scan('pyramid_debugtoolbar_api_sqlalchemy.views')
        altconfig.commit()
    now we are included within the debugtoolbar , so are under it's prefix (note the routing below)
    this keeps our routes from appearing in the debugtoolbar
    """
    config.add_debugtoolbar_panel(SqlalchemyCsvDebugPanel)
    config.add_route('debugtoolbar.api_sqlalchemy.queries.csv', '/api-sqlalchemy/sqlalchemy-{request_id}.csv')
    config.scan('pyramid_debugtoolbar_api_sqlalchemy.views')
    config.commit()


# ==============================================================================
