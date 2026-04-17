# Safe: Require authentication and ownership check
class OrdersController < ApplicationController
  before_action :authenticate_user!

  def show
    order_id = params[:id].to_i
    @order = Order.find(order_id)
    unless @order.user_id == current_user.id
      render status: :forbidden, json: { error: 'Not your order' }
      return
    end
    render json: @order
  end
end

# Safe: Admin actions with role check
class AdminController < ApplicationController
  before_action :require_admin

  def delete_user
    user_id = params[:id].to_i
    User.find(user_id).destroy
    head :no_content
  end

  private

  def require_admin
    render status: :forbidden unless current_user.admin?
  end
end
