import importlib

import tools.login as LoginModule
from tools.login import Login

import tools.tasking as TaskingModule
from tools.tasking import Tasking


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Ursa Platform Toolbox"
        self.alias = "UrsaPlatformToolbox"

        # trigger reload for hmr development
        importlib.reload(LoginModule)
        importlib.reload(TaskingModule)

        # List of tool classes associated with this toolbox
        self.tools = [Login, Tasking]
