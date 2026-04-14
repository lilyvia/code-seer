<?php

// Pattern 1: IDOR - findOrFail with request input
$order = Order::findOrFail($request->input('order_id'));

// Pattern 2: Direct model query from request
$user = User::findOrFail($request->input('user_id'));
$item = Item::find($request->get('id'));

// Pattern 3: Delete with only Auth::check()
if (Auth::check()) {
    User::where('id', $id)->delete();
}

// Pattern 4: Direct where query from request
$record = Model::where('id', $request->input('id'))->first();

// Additional vulnerable patterns
$post = Post::findOrFail($request->input('post_id'));
$comment = Comment::find($request->get('comment_id'));
$setting = Setting::where('key', $request->input('key'))->first();

if (Auth::check()) {
    Order::where('id', $orderId)->forceDelete();
}

// Safe patterns (should NOT match)
$admin = Admin::where('role', 'admin')->first();
$static = User::find(1);
