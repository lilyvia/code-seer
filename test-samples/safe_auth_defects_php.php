<?php

// Safe: Check ownership before returning data
function showOrder($orderId, $currentUserId) {
    $order = Order::findOrFail($orderId);
    if ($order->user_id !== $currentUserId) {
        abort(403, 'Not your order');
    }
    return response()->json($order);
}

// Safe: Admin routes with middleware
Route::middleware(['auth', 'can:admin'])->group([AdminController::class, 'routes']);

Route::middleware('auth')->delete('/admin/users/{id}', [AdminController::class, 'deleteUser']);
