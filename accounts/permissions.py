from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user.is_seller)
        # if request.user.is_seller == 0:
        #     return False
        
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_seller
        )

class IsSelleOfTheProduct(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print(request.user.is_seller)
        # if request.user.is_seller == 0:
        #     return False
        
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj.seller == request.user 
        )


class IsOwnerOfTheAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj == request.user 
        )