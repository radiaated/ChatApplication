from sqladmin import Admin
from admin.views import UserAdmin, RoomAdmin, MessageAdmin

from db.session import engine


def setup_admin(app):
    """Configure and register admin views."""
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(MessageAdmin)
