from datetime import datetime

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, DetailView, View
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from .models import Position, Person, Product, Cart, CartItem
from .serializers import (
    UserRegistrationModelSerializer,
    PositionModelSerializer,
    PersonModelSerializer,
    ProductModelSerializer,
    CartModelSerializer,
    CartItemModelSerializer
)
from .permissions import CustomPermission

class UserRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationModelSerializer
    def perform_create(self, serializer):
        user = serializer.save()
        Cart.objects.create(user=user)

class CustomLoginView(LoginView):
    template_name = 'sklep/login_register.html'
    def get_success_url(self):
        return '/'

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class IndexView(TemplateView):
    template_name = "sklep/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            context['cart'] = cart
            context['user'] = self.request.user
        return context


class PersonListView(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class PersonDetailView(RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class PersonAddView(CreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)

class PersonUpdateView(UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class PersonDeleteView(DestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]


class PositionListView(ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class PositionDetailView(RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class PositionAddView(CreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class PositionUpdateView(UpdateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class PositionDeleteView(DestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class ProductAddView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]


class CartListView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({"detail":"User must be authenticated"},status=status.HTTP_400_BAD_REQUEST)
        if Cart.objects.filter(user=self.request.user).exists():
            return Response({"detail":"User already has a cart."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)

class CartDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    def update(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            cart = self.get_object()
            cart.user = user
            cart.save()
        return super().update(request, *args, **kwargs)

class CartDetailTemplateView(DetailView):
    model = Cart
    template_name = "sklep/cart_detail.html"
    pk_url_kwarg = 'cart_id'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.object
        items = cart.items.all()
        for i in items:
            i.line_total = i.quantity * i.product.price
        context['cart'] = cart
        context['items'] = items
        return context

class CartItemListView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    serializer_class = CartItemModelSerializer
    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        cart = get_object_or_404(Cart, pk=cart_id)
        return CartItem.objects.filter(cart=cart)
    def perform_create(self, serializer):
        cart_id = self.kwargs['cart_id']
        cart = get_object_or_404(Cart, pk=cart_id)
        serializer.save(cart=cart)

class CartItemDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    serializer_class = CartItemModelSerializer
    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        cart = get_object_or_404(Cart, pk=cart_id)
        return CartItem.objects.filter(cart=cart)

class CartItemDeleteView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    def post(self, request, cart_id, item_id):
        if not request.user.is_authenticated:
            return Response({"detail":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        cart = get_object_or_404(Cart, pk=cart_id, user=request.user)
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddToCartView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

    # We'll handle POST now, as adding to cart is a state-changing action
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return Response({"detail":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=product_id)
        item, created_item = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created_item:
            item.quantity += 1
            item.save()
        return redirect('index')


class RemoveFromCartView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]

    def post(self, request, cart_id, item_id):
        if not request.user.is_authenticated:
            return Response({"detail":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        cart = get_object_or_404(Cart, pk=cart_id, user=request.user)
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        item.delete()
        return redirect('cart-detail-page', cart_id=cart.id)


class ProductsByInitialView(ListAPIView):
    serializer_class = ProductModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    def get_queryset(self):
        letter = self.kwargs['letter']
        return Product.objects.filter(product_text__istartswith=letter)


class ProductsPublishedAfterView(ListAPIView):
    serializer_class = ProductModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    def get_queryset(self):
        date_str = self.kwargs['date_str']
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return Product.objects.none()
        return Product.objects.filter(publication_date__gt=date)


class ProductsSearchView(ListAPIView):
    serializer_class = ProductModelSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomPermission]
    def get_queryset(self):
        substring = self.kwargs['substring']
        return Product.objects.filter(product_text__icontains=substring)
