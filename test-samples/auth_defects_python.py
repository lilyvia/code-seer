def view_order_django(request):
    order = Order.objects.get(id=request.GET.get('order_id'))
    return render(request, 'order.html', {'order': order})

def view_order_flask():
    order = Order.query.get(request.args.get('id'))
    return jsonify(order.to_dict())

def get_user_django(request):
    user = User.objects.get(id=request.POST.get('user_id'))
    return JsonResponse({'user': user.username})

def get_item_django(request):
    obj = Item.objects.get(pk=request.GET.get('item_id'))
    return render(request, 'item.html', {'item': obj})

def get_item_flask():
    obj = db.session.query(Item).get(request.args.get('item_id'))
    return jsonify(obj.to_dict())

@login_required
def delete_user_django(request, user_id):
    User.objects.filter(id=user_id).delete()
    return JsonResponse({'status': 'deleted'})

@login_required
def delete_user_flask(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return jsonify({'status': 'deleted'})

def get_profile_django(request):
    profile = Profile.objects.filter(user_id=request.GET.get('uid')).first()
    return render(request, 'profile.html', {'profile': profile})

def get_profile_flask():
    profile = Profile.query.filter_by(user_id=request.args.get('uid')).first()
    return jsonify(profile.to_dict())
