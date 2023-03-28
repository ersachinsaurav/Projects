import './App.css';
import InputToDo from './components/InputToDo';
import ListTodos from './components/ListTodos';

function App() {
	return (
		<>
			<div className="container">
				<InputToDo />
				<ListTodos />
			</div>
		</>
	);
}

export default App;
