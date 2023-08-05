from PyDictionary import core


core.print = lambda x: None
# # patching PyDictionary to use lxml and be silent


__all__ = ['core']
