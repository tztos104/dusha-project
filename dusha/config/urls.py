from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from board import views
from board.views import CustomPasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls), #관리자 페이지
    path('', views.index), #인덱스
    path('board/', include('board.urls')), #게시판
    path('item/', include('item.urls')),  # 제품페이지
    path('cart/', include('cart.urls')), #장바구니
    path('coupon/', include('coupon.urls')), #장바구니
    path('', include('common.urls')),#allauth  로
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('', include('allauth.urls')),



]

# 이미지 추가
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)