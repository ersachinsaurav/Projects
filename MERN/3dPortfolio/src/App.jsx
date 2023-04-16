import { BrowserRouter } from 'react-router-dom';
import {
	About,
	Contact,
	Experience,
	Feedbacks,
	Hero,
	Navbar,
	Tech,
	Works,
	StarsCanvas,
} from './components';
import { CCSizeState } from './contexts';

const App = () => {
	return (
		<CCSizeState>
			<BrowserRouter>
				<div className="relative z-0 bg-primary">
					<div className="bg-hero-pattern bg-cover bg-no-repeat bg-center">
						<Navbar />
						<Hero />
					</div>
					<About />
					<Experience />
					<Tech />
					<Works />
					<Feedbacks />
					<div className="relative z-0">
						<Contact />
						<StarsCanvas />
					</div>
				</div>
			</BrowserRouter>
		</CCSizeState>
	);
};

export default App;
