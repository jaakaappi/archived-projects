import pg from "pg";
import express from "express";
import cors from "cors";
import morgan from "morgan";
import randanimal from "randanimal";
import { createSession, getSession } from "./src/databaseService.js";

const { Pool } = pg;
const { randanimalSync } = randanimal;
const app = express();

const pool = new Pool(
  process.env.DATABASE_URL
    ? {
        connectionString: process.env.DATABASE_URL,
        ssl: {
          rejectUnauthorized: false,
        },
      }
    : {
        connectionString:
          "postgresql://postgres:example@localhost:5432/postgres",
      }
);
const port = process.env.PORT || 3001;

app.use(cors());
app.use(morgan("dev"));

app.post("/", async (req, res) => {
  const id = randanimalSync().split(" ").join("-");
  try {
    await createSession(pool, id);
    res.json({ sessionId: id });
  } catch (error) {
    console.error(error);
    res.sendStatus(500);
  }
});

app.get("/:id", async (req, res) => {
  if (req.params.id) {
    try {
      const session = await getSession(pool, req.params.id);
      if (session) {
        res.send(session);
      } else {
        res.sendStatus(404);
      }
    } catch (error) {
      console.error(error);
      res.sendStatus(500);
    }
  } else {
    return sendStatus(403);
  }
});

app.listen(port, () => {
  console.log(`Server running`);
});
