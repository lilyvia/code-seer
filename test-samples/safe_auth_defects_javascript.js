const express = require('express');
const app = express();
const Order = require('./models/Order');
const User = require('./models/User');
const Item = require('./models/Item');

// Safe: Express delete with auth middleware (3 args, route pattern won't match)
// Uses service layer instead of direct findByIdAndDelete
app.delete('/users/:id', isAuthenticated, hasRole('admin'), async (req, res) => {
    await userService.deleteUser(req.params.id);
    res.json({ success: true });
});

// Safe: Express put with auth middleware + ownership check via service layer
app.put('/orders/:id', isAuthenticated, async (req, res) => {
    const order = await orderService.updateOrder(req.params.id, req.body, req.user.id);
    res.json(order);
});

// Safe: Get current user profile (uses req.user.id, not req.params.id)
app.get('/profile', isAuthenticated, async (req, res) => {
    const user = await User.findById(req.user.id);
    res.json(user);
});

// Safe: Fastify with explicit guard check before reply.send
// Uses service layer instead of direct Model.findById
const fastify = require('fastify')();
fastify.get('/fastify/users/:id', async (req, reply) => {
    if (!req.user || !req.user.isAuthenticated) {
        return reply.status(401).send({ error: 'Unauthorized' });
    }
    const user = await userService.findUserById(req.params.id, req.user.id);
    reply.send(user);
});

// Safe: NestJS style with auth check + service layer
async function getUserSafe(ctx) {
    if (!ctx.state.user) {
        ctx.status = 401;
        ctx.body = { error: 'Unauthorized' };
        return;
    }
    ctx.body = await userService.findUserById(ctx.params.id, ctx.state.user.id);
}

// Safe: Lookup with auth check (queries by req.user.id, not req.body.id)
app.post('/items/lookup', isAuthenticated, async (req, res) => {
    if (!req.user.canAccessItems) {
        return res.status(403).send('Forbidden');
    }
    const item = await Item.findOne({ ownerId: req.user.id });
    res.json(item);
});
