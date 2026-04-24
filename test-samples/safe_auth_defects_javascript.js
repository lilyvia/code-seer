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

// Safe: Express POST with auth middleware
app.post('/orders', isAuthenticated, hasRole('admin'), async (req, res) => {
    const order = await orderService.createOrder(req.body, req.user.id);
    res.json(order);
});

// Safe: Express PUT with auth middleware + ownership check inline
app.put('/orders/:id', isAuthenticated, async (req, res) => {
    const order = await orderService.findOrderById(req.params.id);
    if (order.userId.toString() !== req.user.id) {
        return res.status(403).send('Forbidden');
    }
    const updated = await orderService.updateOrder(req.params.id, req.body);
    res.json(updated);
});

// Safe: Express DELETE with auth middleware + ownership check inline
app.delete('/items/:id', isAuthenticated, async (req, res) => {
    const item = await itemService.findItemById(req.params.id);
    if (!item || item.ownerId !== req.user.id) {
        return res.status(403).send('Forbidden');
    }
    await itemService.deleteItem(req.params.id);
    res.json({ deleted: true });
});

// Safe: Fastify POST with auth check
fastify.post('/fastify/orders', async (req, reply) => {
    if (!req.user) {
        return reply.status(401).send({ error: 'Unauthorized' });
    }
    const order = await orderService.createOrder(req.body, req.user.id);
    reply.send(order);
});

// Safe: Fastify PUT with auth check
fastify.put('/fastify/orders/:id', async (req, reply) => {
    if (!req.user) {
        return reply.status(401).send({ error: 'Unauthorized' });
    }
    const order = await orderService.updateOrder(req.params.id, req.body, req.user.id);
    reply.send(order);
});

// Safe: Fastify DELETE with auth check
fastify.delete('/fastify/users/:id', async (req, reply) => {
    if (!req.user || !req.user.isAdmin) {
        return reply.status(403).send({ error: 'Forbidden' });
    }
    await userService.deleteUser(req.params.id);
    reply.send({ deleted: true });
});

// Safe: NestJS Controller with @UseGuards
@Controller('users')
@UseGuards(JwtAuthGuard)
class UserControllerSafe {
    @Get(':id')
    async getUser(@Param() params): Promise<User> {
        return await this.userService.findById(params.id, req.user.id);
    }

    @Post()
    async createUser(@Body() body, @Req() req): Promise<User> {
        return await this.userService.create(body, req.user.id);
    }

    @Put(':id')
    @UseGuards(RolesGuard)
    async updateUser(@Param('id') id: string, @Body() body, @Req() req): Promise<User> {
        return await this.userService.update(id, body, req.user.id);
    }
}

// Safe: Router instance with auth middleware
const router = express.Router();
router.get('/users/:id', isAuthenticated, async (req, res) => {
    const user = await userService.findUserById(req.params.id, req.user.id);
    res.json(user);
});
router.post('/items', isAuthenticated, hasRole('admin'), async (req, res) => {
    const item = await itemService.createItem(req.body, req.user.id);
    res.json(item);
});
router.put('/orders/:id', isAuthenticated, async (req, res) => {
    const order = await orderService.updateOrder(req.params.id, req.body, req.user.id);
    res.json(order);
});
router.delete('/users/:id', isAuthenticated, hasRole('admin'), async (req, res) => {
    await userService.deleteUser(req.params.id);
    res.json({ deleted: true });
});

// Safe: Generic async handler with auth check
async function deleteUserSafe(req, res) {
    if (!req.user || !req.user.isAdmin) {
        return res.status(403).send('Forbidden');
    }
    await userService.deleteUser(req.params.id);
    res.json({ success: true });
}

// Safe: Prisma with auth middleware + ownership check
app.get('/prisma/users/:id', isAuthenticated, async (req, res) => {
    const user = await prismaUserService.findById(req.params.id, req.user.id);
    if (!user) {
        return res.status(403).send('Forbidden');
    }
    res.json(user);
});

app.put('/prisma/users/:id', isAuthenticated, async (req, res) => {
    if (req.params.id !== req.user.id) {
        return res.status(403).send('Forbidden');
    }
    const user = await prismaUserService.update(req.params.id, req.body);
    res.json(user);
});

app.delete('/prisma/users/:id', isAuthenticated, hasRole('admin'), async (req, res) => {
    await prismaUserService.deleteUser(req.params.id);
    res.json({ deleted: true });
});

app.post('/prisma/orders', isAuthenticated, async (req, res) => {
    const order = await prismaOrderService.create({ ...req.body, userId: req.user.id });
    res.json(order);
});

// Safe: findOneAndDelete with ownership check
app.delete('/items/soft/:id', isAuthenticated, async (req, res) => {
    const item = await itemService.findItemById(req.params.id);
    if (!item || item.ownerId !== req.user.id) {
        return res.status(403).send('Forbidden');
    }
    await itemService.findOneAndDelete({ _id: req.params.id });
    res.json({ deleted: true });
});

// Safe: NestJS direct repository access but with @UseGuards
class OrderControllerSafe {
    @Get(':id')
    @UseGuards(JwtAuthGuard)
    async getOrder(@Param('id') id: string, @Req() req) {
        return await this.orderService.findOne({ where: { id, userId: req.user.id } });
    }
}

// Safe: Public endpoint that doesn't access sensitive resources
app.get('/health', async (req, res) => {
    res.json({ status: 'ok' });
});

// Safe: Static file serving
app.get('/public/*', express.static('public'));

export const safeConfig = { matcher: ["/admin/:path*"] };

definePageMeta({
    middleware: ['auth'],
    layout: 'admin'
});
