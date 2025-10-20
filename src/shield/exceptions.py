__all__ = ("ShieldPermissionDenied",)

class ShieldPermissionDenied(Exception):
    def __init__(self, permission: str):
        super().__init__()
        self.permission: str = permission
