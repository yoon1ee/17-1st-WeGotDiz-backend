import json
import re
import datetime

from django.http                       import JsonResponse, HttpResponse
from django.views                      import View

from user.models                       import User
from product.models                    import Product, LikeUser, Reward
from purchase.models                   import RewardOrder, Order

from .utils                            import login_decorator
from my_settings                       import SECRET_KEY, ALGORITHM

# funding view, like_view

class UserLikeView(View):
    @login_decorator
    def get(self, request):
        if not User.objects.filter(id=request.user.id):
            return JsonResponse({"message" : "INVALID_USER"})
        
        user = User.objects.get(id=request.user.id)

        user_info = [
            {
                "id"            : user.id,
                "userName"      : user.fullname
            }
        ]
        
        likes = LikeUser.objects.filter(user=request.user.id)
        
        like_list = [{
            "product_id"            : like.product.id,
            "product_title"         : like.product.title,
            "product_image"         : like.product.thumbnail_url,
            "product_maker_info"    : like.product.maker_info.name,
            "product_total_amount"  : like.product.total_amount,  
            "product_achieved_rate" : like.product.achieved_rate, 
            "product_category"      : [category.name for category in like.product.category_set.all()]

        } for like in likes]
        
        return JsonResponse({"data" : {'user_info' : user_info, 'like_list' : like_list}}, status=200)

class UserFundView(View):
    @login_decorator
    def get(self, request):
        if not User.objects.filter(id=request.user.id):
            return JsonResponse({"message" : "INVALID_USER"})
        
        user = User.objects.get(id=request.user.id)

        user_info = [
            {
                "id"            : user.id,
                "userName"      : user.fullname
            }
        ]
        
        funding_list = [
            
            {
                "product_image"          : reward.product.thumbnail_url,
                "product_date_countdown" : str((datetime.datetime.today() - reward.product.closing_date).days),
                "product_total_amount"   : reward.product.total_amount,
                "product_achieved_rate"  : reward.product.achieved_rate,
                "product_title"          : reward.product.title,
                "product_maker_info"     : reward.product.maker_info.name,
                "product_category"       : [category.name for category in reward.product.category_set.all()]
            }
            for order in user.order_set.all()
            for reward in order.reward.all()]

        return JsonResponse({"data" : {'user_info' : user_info, 'funding_list' : funding_list}}, status=200)

class UserInfoView(View):
    @login_decorator  
    def get(self, request, product_id): 
        user  = request.user
        user_info = {
            'email' : user.email,
            'name' : user.fullname
        }
        return JsonResponse({'user_info' : user_info}, status=200)