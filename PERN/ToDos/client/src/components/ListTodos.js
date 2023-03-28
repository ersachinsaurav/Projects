import React, { useState, useEffect } from 'react';
import EditTodo from './EditTodo';

const ListTodos = () => {
	const [todos, setTodos] = useState([]);

	const getTodos = async () => {
		try {
			const response = await fetch('http://127.0.0.1:5000/todos');
			const jsonData = await response.json();
			setTodos(jsonData);
		} catch (error) {
			console.log(error.message);
		}
	};

	useEffect(() => {
		getTodos();
	}, []);

	const handleDelete = async (id) => {
		try {
			const response = await fetch(`http://127.0.0.1:5000/todos/${id}`, {
				method: 'DELETE',
			});
			setTodos(todos.filter((todo) => todo.todo_id !== id));
		} catch (error) {
			console.log(error.message);
		}
	};
	return (
		<>
			<table className="table table-hover mt-5">
				<thead>
					<tr>
						<th scope="col">Description</th>
						<th scope="col">Edit</th>
						<th scope="col">Delete</th>
					</tr>
				</thead>
				<tbody>
					{todos.map((todo) => (
						<tr key={todo.todo_id}>
							<td>{todo.description}</td>
							<td>
								<EditTodo todo={todo} />
							</td>
							<td>
								<button
									className="btn btn-danger"
									onClick={() => handleDelete(todo.todo_id)}>
									Delete
								</button>
							</td>
						</tr>
					))}
				</tbody>
			</table>
		</>
	);
};

export default ListTodos;
