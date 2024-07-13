from django.contrib import admin
from backend.models.user import CompanyUser
from backend.models.ads import *

# Register your models here.

admin.site.register(CompanyUser)
admin.site.register(Location)
admin.site.register(AdCampaign)
admin.site.register(Ads)
admin.site.register(CampaignType)
admin.site.register(TargetAudience)