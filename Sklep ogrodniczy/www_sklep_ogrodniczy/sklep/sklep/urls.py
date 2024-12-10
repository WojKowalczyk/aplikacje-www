from django.urls import path
from .views import (
    UserRegisterView, CustomLoginView, CustomLogoutView, IndexView,
    PersonListView, PersonDetailView, PersonAddView, PersonUpdateView, PersonDeleteView,
    PositionListView, PositionDetailView, PositionAddView, PositionUpdateView, PositionDeleteView,
    ProductListView, ProductDetailView, ProductAddView, ProductUpdateView, ProductDeleteView,
    CartListView, CartDetailView, CartDetailTemplateView,
    CartItemListView, CartItemDetailView, CartItemDeleteView,
    AddToCartView, RemoveFromCartView,
    ProductsByInitialView, ProductsPublishedAfterView, ProductsSearchView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # person CRUD
    path('persons/', PersonListView.as_view(), name='person-list'),
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('persons/add/', PersonAddView.as_view(), name='person-add'),
    path('persons/<int:pk>/update/', PersonUpdateView.as_view(), name='person-update'),
    path('persons/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),
    # position CRUD
    path('positions/', PositionListView.as_view(), name='position-list'),
    path('positions/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
    path('positions/add/', PositionAddView.as_view(), name='position-add'),
    path('positions/<int:pk>/update/', PositionUpdateView.as_view(), name='position-update'),
    path('positions/<int:pk>/delete/', PositionDeleteView.as_view(), name='position-delete'),
    # product CRUD
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/add/', ProductAddView.as_view(), name='product-add'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    # carts CRUD
    path('carts/', CartListView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('carts/<int:cart_id>/items/', CartItemListView.as_view(), name='cart-item-list'),
    path('carts/<int:cart_id>/items/<int:item_id>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('carts/<int:cart_id>/detail/', CartDetailTemplateView.as_view(), name='cart-detail-page'),
    path('carts/<int:cart_id>/items/<int:item_id>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),

    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove_from_cart/<int:cart_id>/<int:item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    # advanced CRUDs
    path('products/initial/<str:letter>/', ProductsByInitialView.as_view(), name='products-by-initial'),
    path('products/after/<str:date_str>/', ProductsPublishedAfterView.as_view(), name='products-after'),
    path('products/search/<str:substring>/', ProductsSearchView.as_view(), name='products-search'),
]
