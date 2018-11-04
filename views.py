from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.urls import reverse
from django.views import generic
from django.template import Context, Template, loader, RequestContext
from django.conf import settings
from django.http import Http404
import requests, ast, urllib.request, smtplib, random
from .functions import *
from Katie_Site.models import *
from Katie_Site.forms import *
from .forms import *

# Create your views here.

def index(request):
	template=loader.get_template('./Katie_Site/index.html')
	args={'Title': 'Home',}
	return render(request, './Katie_Site/index.html', args)

def products_page(request):
	if request.method == 'POST':
		if 'product_filter' in request.POST:
			product_filter=ProductFilterForm(request.POST)
			product_filter.is_valid()
			filtered_products=None
			if product_filter.cleaned_data['clothes']== True or product_filter.cleaned_data['dresses']== True or product_filter.cleaned_data['shirts']== True or product_filter.cleaned_data['crafts'] == True:
				if product_filter.cleaned_data['clothes'] == True:
					clothes=products.objects.filter(category__contains="clothes")
					if filtered_products:
						filtered_products=filtered_products | clothes
					else:
						filtered_products=clothes
				if product_filter.cleaned_data['dresses'] == True:
					dresses=products.objects.filter(category__contains="dresses")
					if filtered_products:
						filtered_products=filtered_products | dresses
					else:
						filtered_products=dresses
				if product_filter.cleaned_data['shirts'] == True:
					shirts=products.objects.filter(category__contains="shirts")
					if filtered_products:
						filtered_products=filtered_products | shirts
					else:
						filtered_products=shirts
				if product_filter.cleaned_data['crafts'] == True:
					crafts=products.objects.filter(category__contains="crafts")
					if filtered_products:
						filtered_products=filtered_products | crafts
					else:
						filtered_products=crafts
				form=product_filter
				products_list=''
				for product in filtered_products:
					products_list=products_list+product_adder(product)
				args={'products_list': products_list, 'form': form, 'Title': 'Products', 'product_matches': filtered_products}
				template=loader.get_template('./Katie_Site/products_page.html')
				return render(request, './Katie_Site/products_page.html', args)
			else:
				all_products=products.objects.all()
				products_list=''
				for product in all_products:
					products_list=products_list+product_adder(product)
				form=ProductFilterForm()
				args={'form': form, 'products_list': products_list, 'Title': 'Products', 'product_matches': all_products}
				template=loader.get_template('./Katie_Site/products_page.html')
				return render(request, './Katie_Site/products_page.html', args)
		
	else:
		all_products=products.objects.all()
		products_list=''
		for product in all_products:
			products_list=products_list+product_adder(product)
		form=ProductFilterForm()
		args={'form': form, 'products_list': products_list, 'Title': 'Products', 'product_matches': all_products}
		template=loader.get_template('./Katie_Site/products_page.html')
		return render(request, './Katie_Site/products_page.html', args)

def collections(request, collection_name):
#need to put in a 'if request.method=post' here for the filter

	#Uses the collection name in order to filter by category and display products in that category
	collection_list=products.objects.filter(category__contains=collection_name)
	product_filter=ProductFilterForm(request.POST)
	form=product_filter
	products_list=''
	for product in collection_list:
		products_list=products_list+product_adder(product)
	args={'products_list': products_list, 'form': form, 'Title': 'Products', 'product_matches': collection_list}
	template=loader.get_template('./Katie_Site/products_page.html')
	return render(request, './Katie_Site/products_page.html', args)

def individual_product_page(request, product_name):
	revised_product_name=''
	#Translates the URL to the initial product name
	for char in product_name:
		if char=="-":
			revised_product_name=revised_product_name+' '
		else:
			revised_product_name=revised_product_name+char
	try:
		products.objects.filter(name=revised_product_name).exists()
	except:
		raise Http404
	product=products.objects.get(name=revised_product_name)
	#URL used to get user back from paypal
	return_url='http://127.0.0.1:8000/products/'+product_name
	template=loader.get_template('./Katie_Site/individual_product_page.html')
	args={'product':product,'picture_url':product.picture_url, 'name':revised_product_name, 'price':product.price, 'return_url': return_url, 'Title': revised_product_name, 'paypal_button': product.paypal_button}
	return render(request, './Katie_Site/individual_product_page.html', args)

def product_search(request):
	product_query=request.GET.get('query')
	category_search=products.objects.filter(category__contains=product_query)
	name_search=products.objects.filter(name__contains=product_query)
	description_search=products.objects.filter(description__contains=product_query)
	product_matches=category_search | name_search | description_search
	products_list=''
	for product in product_matches:
		products_list=products_list+product_adder(product)
	print(products_list)
	if products_list=='':
		print('product list empty')
		products_list="<p>I'm sorry, we weren't able to find any products that matched that description. If you think we should, though, please let us know!</p>"
	args={'products_list': products_list, 'Title': 'Search Results for '+product_query, 'product_matches': product_matches}
	template=loader.get_template('./Katie_Site/product_search.html')
	return render(request, './Katie_Site/product_search.html', args)

def contact(request):
	template=loader.get_template('./Katie_Site/contact.html')
	args={'Title': 'Contact Us',}
	return render(request, './Katie_Site/contact.html', args)

def about(request):
	template=loader.get_template('./Katie_Site/about.html')
	args={'Title': 'About Us',}
	return render(request, './Katie_Site/about.html', args)

def product_adder(product):
	return '<div class="products-outerdiv"><li class="products-li"><div class="products-innerdiv"><a class="product-link" id="product-link" href=/NKRawsonCreations/products/'+product.name+'><img src="'+product.picture_url+'" class="product-image">'+'<p class="product-list-text">'+product.name+'</p><p class="product-list-text">Price: $'+str(product.price)+'</p></a></div></li></div>'