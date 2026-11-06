from rest_framework.permissions import BasePermission,SAFE_METHODS
class StaffWriteOrReadOnly(BasePermission):
 def has_permission(self,request,view): return request.method in SAFE_METHODS or bool(request.user and request.user.is_staff)
class IsOrderOwnerOrStaff(BasePermission):
 def has_object_permission(self,request,view,obj): return request.user.is_staff or obj.customer_id==request.user.id
