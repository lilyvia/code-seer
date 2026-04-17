// Safe: Verify resource ownership before access
fn safe_check_ownership(order_uid: i32, current_uid: i32) -> Result<(), &'static str> {
    if order_uid != current_uid {
        return Err("Forbidden");
    }
    Ok(())
}

// Safe: Admin middleware pattern
fn safe_require_admin(is_admin: bool) -> Result<(), &'static str> {
    if !is_admin {
        return Err("Admin required");
    }
    Ok(())
}
