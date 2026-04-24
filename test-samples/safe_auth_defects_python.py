from flask_login import login_required, current_user
from flask import abort
from django.contrib.auth.decorators import login_required as django_login_required


# Safe: Flask with proper authorization
@login_required
def admin_panel():
    if not current_user.is_admin:
        abort(403)
    return "Admin panel"


# Safe: Django with permission check
@django_login_required
def user_dashboard(request):
    return render(request, "dashboard.html")


# Safe: Explicit ownership check
def view_order(order_id, current_user_id):
    order = Order.objects.get(id=order_id)
    if order.user_id != current_user_id:
        raise PermissionDenied("Not your order")
    return order


@app.api_route("/admin/users/{id}", methods=["DELETE"], dependencies=[Depends(get_current_user)])
def safe_delete_admin_user(id: int, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise PermissionDenied("Admin required")
    User.objects.filter(id=id).delete()
    return {"status": "deleted"}
