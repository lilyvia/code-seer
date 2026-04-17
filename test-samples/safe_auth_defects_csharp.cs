using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;

[ApiController]
[Route("api")]
public class SafeAuthController : ControllerBase
{
    [Authorize(Roles = "Admin")]
    [HttpDelete("users/{id}")]
    public IActionResult DeleteUser(int id)
    {
        _service.DeleteUser(id);
        return NoContent();
    }

    [Authorize]
    [HttpGet("orders/{id}")]
    public IActionResult GetOrder(int id)
    {
        var order = _context.Orders.Find(id);
        if (order == null || order.UserId != User.Identity!.Name)
        {
            return Forbid();
        }
        return Ok(order);
    }
}
