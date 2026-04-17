function vulnerableMongoWhere(users, userExpression) {
    return users.find({ $where: userExpression });
}

function vulnerableMongooseWhere(User, req) {
    return User.findOne({ $where: req.query.expression });
}

function vulnerableDynamicFilter(User, req) {
    const filter = {};
    filter[req.query.field] = req.query.value;
    return User.find(filter);
}
