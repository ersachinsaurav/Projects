import React, { useState } from 'react';

const EditTodo = ({ todo }) => {
	const [description, setDescription] = useState(todo.description);

	const updateDescription = async (e) => {
		e.preventDefault();
		try {
			const body = { description };
			const response = await fetch(
				`http://127.0.0.1:5000/todos/${todo.todo_id}`,
				{
					method: 'PUT',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify(body),
				}
			);
			window.location = '/';
		} catch (error) {
			console.log(error.message);
		}
	};

	return (
		<>
			<button
				type="button"
				className="btn btn-warning"
				data-bs-toggle="modal"
				data-bs-target={`#id${todo.todo_id}`}>
				Edit
			</button>

			<div
				className="modal fade"
				id={`id${todo.todo_id}`}
				data-bs-backdrop="static"
				data-bs-keyboard="false"
				tabIndex="-1"
				aria-labelledby="editModalLabel"
				aria-hidden="true">
				<div className="modal-dialog">
					<div className="modal-content">
						<div className="modal-header">
							<h1 className="modal-title fs-5" id="editModalLabel">
								Edit ToDo
							</h1>
							<button
								type="button"
								className="btn-close"
								data-bs-dismiss="modal"
								onClick={() => setDescription(todo.description)}
								aria-label="Close"></button>
						</div>
						<div className="modal-body">
							<input
								type="text"
								className="form-control"
								value={description}
								onChange={(e) => setDescription(e.target.value)}
							/>
						</div>
						<div className="modal-footer">
							<button
								type="button"
								className="btn btn-secondary"
								onClick={() => setDescription(todo.description)}
								data-bs-dismiss="modal">
								Cancel
							</button>
							<button
								type="button"
								className="btn btn-primary"
								data-bs-dismiss="modal"
								onClick={(e) => updateDescription(e)}>
								Update
							</button>
						</div>
					</div>
				</div>
			</div>
		</>
	);
};

export default EditTodo;
