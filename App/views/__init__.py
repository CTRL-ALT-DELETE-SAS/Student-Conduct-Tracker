# blue prints are imported
# explicitly instead of using *
from .user import *
from .index import *
from .review import *
from .karma import *
from .staff import *

views = [user_views, index_views, review_views, karma_views, staff_views]
# blueprints must be added to this list
