import { Client } from "https://deno.land/x/postgres@v0.17.2/mod.ts";
import * as bcrypt from "https://deno.land/x/bcrypt@v0.4.1/mod.ts";

const user = prompt("Enter the username: ");
const password = prompt("Enter the password: ");

if (!user || !password) {
  console.error("Username and password are required");
  Deno.exit(1);
}

const client = new Client({
  user,
  password,
  database: "Cirmax",
  hostname: "localhost",
  port: 3306,
});
await client.connect();

const users = await client.queryArray("SELECT * FROM users");

if (users.rowCount === 0) {
  console.error("No users found...\nPopulating the database with one user...");
  const dbUsername = prompt("Enter the username for the database: ");
  const dbPassword = prompt("Enter the password for the database: ");
  if (!dbUsername || !dbPassword) {
    console.error("Username and password are required");
    Deno.exit(1);
  }
  const hashedPassword = await bcrypt.hash(dbPassword);
  await client
    .queryArray`INSERT INTO users (code, name, password) VALUES (${dbUsername}, ${dbUsername}, ${hashedPassword})`;
} else {
  console.error("Users found in the database...");
}
