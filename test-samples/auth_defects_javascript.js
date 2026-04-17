const express = require('express');
const app = express();
const Order = require('./models/Order');
const User = require('./models/User');
const Item = require('./models/Item');

// Pattern 1: IDOR - Direct database lookup from request params
app.get('/orders/:id', async (req, res) => {
    const order = await Order.findById(req.params.id);
    res.json(order);
});

// Pattern 2: Direct findOne from user input
app.post('/items/lookup', async (req, res) => {
    const item = await Item.findOne({ _id: req.body.id });
    res.json(item);
});

// Pattern 3: Direct findById lookup without auth check
app.get('/users/:id', async (req, res) => {
    const user = await User.findById(req.params.id);
    res.json(user);
});

// Pattern 4: Direct model query and return
app.get('/orders/direct/:id', async (req, res) => {
    res.json(await Order.findById(req.params.id));
});

// Pattern 5: Delete without ownership check
app.delete('/users/:id', async (req, res) => {
    await User.findByIdAndDelete(req.params.id);
    res.json({ success: true });
});

// Pattern 6: Update without ownership check
app.put('/orders/:id', async (req, res) => {
    const order = await Order.findByIdAndUpdate(req.params.id, req.body);
    res.json(order);
});

// Safe pattern: with ownership check
app.get('/orders/safe/:id', async (req, res) => {
    const order = await Order.findById(req.params.id);
    if (order.userId !== req.user.id) {
        return res.status(403).send('Forbidden');
    }
    res.json(order);
});

// Pattern 7: Express delete without guard middleware
app.delete('/items/:id', async (req, res) => {
    await Item.findByIdAndDelete(req.params.id);
    res.json({ deleted: true });
});

// Pattern 8: Express put without guard middleware
app.put('/users/:id', async (req, res) => {
    const user = await User.findByIdAndUpdate(req.params.id, req.body);
    res.json(user);
});

// Pattern 9: Fastify direct resource exposure
const fastify = require('fastify')();
fastify.get('/fastify/users/:id', async (req, reply) => {
    reply.send(await User.findById(req.params.id));
});

// Pattern 10: NestJS style ctx.body direct resource exposure
async function getUser(ctx) {
    ctx.body = await User.findById(ctx.params.id);
}
