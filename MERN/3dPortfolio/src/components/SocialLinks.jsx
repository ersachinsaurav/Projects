import React from 'react';
import { motion } from 'framer-motion';
import { styles } from '../styles';
import { SectionWrapper } from '../hoc';
import { fadeIn, textVariant } from '../utils/motion';
import { github, linkedin } from '../assets';

const SocialLinks = () => {
	return (
		<>
			<motion.div variants={textVariant()}>
				<p className={styles.sectionSubText}>Get in touch</p>
				<h2 className={styles.sectionHeadText}>Other Ways to Connect</h2>
			</motion.div>

			<motion.div
				variants={fadeIn('', '', 0.1, 1)}
				className="mt-4 max-w-7xl mx-auto">
				<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
					{/* LinkedIn */}
					<motion.a
						href="https://in.linkedin.com/in/ersachinsaurav"
						target="_blank"
						rel="noopener noreferrer"
						className="flex items-center justify-center p-6 bg-tertiary rounded-lg transition-all duration-300 h-24"
						whileHover={{
							scale: 1.05,
							boxShadow: '0 0 15px rgba(145, 94, 255, 0.4)'
						}}
						whileTap={{ scale: 0.95 }}>
						<img src={linkedin} alt="linkedin" className="w-8 h-8 mr-4" />
						<span className="text-white text-lg">Connect on LinkedIn</span>
					</motion.a>

					{/* GitHub */}
					<motion.a
						href="https://github.com/ersachinsaurav"
						target="_blank"
						rel="noopener noreferrer"
						className="flex items-center justify-center p-6 bg-tertiary rounded-lg transition-all duration-300 h-24"
						whileHover={{
							scale: 1.05,
							boxShadow: '0 0 15px rgba(145, 94, 255, 0.4)'
						}}
						whileTap={{ scale: 0.95 }}>
						<img src={github} alt="github" className="w-8 h-8 mr-4" />
						<span className="text-white text-lg">View GitHub Profile</span>
					</motion.a>

					{/* Email */}
					<motion.a
						href="mailto:contact@sachinsaurav.dev"
						className="flex items-center justify-center p-6 bg-tertiary rounded-lg transition-all duration-300 h-24"
						whileHover={{
							scale: 1.05,
							boxShadow: '0 0 15px rgba(145, 94, 255, 0.4)'
						}}
						whileTap={{ scale: 0.95 }}>
						<svg
							className="w-8 h-8 mr-4 text-white"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								strokeLinecap="round"
								strokeLinejoin="round"
								strokeWidth={2}
								d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
							/>
						</svg>
						<span className="text-white text-lg">Email Me</span>
					</motion.a>
				</div>
			</motion.div>
		</>
	);
};

export default SectionWrapper(SocialLinks, 'social-links');
