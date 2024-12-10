from rest_framework.permissions import BasePermission

# 1 - user who is not logged in
# 2 - user who is logged in, but not in worker group
# 3 - user who is logged in, and is part of the worker group
# 4 - user who is logged in, and is part of the admin group
class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            group_level = 1
        elif user.is_superuser or user.groups.filter(name__iexact='admin').exists():
            group_level = 4
        elif user.groups.filter(name__iexact='worker').exists():
            group_level = 3
        else:
            group_level = 2

        url_name = request.resolver_match.url_name

        if url_name in ['index', 'user-register', 'login', 'logout']:
            return True

        if url_name in ['person-list', 'person-detail', 'person-add', 'person-update', 'person-delete']:
            return group_level == 4

        if url_name in ['position-list', 'position-detail', 'position-add', 'position-update', 'position-delete']:
            return group_level == 4

        if url_name in ['product-list', 'product-detail', 'product-add', 'product-update', 'product-delete']:
            return group_level in [3,4]

        if url_name in ['cart-list', 'cart-detail', 'cart-item-list', 'cart-item-detail', 'cart-detail-page', 'cart-item-delete', 'add-to-cart', 'remove-from-cart']:
            return group_level in [2,3,4]

        # Advanced product views - only group 4
        if url_name in ['products-by-initial', 'products-after', 'products-search']:
            return group_level == 4

        return False




