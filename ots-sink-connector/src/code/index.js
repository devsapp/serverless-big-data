const{ Long, Config, Client, TableStore, Condition, RowExistenceExpectation } = require("tablestore")

var client;

exports.initializer = (context, callback) => {
  client = new Client({
    accessKeyId: context.credentials.accessKeyId,
    accessKeySecret: context.credentials.accessKeySecret,
    endpoint: process.env.endpoint,
    instancename: process.env.instance_name,
    securityToken: context.credentials.securityToken
  });
  callback(null, "success")
};

exports.handler = (event, context, callback) => {
    const eventObj = JSON.parse(event);
    console.log(eventObj);
    const params = {
      tableName: process.env.table_name,
      condition: new Condition(RowExistenceExpectation.IGNORE),
      primaryKey: [{ 'pk1': eventObj.pk1 }, { 'pk2': eventObj.pk2 }],
      attributeColumns: [
        { 'col1': eventObj.col1 },
        { 'col2': eventObj.col2 }
      ]
    };

    client.putRow(params, function (err, data) {
      if (err) {
        console.log(err);
        callback(null, 'failed');
        return;
      }
      callback(null, 'success');
    });
}