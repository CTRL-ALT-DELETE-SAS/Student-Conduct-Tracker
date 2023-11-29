# blue prints are imported
# explicitly instead of using *
from .admin import *
from .index import *
from .review import *
from .staff import *
from .auth import *

views = [admin_views, index_views, review_views, staff_views, auth_views]
# blueprints must be added to this list
