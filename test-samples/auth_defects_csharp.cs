using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

public class OrdersController : ControllerBase
{
    private readonly AppDbContext _context;

    public OrdersController(AppDbContext context)
    {
        _context = context;
    }

    // Pattern 1: IDOR - Direct Find from parameter
    [HttpGet("users/{id}")]
    public IActionResult GetUser(int id)
    {
        return Ok(_context.Users.Find(id));
    }

    // Pattern 2: Direct return of database query without ownership check (async)
    [HttpGet("orders/{id}")]
    public async Task<IActionResult> GetOrder(int id)
    {
        return Ok(await _context.Orders.FindAsync(id));
    }

    // Pattern 3: Delete with only IsAuthenticated check
    [HttpDelete("users/{id}")]
    public IActionResult DeleteUser(int id)
    {
        var user = _context.Users.Find(id);
        if (User.Identity != null && User.Identity.IsAuthenticated)
        {
            _context.Users.Remove(user);
            _context.SaveChanges();
        }
        return NoContent();
    }

    // Pattern 4: Direct entity return using FirstOrDefault
    [HttpGet("products/{id}")]
    public IActionResult GetProduct(int id)
    {
        return Ok(_context.Products.FirstOrDefault(o => o.Id == id));
    }

    // Additional variant: async FirstOrDefault
    [HttpGet("items/{id}")]
    public async Task<IActionResult> GetItem(int id)
    {
        return Ok(await _context.Items.FirstOrDefaultAsync(o => o.Id == id));
    }
}
