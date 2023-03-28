console.clear();

const express = require('express');
const app = express();
const cors = require('cors');
const pool = require('./db');

//Middleware
app.use(cors());
app.use(express.json());

// ROUTES

// Create a ToDo
app.post('/todos', async (req, res) => {
	try {
		const { description } = req.body;
		const newToDo = await pool.query(
			'INSERT INTO todos (description) values ($1) RETURNING *',
			[description]
		);
		res.json(newToDo.rows[0]);
	} catch (error) {
		console.log(error.message);
	}
});

// Fetch all ToDos
app.get('/todos', async (req, res) => {
	try {
		const ToDos = await pool.query('SELECT * FROM todos');
		res.json(ToDos.rows);
	} catch (error) {
		console.log(error.message);
	}
});

// Fetch a ToDo
app.get('/todos/:id', async (req, res) => {
	try {
		const { id } = req.params;
		const ToDo = await pool.query(`SELECT * FROM todos WHERE todo_id = $1`, [
			id,
		]);
		res.json(ToDo.rows);
	} catch (error) {
		console.log(error.message);
	}
});

// Update a ToDo
app.put('/todos/:id', async (req, res) => {
	try {
		const { id } = req.params;
		const { description } = req.body;
		const ToDo = await pool.query(
			`UPDATE todos SET description = $1 WHERE todo_id = $2 RETURNING *`,
			[description, id]
		);
		res.json('ToDo Updated Successfully!');
	} catch (error) {
		console.log(error.message);
	}
});

// Delete a todo
app.delete('/todos/:id', async (req, res) => {
	try {
		const { id } = req.params;
		const ToDo = await pool.query(`DELETE FROM todos WHERE todo_id = $1`, [id]);
		res.json('ToDo Deleted Successfully!');
	} catch (error) {
		console.log(error.message);
	}
});

app.listen(5000, () => {
	console.log('Running @ http://127.0.0.1:5000');
});
