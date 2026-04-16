class OrdersController < ApplicationController
  def show
    @order = Order.find(params[:id])
  end

  def edit
    @user = User.find_by_id(params[:id])
  end

  def update
    @post = Post.find_by(params[:post_id])
  end

  def destroy
    @item = Item.where(id: params[:id]).first
  end
end
