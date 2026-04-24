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

// Pattern 11: Express POST create without auth
app.post('/orders', async (req, res) => {
    const order = await Order.create(req.body);
    res.json(order);
});

// Pattern 12: Express PUT with updateOne without auth
app.put('/items/:id', async (req, res) => {
    await Item.updateOne({ _id: req.params.id }, req.body);
    res.json({ updated: true });
});

// Pattern 13: Express DELETE with deleteOne without auth
app.delete('/orders/:id', async (req, res) => {
    await Order.deleteOne({ _id: req.params.id });
    res.json({ deleted: true });
});

// Pattern 14: Fastify POST create without auth
fastify.post('/fastify/orders', async (req, reply) => {
    const order = await Order.create(req.body);
    reply.send(order);
});

// Pattern 15: Fastify PUT update without auth
fastify.put('/fastify/orders/:id', async (req, reply) => {
    const order = await Order.findByIdAndUpdate(req.params.id, req.body);
    reply.send(order);
});

// Pattern 16: Fastify DELETE without auth
fastify.delete('/fastify/users/:id', async (req, reply) => {
    await User.findByIdAndDelete(req.params.id);
    reply.send({ deleted: true });
});

// Pattern 17: NestJS Controller direct resource exposure
class UserController {
    @Get(':id')
    async getUser(@Param() params): Promise<User> {
        return await this.userService.findById(params.id);
    }

    @Post()
    async createUser(@Body() body): Promise<User> {
        return await this.userService.create(body);
    }

    @Put(':id')
    async updateUser(@Param('id') id: string): Promise<User> {
        return await this.userService.findByIdAndUpdate(id, req.body);
    }
}

// Pattern 18: Router instance patterns
const router = express.Router();
router.get('/users/:id', async (req, res) => {
    const user = await User.findById(req.params.id);
    res.json(user);
});
router.post('/items', async (req, res) => {
    const item = await Item.create(req.body);
    res.json(item);
});
router.put('/orders/:id', async (req, res) => {
    const order = await Order.findByIdAndUpdate(req.params.id, req.body);
    res.json(order);
});
router.delete('/users/:id', async (req, res) => {
    await User.findByIdAndDelete(req.params.id);
    res.json({ deleted: true });
});

// Pattern 19: Generic async handler function
async function deleteUserHandler(req, res) {
    await User.findByIdAndDelete(req.params.id);
    res.json({ success: true });
}

// Pattern 20: Prisma direct resource exposure
app.get('/prisma/users/:id', async (req, res) => {
    const user = await prisma.user.findUnique({ where: { id: req.params.id } });
    res.json(user);
});

app.put('/prisma/users/:id', async (req, res) => {
    const user = await prisma.user.update({ where: { id: req.params.id }, data: req.body });
    res.json(user);
});

app.delete('/prisma/users/:id', async (req, res) => {
    await prisma.user.delete({ where: { id: req.params.id } });
    res.json({ deleted: true });
});

app.post('/prisma/orders', async (req, res) => {
    const order = await prisma.order.create({ data: req.body });
    res.json(order);
});

// Pattern 21: findOneAndDelete without auth
app.delete('/items/soft/:id', async (req, res) => {
    await Item.findOneAndDelete({ _id: req.params.id });
    res.json({ deleted: true });
});

// Pattern 22: Direct send of findOne result
app.get('/items/lookup/:id', async (req, res) => {
    res.send(await Item.findOne({ _id: req.params.id }));
});

// Pattern 23: NestJS direct repository access
class OrderController {
    @Get(':id')
    async getOrder(@Param('id') id: string) {
        return await this.orderRepo.findOne({ where: { id } });
    }
}

// Pattern 24: Prisma findFirst direct exposure
app.get('/prisma/orders/:id', async (req, res) => {
    const order = await prisma.order.findFirst({ where: { id: req.params.id } });
    res.json(order);
});

function false_negative_expansion_auth_js(app, router, User, req, res) {
    app.patch('/users/:id', async (req, res) => res.json(await User.findByIdAndUpdate(req.params.id, req.body)));
    router.patch('/users/:id', async (req, res) => res.json(await User.findOne({ _id: req.params.id })));
}

export const config = { matcher: ["/:path*"] };

definePageMeta({
    layout: 'admin'
});
