import React from 'react';
import { Tilt } from 'react-tilt';
import { motion } from 'framer-motion';
import { styles } from '../styles';
import { services } from '../constants';
import { fadeIn, textVariant } from '../utils/motion';
import { SectionWrapper } from '../hoc';
import { isMobile } from 'react-device-detect';

const ServiceCard = ({ index, title, icon }) => {
	return (
		<Tilt className="xs:w-[250px] w-full">
			<motion.div
				variants={fadeIn('right', 'spring', 0.5 * index, 0.75)}
				className="w-full green-pink-gradient p-[1px] rounded-[20px] shadow-card">
				<div
					options={{
						max: 45,
						scale: 1,
						speed: 450,
					}}
					className="bg-tertiary rounded-[20px] py-5 px-12 min-h-[280px] flex justify-evenly items-center flex-col">
					<img
						src={icon}
						alt={title}
						className="w-20 h-20 object-contain mb-4"
					/>
					<h3 className="text-white text-[20px] font-bold text-center">
						{title}
					</h3>
				</div>
			</motion.div>
		</Tilt>
	);
};

const About = () => {
	return (
		<>
			<motion.div variants={textVariant()}>
				<p className={styles.sectionSubText}>Introduction</p>
				<h2 className={styles.sectionHeadText}>Overview</h2>
			</motion.div>
			<motion.p
				variants={fadeIn('', '', 0.1, 1)}
				className={`mt-4 text-secondary text-[17px] max-w-7xl leading-[30px] ${
					isMobile ? 'text-left' : 'text-justify'
				} `}>
				I help businesses translate their ideas into code by building scalable, user-friendly web applications and seamless software integrations. As a Senior Software Engineer with 6+ years of experience, I lead teams in delivering end-to-end solutions—from initial requirements analysis to final deployment and beyond.
				<br className="sm:block hidden" />
				Specializing in Agile methodologies and cloud-native architecture, I work closely with my team to ensure efficient collaboration, rapid iteration, and high-quality delivery. I'm passionate about building intuitive user interfaces and robust back-end systems, leveraging a diverse set of programming languages, frameworks, and tools to create innovative solutions that meet business needs.
				<br className="sm:block hidden" />
				In my current role, I take ownership of projects from scratch, guiding them through every phase of the software development lifecycle. I mentor engineers, promote cross-functional collaboration, and ensure clear communication to align technical solutions with business objectives. Driven by a passion for continuous learning, I stay on top of industry trends and emerging technologies, always striving to deliver lasting value to both my team and the business. My philosophy is simple: <span className="text-[#915eff]">elegant code solves complex problems</span> — a mindset I've carried since writing my first "Hello World" program at age 14.
			</motion.p>

			<div className="mt-20 flex flex-wrap gap-10">
				{services.map((service, index) => (
					<ServiceCard key={service.title} index={index} {...service} />
				))}
			</div>
		</>
	);
};

export default SectionWrapper(About, 'about');
