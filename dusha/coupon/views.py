from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.utils import timezone
from django.views.decorators.http import require_POST

from coupon.forms import AddCouponForm
from coupon.models import Coupon
#쿠폰 추가
@login_required(login_url='/member/login/')
def add_coupon(request):
    now = timezone.now()
    form = AddCouponForm(request.POST)


    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, use_from__lte=now, use_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist as e:
            request.session['coupon_id'] = None
    return redirect('cart:detail')

# 맴버쉽 설정
@login_required(login_url='/login/')
def grade(request):
    my_profile = Profile.objects.all()
    orders = Order.objects.filter(user_id=request.user)
    total = sum([order.total_price for order in orders])
    if total > 1000000:
        my_profile.user_grade = 'mvp'
        my_profile.coupon = '30%'
    elif total > 500000:
        my_profile.user_grade = 'platinum'
        my_profile.coupon = '20%'
    else:
        my_profile.user_grade = 'normal'
        my_profile.coupon = '10%'
    context = {
        'total': total,
        'my_profile': my_profile
    }
    return render(request, 'member/profile-rate.html', context)
