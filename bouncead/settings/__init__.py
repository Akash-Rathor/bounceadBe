from .base import *
import os


# if os.environ['APP_ENV'] == 'prod':
#    from .prod import *

# elif os.environ['APP_ENV'] == 'pre-prod':
#     from .uat import *

# elif os.environ['APP_ENV'] == 'pre-uat':
# 	from .pre_uat import *

# else:
from .dev import *

REDIS_LOCATION = os.getenv("REDIS_LOCATION")

# if CACHE_ENABLE:
# 	CACHES = {
# 		"default": {
# 			"BACKEND": "django_redis.cache.RedisCache",
# 			"LOCATION": REDIS_LOCATION,
# 			"OPTIONS": {
# 				'REDIS_CLIENT_CLASS': 'rediscluster.RedisCluster',
# 				'CONNECTION_POOL_CLASS': 'rediscluster.connection.ClusterConnectionPool',
# 				'CONNECTION_POOL_KWARGS': {
# 					'skip_full_coverage_check': True
# 				}
# 			},
# 			"KEY_PREFIX": REDIS_KEY_PREFIX
# 		}
# 	}
# 	CACHE_TTL = None
# CACHE_TTL = 24*60*60 #1 day
