import itertools

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from cart.forms import AddItemForm
from item.forms import ItemForm
from item.models import Category, Item



# Create your views here.


#남녀 베스트 리스트
def index(request):
    #각 카테고리에서 판매량 1순위인 상품 리스트에 추가


    category = Category.objects.order_by('id').all()
    count = range(1, len(category)+1)
    best3 = Item.objects.filter(gender__isnull=True)

    for n in count:
        best = Item.objects.filter(gender='MEN', item_category=n).order_by('-sales')[:1]
        best2 = Item.objects.filter(gender='WOMEN', item_category=n).order_by('-sales')[:1]
        best3 = itertools.chain(best, best2, best3)
    best_list = []  # 빈 리스트
    best_list = best3
    context= {'best_list': best_list}
    return render( request, 'item/index_item.html',  context )

#상품 등록
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.Files) #일반속성, 파일
        if form.is_valid(): #폼이 유효하다면
            item =form.save(commit=False) #가저장
            item.author = request.user
            item.create_date = timezone.now()
            item.save() #db에 저장
            return redirect('item:item_list')
    else:
        form = ItemForm()
    context = {'form': form}
    return render(request, 'item/item_form.html', context)

#상품 목록

def item_list(request):
    page = request.GET.get('page', 1) #페이징 처리
    kw = request.GET.get('kw', '') #검색어 가져오기
    item_list = Item.objects.order_by('-create_date') #작성일 내림차수

    if kw:
        item_list = item_list.filter(
            Q(item_title__icontains=kw) | #제목검색
            Q(content__icontains=kw)  # 내용검색

        ).distinct()
    paginator = Paginator(item_list, 10) #페이지당 10개씩 설정
    page_obj = paginator.get_page(page) #페이지 가져오기


    context = {'item_list': page_obj , 'page':page, 'kw':kw}
    return render(request, 'item/item_list.html', context)

# 카테고리 페이지
def category_page(request, slug):
    current_category = Category.objects.get(slug=slug)
    item_list = Item.objects.filter(category=current_category) #현재 카테고리의 포스트
    item_list = item_list.order_by('-pub_date')  #날짜순 내림 차순
    categories = Category.objects.all()

    context = {
        'current_category': current_category,
        'item_list': item_list,
        'categories': categories
    }
    return render(request, 'item/item_list.html', context)

def item_detail(request, id):

    # 제품 상세
    #item = Item.objects.get(id=item_id) #해당 id의 질문
    #item = Item.objects.get(id=item_id)
    item = get_object_or_404(Item, pk=id)
    # 경로에 오류가 있을 때 404로 처리(페이지가 없음)
    add_to_cart = AddItemForm(initial={'quantity': 1})
    context = {'item': item, 'add_to_cart': add_to_cart}
    return render(request, 'item/item_detail.html', context)
