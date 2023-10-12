# blue prints are imported
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .review import review_views
from .karma import karma_views
from .staff import staff_views

views = [user_views, index_views, review_views, karma_views, staff_views]
# blueprints must be added to this list
