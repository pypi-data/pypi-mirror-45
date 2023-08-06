# coding=utf-8
# import
from pythoncommontools.objectUtil.POPO import POPO
# workspace
class Workspace(POPO):
    # constructors
    @staticmethod
    def constructFromAttributes(id,comments=''):
        # initialize workspace
        workspace = Workspace()
        # add attributs
        workspace.id=id
        workspace.comments=comments
        # return
        return workspace
    pass
