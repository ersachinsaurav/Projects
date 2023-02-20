import React, { useContext, useState } from 'react';
import noteContext from '../context/notes/noteContext';

const AddNote = (props) => {
	const { addNote } = useContext(noteContext);
	const [note, setNote] = useState({
		title: '',
		description: '',
		tag: '',
	});

	const handleAddNote = async () => {
		const response = addNote(note.title, note.description, note.tag);
		let errorMsg = '';
		await response.then((errors) => {
			console.log(errors);
			if (errors) {
				for (let index = 0; index < errors.length; index++) {
					const error = errors[index];
					errorMsg = errorMsg + ' ' + error.msg;
				}
			}
		});

		if (errorMsg) {
			props.handleAlert(errorMsg, 'danger');
		} else {
			setNote({ title: '', description: '', tag: '' });
			props.handleAlert('Note Added Successfully.', 'success');
		}
	};

	const onChange = (e) => {
		setNote({ ...note, [e.target.name]: e.target.value });
	};

	return (
		<div className="my-3" id="addNote">
			<h2 className="mb-3">Add A Note</h2>
			<div className="mb-3">
				<label htmlFor="title" className="form-label">
					Title
				</label>
				<input
					type="text"
					className="form-control"
					id="title"
					name="title"
					placeholder="Title of Note"
					onChange={onChange}
					value={note.title}
				/>
			</div>
			<div className="mb-3">
				<label htmlFor="description" className="form-label">
					Description
				</label>
				<textarea
					className="form-control"
					id="description"
					name="description"
					placeholder="Description of Note"
					rows="3"
					onChange={onChange}
					value={note.description}></textarea>
			</div>
			<div className="mb-3">
				<label htmlFor="tag" className="form-label">
					Tag
				</label>
				<input
					type="text"
					className="form-control"
					id="tag"
					name="tag"
					placeholder="Tag of Note"
					onChange={onChange}
					value={note.tag}
				/>
			</div>
			<div className="mb-3">
				<button
					type="submit"
					className="btn btn-primary mb-3"
					onClick={handleAddNote}
					disabled={note.title.length < 5 || note.description.length < 20}>
					Add Note
				</button>
			</div>
		</div>
	);
};

export default AddNote;
