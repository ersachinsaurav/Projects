import {
	pern,
	mern,
	lamp,
	backend,
	creator,
	web,
	javascript,
	typescript,
	html,
	css,
	reactjs,
	redux,
	nodejs,
	git,
	savisoft,
	entrata,
	sauraviCafe,
	blogera,
	cloudBook,
	newsBilla,
	nodeChat,
	weatherBot,
	php,
	nextjs,
	expressjs,
	postgres,
	mysql,
	sachin,
	raj,
	chris,
} from '../assets';

export const navLinks = [
	{
		id: 'about',
		title: 'About',
	},
	{
		id: 'work',
		title: 'Work',
	},
	{
		id: 'contact',
		title: 'Contact',
	},
];

const services = [
	{
		title: 'PERN Stack Developer',
		icon: pern,
	},
	{
		title: 'MERN Stack Developer',
		icon: mern,
	},
	{
		title: 'LAMP Stack Developer',
		icon: lamp,
	},
	{
		title: 'Backend Developer',
		icon: backend,
	},
	{
		title: 'WebApp Developer',
		icon: web,
	},
	{
		title: 'Content Creator',
		icon: creator,
	},
];

const technologies = [
	{
		name: 'HTML 5',
		icon: html,
	},
	{
		name: 'CSS 3',
		icon: css,
	},
	{
		name: 'JavaScript',
		icon: javascript,
	},
	{
		name: 'TypeScript',
		icon: typescript,
	},
	{
		name: 'PHP',
		icon: php,
	},
	{
		name: 'Node JS',
		icon: nodejs,
	},
	{
		name: 'React JS',
		icon: reactjs,
	},
	{
		name: 'Next JS',
		icon: nextjs,
	},
	{
		name: 'Redux Toolkit',
		icon: redux,
	},
	{
		name: 'Express.js',
		icon: expressjs,
	},
	{
		name: 'PostgresSQL',
		icon: postgres,
	},
	{
		name: 'MySQL',
		icon: mysql,
	},
	{
		name: 'GIT',
		icon: git,
	},
];

const experiences = [
	{
		title: 'Trainee',
		company_name: 'SaviSoft Private Limited',
		icon: savisoft,
		iconBg: '#E6DEDD',
		date: 'March 2019 - June 2019',
		points: [
			'Exploring technologies and developing application modules and components from specifications.',
			'Crafting and optimizing business processes and workflows, and documenting them appropriately.',
			'Collaborating with development and testing teams to conduct UI and functional testing of web application implementations.',
		],
	},
	{
		title: 'Associate Software Engineer',
		company_name: 'SaviSoft Private Limited',
		icon: savisoft,
		iconBg: '#383E56',
		date: 'June 2019 - October 2021',
		points: [
			'Creating detailed functional specifications and feature summary documents to define the requirements and features of web applications clearly.',
			'Designing interactive layouts and interfaces to create user-friendly web applications.',
			'Designing the database schema and developing web applications.',
			'Ensuring the high quality and compatibility of web applications across multiple browsers through Unit testing and quality assurance processes.',
			'Performing upgrades and regular maintenance to keep web applications up-to-date and fully functional.',
		],
	},
	{
		title: 'Software Engineer',
		company_name: 'Entrata India Private Limited',
		icon: entrata,
		iconBg: '#E6DEDD',
		date: 'October 2021 - Present',
		points: [
			'Collaborating with cross-functional teams to execute the complete software development life cycle using Agile methodologies.',
			'Writing well-designed, efficient, and testable code to meet software requirements.',
			'Optimizing databases and writing efficient queries to ensure optimal performance.',
			'Writing efficient Unit tests to verify the correctness and functionality of software components.',
			'Developing APIs for Android and iOS applications to provide seamless integration with software components.',
			'Debugging and upgrading existing systems to resolve issues and improve functionality.',
			'Documenting and maintaining software functionality, including technical specifications, user manuals, etc.',
		],
	},
];

const testimonials = [
	{
		testimonial:
			"What sets Sachin apart is his ability to effectively collaborate with cross functional teams and lead discussions. He is a kind, supportive colleague, and he is always eager to learn and improve. He's an exceptional Software Engineer who possesses a range of technical and personal qualities that make him a valuable asset to any team in the IT industry.",
		name: 'Raj Kumar Mohite',
		designation: 'Engineering Manager',
		company: 'Entrata India',
		image: raj,
	},
	{
		testimonial:
			'Sachin is a stellar developer! He never shied away from a difficult task and he would ask questions to better understand use cases so he could develop all intersections of function around his code. He has a keen eye for quality and is a natural problem solver. Sachin is a pleasure to work with.',
		name: 'Chris Bills',
		designation: 'Product Manager',
		company: 'Entrata, Inc.',
		image: chris,
	},
	{
		testimonial:
			'Sachin is quality driven, which is crucial in developing high performance software. He stays up-to-date with the latest trends in the industry, making him well-rounded and adaptable. One of his outstanding qualities is his human qualities, including his polite nature and kind personality, which make him a pleasure to work with.',
		name: 'Sachin Kumar Singh',
		designation: 'Co-Founder',
		company: 'SaviSoft',
		image: sachin,
	},
];

const projects = [
	{
		name: 'CloudBook',
		description:
			'Cloud Book is a digital notebook that stores your data on the cloud, accessible from anywhere with powerful encryption for secure protection.',
		tags: [
			{
				name: 'node',
				color: 'green-text-gradient',
			},
			{
				name: 'express',
				color: 'pink-text-gradient',
			},
			{
				name: 'react',
				color: 'blue-text-gradient',
			},
			{
				name: 'mongodb',
				color: 'green-text-gradient',
			},
			{
				name: 'bootstrap',
				color: 'pink-text-gradient',
			},
			{
				name: 'restAPI',
				color: 'blue-text-gradient',
			},
		],
		image: cloudBook,
		source_code_link:
			'https://github.com/ersachinsaurav/Projects/tree/main/MERN/CloudBook',
	},
	{
		name: 'NewsBilla',
		description:
			'NewsBilla is a user-friendly news app powered by newsapi.org. It provides up-to-the-minute news coverage and allows customisation of news feed.',
		tags: [
			{
				name: 'node',
				color: 'green-text-gradient',
			},
			{
				name: 'react',
				color: 'blue-text-gradient',
			},
			{
				name: 'mongodb',
				color: 'green-text-gradient',
			},
			{
				name: 'express',
				color: 'pink-text-gradient',
			},
			{
				name: 'newsAPI',
				color: 'blue-text-gradient',
			},
		],
		image: newsBilla,
		source_code_link:
			'https://github.com/ersachinsaurav/Projects/tree/main/MERN/NewsApp_ClassBased',
	},
	{
		name: 'NodeChat',
		description:
			'NodeChat is a chat application built using Node.js, which allows users to communicate with each other in real-time through text-based messaging.',
		tags: [
			{
				name: 'node',
				color: 'green-text-gradient',
			},
			{
				name: 'react',
				color: 'blue-text-gradient',
			},
			{
				name: 'socket.io',
				color: 'green-text-gradient',
			},
			{
				name: 'express',
				color: 'pink-text-gradient',
			},
			{
				name: 'jasmineUnitTest',
				color: 'blue-text-gradient',
			},
		],
		image: nodeChat,
		source_code_link:
			'https://github.com/ersachinsaurav/Projects/tree/main/MERN/NodeChat',
	},
	{
		name: 'Blogera',
		description:
			'Blogera is a blogging app with an intuitive admin panel that allows bloggers to create, publish, and manage their content and site design.',
		tags: [
			{
				name: 'php',
				color: 'green-text-gradient',
			},
			{
				name: 'mysql',
				color: 'blue-text-gradient',
			},
			{
				name: 'html',
				color: 'green-text-gradient',
			},
			{
				name: 'css',
				color: 'pink-text-gradient',
			},
			{
				name: 'materialize',
				color: 'blue-text-gradient',
			},
		],
		image: blogera,
		source_code_link:
			'https://github.com/ersachinsaurav/Projects/tree/main/PHP/Blogera',
	},
	{
		name: 'WeatherBot',
		description:
			"WeatherBot is a weather reporting app that provides real-time weather updates based on the user's current location or IP address.",
		tags: [
			{
				name: 'javascript',
				color: 'green-text-gradient',
			},
			{
				name: 'restAPI',
				color: 'pink-text-gradient',
			},
			{
				name: 'css',
				color: 'blue-text-gradient',
			},
			{
				name: 'html',
				color: 'green-text-gradient',
			},
			{
				name: 'geoLocation',
				color: 'pink-text-gradient',
			},
		],
		image: weatherBot,
		source_code_link:
			'https://github.com/ersachinsaurav/Projects/tree/main/JavaScript/WeatherBOT',
	},
	{
		name: 'Other Projects',
		description:
			'This GitHub folder contains a collection of practice works demonstrating my web development skills and knowledge.',
		tags: [
			{
				name: 'php',
				color: 'green-text-gradient',
			},
			{
				name: 'postgreSQL',
				color: 'blue-text-gradient',
			},
			{
				name: 'text2PNG',
				color: 'green-text-gradient',
			},
			{
				name: 'pdfGenerator',
				color: 'blue-text-gradient',
			},
		],
		image: sauraviCafe,
		source_code_link: 'https://github.com/ersachinsaurav/Projects',
	},
];

export { services, technologies, experiences, testimonials, projects };
