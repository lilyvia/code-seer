function safeFixedFilter(User, req) {
    return User.find({ email: String(req.query.email) });
}

function safeAllowlistedField(User, req) {
    const allowedFields = new Set(['email', 'status']);
    const field = req.query.field;
    if (!allowedFields.has(field)) {
        throw new Error('invalid field');
    }

    return User.find({ [field]: String(req.query.value) });
}

function safeMongoCount(users, req) {
    return users.countDocuments({ status: String(req.query.status) });
}

function safeQueryWithoutOperators(User, req) {
    return User.find({
        name: String(req.query.name || ''),
        status: 'active'
    });
}
