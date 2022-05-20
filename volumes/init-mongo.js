
print('Start #################################################################');

db = db.getSiblingDB("testDB");

db.createUser({
    user: 'test_user',
    pwd: 'test',
    roles: [
        {
            role: 'readWrite',
            db: 'testDB',
        },
    ],
});


db.createCollection('goods', { capped: false });