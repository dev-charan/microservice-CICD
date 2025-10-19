const express = require("express");
const amqp = require("amqplib");
const app = express();
const port = 3000;

app.use(express.json());

let todos = [];

async function publishToQueue(message) {
  try {
    const connection = await amqp.connect(
      process.env.RABBITMQ_URL || "amqp://guest:guest@localhost:5672/"
    );
    const channel = await connection.createChannel();
    const queue = "todo_notifications";
    await channel.assertQueue(queue, { durable: false });
    channel.sendToQueue(queue, Buffer.from(JSON.stringify(message)));
    console.log("Sent to queue:", message);
    await channel.close();
    await connection.close();
  } catch (err) {
    console.error("Failed to publish to RabbitMQ:", err);
  }
}

app.post("/todos", async (req, res) => {
  const { text } = req.body;
  if (!text) return res.status(400).send("Text is required");
  const todo = { id: todos.length + 1, text };
  todos.push(todo);

  await publishToQueue({ message: `New todo: ${text}` });
  res.status(201).json(todo);
});

app.get("/todos", (req, res) => {
  res.json(todos);
});

app.listen(port, () => {
  console.log(`API service running on http://localhost:${port}`);
});
