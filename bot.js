exports.handler = async function(event, context) {
  const body = JSON.parse(event.body);

  // التعامل مع الرسالة الواردة
  console.log(body);

  return {
    statusCode: 200,
    body: JSON.stringify({ message: "Webhook received!" }),
  };
};
