import React, { useState } from 'react';

const InputToDo = () => {
	const [description, setDescription] = useState('');

	const handleDesciption = (event) => {
		event.preventDefault();
		setDescription(event.target.value);
	};

	const handleSubmit = async (event) => {
		event.preventDefault();
		try {
			const body = { description };
			const response = await fetch('http://127.0.0.1:5000/todos', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(body),
			});
			window.location = '/';
		} catch (error) {
			console.log(error.message);
		}
	};

	return (
		<>
			<h1 className="text-center mt-5">ToDo List</h1>

			<form className="d-flex mt-5" onSubmit={handleSubmit}>
				<input
					type="text"
					className="form-control"
					name="description"
					placeholder="Description"
					value={description}
					onChange={handleDesciption}
				/>
				<button
					type="submit"
					className="btn btn-primary"
					style={{ marginLeft: '10px' }}>
					Add
				</button>
			</form>
		</>
	);
};

export default InputToDo;
